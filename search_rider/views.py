from django.shortcuts import render
from django.conf import settings
import requests
URL = "https://api.nexon.co.kr/kart/v1.0/"
headers = {"Authorization": settings.API_KEY}


def index(request):
    print(get_access_id("SFll폭주M"))
    return render(request, "home.html", {})


def search(request):
    return


def get_access_id(nickname):
    res = requests.get(URL + "users/nickname/" + nickname, headers=headers)
    # res.encoding = 'utf-8'
    res = res.json()

    return res["accessId"]
