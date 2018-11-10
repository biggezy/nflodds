import requests
import json
from bs4 import BeautifulSoup
import lxml

r = requests.get(
    'https://io.oddsshark.com/ticker/nfl', 
    headers = {
        'referer': 'https://www.oddsshark.com/nfl/scores'
    }
)

links = [
    (
        t["event_date"], 
        t["away_name"], 
        t["home_name"], 
        "https://www.oddsshark.com{}".format(t["matchup_link"])
    )
    for t in r.json()['matchups']
    if t["type"] == "matchup"
]

for t in links:
    print("{} - {} vs {} => {}".format(t[0],t[1],t[2],t[3]))
    r = requests.get(t[3])
    soup = BeautifulSoup(r.content, "lxml")
    trends = [
        json.loads(v.text)
        for v in soup.findAll('script', {"type":"application/json", "id":"gc-data"})
    ]
    print(trends[0]["oddsshark_gamecenter"]["trends"])
    print("#########################################")
