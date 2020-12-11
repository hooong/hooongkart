import psycopg2
import json


def insert_data(data, d_name):
    table = "management_metadata_" + d_name

    for d in data:
        id = d["id"]
        name = d["name"]
        cur.execute("INSERT INTO " + table + " (" + d_name + "_id" + ", name) VALUES (%s, %s)", (id, name))


with open("/Users/hooong/secret.json") as f:
    secret = json.load(f)

database = secret["database"]
conn_string = "host='" + database["HOST"] + "' dbname='" + database["NAME"] + "' user='" + database["USER"] + "' password='" + database["PASSWORD"] + "'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

base = "/Users/hooong/PycharmProjects/kartriderProject/management_metadata/metadata/"
with open(base + "character.json") as f:
    character = json.load(f)

with open(base + "flyingPet.json") as f:
    flyingpet = json.load(f)

with open(base + "gameType.json") as f:
    gametype = json.load(f)

with open(base + "pet.json") as f:
    pet = json.load(f)

with open(base + "kart.json") as f:
    kart = json.load(f)

with open(base + "track.json") as f:
    track = json.load(f)

insert_data(character, 'character')
insert_data(flyingpet, 'flyingpet')
insert_data(gametype, 'gametype')
insert_data(pet, 'pet')
insert_data(kart, 'kart')
insert_data(track, 'track')

conn.commit()

cur.close()
conn.close()
