from management_metadata.models import *
from django.conf import settings
import requests
from datetime import timedelta, datetime

URL = "https://api.nexon.co.kr/kart/v1.0/"
headers = {"Authorization": settings.API_KEY}


def get_access_id(nickname):
    res = requests.get(URL + "users/nickname/" + nickname, headers=headers)
    # res.encoding = 'utf-8'
    res = res.json()

    return res["accessId"]


def get_matches(access_id):
    res = requests.get(URL + "users/" + access_id + "/matches?start_date=&end_date=&offset=0&limit=30&match_types=",
                       headers=headers)
    res = res.json()

    tmp = []
    for m in res["matches"]:
        tmp += m["matches"]

    matches = []
    tmp.sort(key=lambda x: x["startTime"])
    for m in tmp:
        match = dict()
        match['match_id'] = m['matchId']
        match['player_count'] = m['playerCount']
        match['rank'] = m['player']['matchRank']

        try:
            match['match_type'] = GameType.objects.get(gametype_id=m['matchType'])
        except:
            match['match_type'] = '-'

        try:
            match['character'] = Character.objects.get(character_id=m['character'])
        except:
            match['character'] = '-'

        try:
            match['kart'] = Kart.objects.get(kart_id=m['player']['kart'])
        except:
            match['kart'] = '-'

        try:
            match['track'] = Track.objects.get(track_id=m['trackId'])
        except:
            match['track'] = '-'

        match['character_img'] = m['character']
        match['kart_img'] = m['player']['kart']
        match['track_img'] = m['trackId']

        match_time = m['player']['matchTime']
        if match_time == '':
            match['match_time'] = '-'
        else:
            match['match_time'] = match_time_calc(match_time)

        match['before_time'] = before_time_calc(m['startTime'])

        matches.append(match)

    return matches


def match_time_calc(time):
    tmp = str(timedelta(0, 0, 0, int(time))).split(':')
    return tmp[1][1] + '`' + tmp[2][:2] + '`' + tmp[2][3:5]


def before_time_calc(start_time):
    diff = str(datetime.now() - datetime.fromisoformat(start_time))
    diff_tmp = str(datetime.now() - datetime.fromisoformat(start_time)).split()

    if not diff_tmp[1].isnumeric():
        return diff_tmp[0] + '일전'
    else:
        diff = diff.split(':')
        if int(diff[0]) == 0:
            if int(diff[1]) == 0:
                return '방금전'
            else:
                return diff[1] + '분전'
        else:
            return diff[0] + '시간전'

