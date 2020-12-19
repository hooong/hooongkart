from django.shortcuts import render
from search_rider.service import *
import binascii


def index(request):
    cookie = request.COOKIES.get('recent_search')

    context = {'recent_search': ''}
    if cookie:
        context['recent_search'] = cookie

    return render(request, "search.html", context=context)


def detail(request):
    nickname = request.GET['nickname']
    access_id = get_access_id(nickname)

    if not access_id:
        context = {'error': '존재하지 않는 닉네임입니다.'}
        return render(request, "search.html", context=context)
    else:
        matches = get_matches(access_id)
        context = {'nickname': nickname, 'matches': matches}

        response = render(request, "detail.html", context=context)
        response.set_cookie('recent_search', nickname.encode('utf-8'))

        return response


