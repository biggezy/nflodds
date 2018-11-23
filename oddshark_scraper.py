#!/usr/bin/python3

import re
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
        "https://www.oddsshark.com{}".format(t["matchup_link"]),
        t["away_odds"],
	t["home_odds"],
	t["total"]
    )
    for t in r.json()['matchups']
    if t["type"] == "matchup"
]

for t in links:
  if "2018-11-25" in t[0]:
    date = t[0]
    awayteam = t[1]
    hometeam = t[2]
    gamelink = t[3]
    awayspread = t[4]
    homespread = t[5]
    overunder = t[6]
    r = requests.get(gamelink)
    soup = BeautifulSoup(r.content, "lxml")
    trends = [
        json.loads(v.text)
        for v in soup.findAll('script', {"type":"application/json", "id":"gc-data"})
    ]

    print("\n#########################################")
    print("{} - {} vs {} => {}\n".format(date, awayteam, hometeam, gamelink))
    print("O/U:", overunder, "\n")
    for side in ['away','home']:
      (team,spread) = (awayteam,awayspread) if side == 'away' else (hometeam, homespread)
      rawTrends = trends[0]["oddsshark_gamecenter"]["trends"][side]
      print (team, "(", spread, ")", side, "Trends")
      for rawTrend in rawTrends:
        parsedTrend = rawTrend["value"]
        if re.search("over|under", parsedTrend, re.IGNORECASE):
          print (parsedTrend)
