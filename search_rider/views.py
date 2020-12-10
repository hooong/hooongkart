from django.shortcuts import render
from django.conf import settings
import requests
URL = "https://api.nexon.co.kr/kart/v1.0/"
headers = {"Authorization": settings.API_KEY}


def index(request):
    return render(request, "search.html", {})


def detail(request):
    nickname = request.GET['nickname']
    access_id = get_access_id(nickname)

    context = {'nickname': nickname, 'access_id': access_id}
    return render(request, "detail.html", context=context)


def get_access_id(nickname):
    res = requests.get(URL + "users/nickname/" + nickname, headers=headers)
    # res.encoding = 'utf-8'
    res = res.json()

    return res["accessId"]
