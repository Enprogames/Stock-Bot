from django.http import HttpRequest
from django.shortcuts import render


def index(request):
    return render(request, 'stock_bot/index.html')