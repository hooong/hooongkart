from django.shortcuts import render
from search_rider.service import *


def index(request):
    return render(request, "search.html", {})


def detail(request):
    nickname = request.GET['nickname']
    access_id = get_access_id(nickname)

    if not access_id:
        context = {'error': '존재하지 않는 닉네임입니다.'}
        return render(request, "search.html", context=context)
    else:
        matches = get_matches(access_id)

        context = {'nickname': nickname, 'matches': matches}
        return render(request, "detail.html", context=context)


