#!/bin/bash

function report_result() {
    # Gets the return value `$?` of the last command and reports success or not
    if [ $? -eq 0 ]; then
        echo -e "Success."
    else
        echo -e "\nSomething went wrong! Bailing..."
        exit 1
    fi
}

# venv
echo -e "\n*** Activating the python virtual environment for this script..."
OS=$(uname -a | cut -c1-5)
report_result
if [[ $OS =~ "Linux" ]]; then
    echo "Making adjustments due to bad choice of operating system"
    source venv/bin/activate
else
    source venv/Scripts/activate
fi
report_result
echo -e "Using: $(which python)"

# upgrade pip
echo -e "\n*** Updating pip to latest version...\n"
python -m pip install --upgrade pip
report_result

# pip install
echo -e "\n*** Installing latest Python requirements...\n"
python -m pip install -r requirements.txt
report_result

# pre-commit install
echo -e "\n*** Installing any new pre-commit hooks\n"
python -m pre_commit install
report_result

# create alg_conf.json file
echo -e "\n*** Creating api_conf.json file"
cat > src/api_conf.json << EOF
{
  "APCA_API_KEY_ID": "Enter api key here",
  "APCA_API_SECRET_KEY": "Enter secret key here",
  "APCA_API_BASE_URL": "https://paper-api.alpaca.markets",
  "APCA_API_DATA_URL": "https://data.alpaca.markets",
  "APCA_RETRY_MAX": -1,
  "APCA_RETRY_WAIT": -1,
  "APCA_RETRY_CODES": -1,
  "DATA_PROXY_WS": ""
}

EOF

# setup post-merge hook
echo -e "\n*** Installing post-merge hooks"
cat > .git/hooks/post-merge << EOF
#!/bin/bash

# Run on successful merge
echo -e "\n*** Running post-merge hook\n"

EOF
report_result

echo -e "\nSetup Completed Successfully."
