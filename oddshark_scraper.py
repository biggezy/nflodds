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
	t["home_odds"]
    )
    for t in r.json()['matchups']
    if t["type"] == "matchup"
]

for t in links:
  if "2018-11-11" in t[0]:
    print("\n#########################################") 
    print("{} - {} vs {} => {}\n".format(t[0],t[1],t[2],t[3]))
    awayteam = t[1]
    hometeam= t[2]
    awayspread = t[4]
    homespread = t[5]
    r = requests.get(t[3])
    soup = BeautifulSoup(r.content, "lxml")
    trends = [
        json.loads(v.text)
        for v in soup.findAll('script', {"type":"application/json", "id":"gc-data"})
    ]

    for side in ['away','home']:
      (team,spread) = (awayteam,awayspread) if side == 'away' else (hometeam, homespread)
      rawTrends = trends[0]["oddsshark_gamecenter"]["trends"][side]
      print (team, "(", spread, ")", side, "Trends")
      for rawTrend in rawTrends:
        parsedTrend = rawTrend["value"]
        if re.search("over|under", parsedTrend, re.IGNORECASE):
          print (parsedTrend)
