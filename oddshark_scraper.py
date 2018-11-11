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
        "https://www.oddsshark.com{}".format(t["matchup_link"])
    )
    for t in r.json()['matchups']
    if t["type"] == "matchup"
]

for t in links:
  if "2018-11-11" in t[0]:
    print("#########################################")   
    print("{} - {} vs {} => {}\n".format(t[0],t[1],t[2],t[3]))
    awayteam = t[1]
    hometeam= t[2]
    r = requests.get(t[3])
    soup = BeautifulSoup(r.content, "lxml")
    trends = [
        json.loads(v.text)
        for v in soup.findAll('script', {"type":"application/json", "id":"gc-data"})
    ]

    awayTrends = trends[0]["oddsshark_gamecenter"]["trends"]["away"]
    print (awayteam, "(AWAY) Trends")
    for rawTrend in awayTrends:
      parsedTrend = rawTrend["value"]
      if re.search("over|under", parsedTrend, re.IGNORECASE):
        print (parsedTrend)


    homeTrends = trends[0]["oddsshark_gamecenter"]["trends"]["home"]
    print (hometeam, "(HOME) Trends")
    for rawTrend in homeTrends:
      parsedTrend = rawTrend["value"]
      if re.search("over|under", parsedTrend, re.IGNORECASE):
        print (parsedTrend)
