#!/bin/bash

function report_result() {
    # Gets the return value '$?'' of the last command and reports success or not
    last_cmd=$?
    if [[ $last_cmd -eq 0 ]]; then
        echo -e "Success."
    else
        echo -e "\nSomething went wrong! Bailing..."
        exit 1
    fi
}

OS=$(uname -a | cut -c1-5)
# venv
## create venv
echo -e "\n*** Checking to see if virtual environment exists"
if [[ -d "/venv" ]]; then
    echo -e "\n*** Creating new virtual environment using python-venv"
    if [[ $OS =~ "Linux" ]]; then
        echo "Making adjustments due to bad choice of operating system"
        python3 -m venv venv --prompt stock-bot
    else
        python -m venv venv --prompt stock-bot
    fi
    report_result
else
    echo -e "\n Virtual environment already exists in this directory."
fi

## activate venv
echo -e "\n*** Activating the python virtual environment for this script..."
if [[ $OS =~ "Linux" ]]; then
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

# This script will run on a successful merge

function report_result() {
    # Gets the return value '$?' of the last command and reports success or not
    if [[ $? -eq 0 ]]; then
        echo -e "Success."
    else
        echo -e "\nSomething went wrong! Bailing..."
        exit 1
    fi
}

echo -e "\n*** Running post-merge hook\n"
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
EOF

echo -e "post-merge hooks installed at .git/hooks/post-merge"
report_result

echo -e "\nSetup Completed Successfully."
