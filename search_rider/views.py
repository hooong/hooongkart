from django.shortcuts import render, redirect
from search_rider.service import *
from django.contrib import messages


def index(request):
    recent_search = request.COOKIES.get('recent_search')

    context = {'recent_search': []}
    for id in recent_search.split()[::-1]:
        context['recent_search'].append(get_nickname(id))

    return render(request, "search.html", context=context)


def detail(request):
    nickname = request.GET['nickname']
    access_id = get_access_id(nickname)
    recent_search = request.COOKIES.get('recent_search')

    if not access_id:
        messages.error(request, "존재하지 않는 닉네임입니다.")
        return redirect('/')
    else:
        if recent_search:
            recent_search = recent_search.split()

            if len(recent_search) == 5:
                recent_search.pop(0)
            recent_search.append(access_id)
        else:
            recent_search = [access_id]

        matches = get_matches(access_id)
        context = {'nickname': nickname, 'matches': matches}

        response = render(request, "detail.html", context=context)
        response.set_cookie('recent_search', ' '.join(recent_search))
        return response


