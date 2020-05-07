#!/usr/bin/env python3

from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json

headers = {"Host": "pre.steam-origin.contest.tuenti.net:9876"}

req_url = "http://steam-origin.contest.tuenti.net:9876/games/cat_fight/get_key"
req = Request(url=req_url, headers=headers)

try:
    with urlopen(req) as resp:
        data = json.loads(resp.read())
        print(data["key"])
except HTTPError as e:
    print(e)

