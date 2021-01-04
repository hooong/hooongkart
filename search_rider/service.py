from management_metadata.models import *
from django.conf import settings
import requests, json
from datetime import timedelta, datetime
from django.core.cache import cache

URL = "https://api.nexon.co.kr/kart/v1.0/"
headers = {"Authorization": settings.API_KEY}

# 메타데이터 load
characters = dict()
game_types = dict()
karts = dict()
tracks = dict()

base = "/Users/hooong/PycharmProjects/kartriderProject/management_metadata/metadata/"
with open(base + "character.json") as f:
    character = json.load(f)
for element in character:
    characters[element['id']] = element['name']

with open(base + "gameType.json") as f:
    gametype = json.load(f)
for element in gametype:
    game_types[element['id']] = element['name']

with open(base + "kart.json") as f:
    kart = json.load(f)
for element in kart:
    karts[element['id']] = element['name']

with open(base + "track.json") as f:
    track = json.load(f)
for element in track:
    tracks[element['id']] = element['name']


def get_access_id(nickname):
    res = requests.get(URL + "users/nickname/" + nickname, headers=headers)
    # res.encoding = 'utf-8'
    if not res.status_code == 200:
        return False

    res = res.json()
    return res["accessId"]


def get_nickname(access_id):
    res = requests.get(URL + "users/" + access_id, headers=headers)
    res.encoding = 'utf-8'
    res = res.json()

    return res["name"]


def get_matches(access_id):
    res = requests.get(URL + "users/" + access_id + "/matches?start_date=&end_date=&offset=0&limit=10&match_types=",
                       headers=headers)

    res = res.json()

    tmp = []
    for m in res["matches"]:
        tmp += m["matches"]

    # DB
    # game_types = GameType.objects.all().values('gametype_id', 'name')
    # characters = Character.objects.all().values('character_id', 'name')
    # karts = Kart.objects.all().values('kart_id', 'name')
    # tracks = Track.objects.all().values('track_id', 'name')

    # Redis
    # game_types = cache.get_or_set('gametypes', GameType.objects.all().values('gametype_id', 'name'))
    # characters = cache.get_or_set('characters', Character.objects.all().values('character_id', 'name'))
    # karts = cache.get_or_set('karts', Kart.objects.all().values('kart_id', 'name'))
    # tracks = cache.get_or_set('tracks', Track.objects.all().values('track_id', 'name'))

    # print(len(list(game_types)))
    # print(len(list(characters)))
    # print(len(list(karts)))
    # print(len(list(tracks)))

    matches = []
    tmp.sort(key=lambda x: x["startTime"], reverse=True)
    for m in tmp:
        match = dict()
        match['match_id'] = m['matchId']
        match['player_count'] = m['playerCount']
        match['rank'] = m['player']['matchRank']

        try:
            match['match_type'] = game_types[m['matchType']]
        except:
            match['match_type'] = '-'

        try:
            match['character'] = characters[m['character']]
        except:
            match['character'] = '-'

        try:
            match['kart'] = karts[m['player']['kart']]
        except:
            match['kart'] = '-'

        try:
            match['track'] = tracks[m['trackId']]
        except:
            match['track'] = '-'


        # DB
        # try:
        #     match['match_type'] = GameType.objects.get(gametype_id=m['matchType']).name
        # except:
        #     match['match_type'] = '-'

        # try:
        #     match['character'] = Character.objects.get(character_id=m['character'])
        #     # match['character'] = cache.get_or_set('characters:' + m['character'], Character.objects.get(character_id=m['character']).name)
        # except:
        #     match['character'] = '-'
        #
        # try:
        #     match['kart'] = Kart.objects.get(kart_id=m['player']['kart'])
        #     # match['kart'] = cache.get_or_set('karts:' + m['player']['kart'], Kart.objects.get(kart_id=m['player']['kart']).name)
        # except:
        #     match['kart'] = '-'
        #
        # try:
        #     match['track'] = Track.objects.get(track_id=m['trackId'])
        #     # match['track'] = cache.get_or_set('tracks:' + m['trackId'], Track.objects.get(track_id=m['trackId']).name)
        # except:
        #     match['track'] = '-'

        # Redis
        # for game_type in game_types:
        #     if game_type['gametype_id'] == m['matchType']:
        #         match['match_type'] = game_type['name']
        #         break
        # else:
        #     match['match_type'] = '-'
        #
        # for character in characters:
        #     if character['character_id'] == m['character']:
        #         match['character'] = character['name']
        #         break
        # else:
        #     match['character'] = '-'
        #
        # for kart in karts:
        #     if kart['kart_id'] == m['player']['kart']:
        #         match['kart'] = kart['name']
        #         break
        # else:
        #     match['kart'] = '-'
        #
        # for track in tracks:
        #     if track['track_id'] == m['trackId']:
        #         match['track'] = track['name']
        #         break
        # else:
        #     match['track'] = '-'

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
    diff_tmp = diff.split()

    if len(diff_tmp) > 2:
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

