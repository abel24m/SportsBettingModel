import http.client

conn = http.client.HTTPSConnection("api.sportradar.us")

key = "8pw73uw6jd2wvkarxwzaz5m5"

conn.request("GET", "/ncaamb/trial/v4/en/games/2019/reg/schedule.xml?api_key=8pw73uw6jd2wvkarxwzaz5m5")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
