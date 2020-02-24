import requests
import json


sportsrada_key = "8pw73uw6jd2wvkarxwzaz5m5"
url = "https://api.sportradar.us/ncaamb/trial/v7/en/seasons/2019/reg/teams/2f4d21f8-6d5f-48a5-abca-52a30583871a/statistics.json?api_key=" + sportsrada_key



response = requests.get(url)

if response.status_code != 200:
    print(str(response) )
    sys.exit()



data = response.text


parsed = json.loads(data)

print(json.dumps(parsed, indent=4))