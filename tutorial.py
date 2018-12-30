import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
# print(page)
# <Response [200]>

# print(page.status_code)
# 200

# print(page.content)
# b'<!DOCTYPE html>\n<html>\n    <head>\n        <title>A simple example page</title>\n    </head>\n    <body>\n

soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())
# <!DOCTYPE html>
# <html>
#  <head>
#   <title>
#    A simple example page
#   </title>
#  </head>
#  <body>
#   <p>
#    Here is some simple content for this page.
#   </p>
#  </body>
# </html>

# print(list(soup.children))
# ['html', '\n', <html>
# <head>
# <title>A simple example page</title>
# </head>
# <body>
# <p>Here is some simple content for this page.</p>
# </body>
# </html>]

# print([type(item) for item in list(soup.children)])
# [<class 'bs4.element.Doctype'>, <class 'bs4.element.NavigableString'>, <class 'bs4.element.Tag'>]

html = list(soup.children)[2]
# ['\n', <head>
# <title>A simple example page</title>
# </head>, '\n', <body>
# <p>Here is some simple content for this page.</p>
# </body>, '\n']

body = list(html.children)[3]
# ['\n', <p>Here is some simple content for this page.</p>, '\n']

p = list(body.children)[1]
# Here is some simple content for this page.

# print(soup.find_all('p'))
# [<p>Here is some simple content for this page.</p>]

# print(soup.find_all('p')[0].get_text())
# Here is some simple content for this page.

# print(soup.find('p'))
# <p>Here is some simple content for this page.</p>

page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup = BeautifulSoup(page.content, 'html.parser')
# <html>
# <head>
# <title>A simple example page</title>
# </head>
# <body>
# <div>
# <p class="inner-text first-item" id="first">
#                 First paragraph.
#             </p>
# <p class="inner-text">
#                 Second paragraph.
#             </p>
# </div>
# <p class="outer-text first-item" id="second">
# <b>
#                 First outer paragraph.
#             </b>
# </p>
# <p class="outer-text">
# <b>
#                 Second outer paragraph.
#             </b>
# </p>
# </body>
# </html>

soup.find_all('p', class_='outer-text')
# soup.find_all(class_='outer-text')
# [<p class="outer-text first-item" id="second">
# <b>
#                 First outer paragraph.
#             </b>
# </p>, <p class="outer-text">
# <b>
#                 Second outer paragraph.
#             </b>
# </p>]

soup.find_all(id="first")
# [<p class="inner-text first-item" id="first">
#                 First paragraph.
#             </p>]

soup.select("div p")
# [<p class="inner-text first-item" id="first">
#                 First paragraph.
#             </p>, <p class="inner-text">
#                 Second paragraph.
#             </p>]

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.XASDUWhKgWU")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
tonight.prettify()
# <div class="tombstone-container"> <p class="period-name"> Tonight <br/> <br/> </p> <p> <img alt="Tonight: Partly
# cloudy, with a low around 46. East northeast wind 5 to 9 mph. " class="forecast-icon"
# src="newimages/medium/nsct.png" title="Tonight: Partly cloudy, with a low around 46. East northeast wind 5 to 9
# mph. "/> </p> <p class="short-desc"> Partly Cloudy </p> <p class="temp temp-low"> Low: 46 °F </p> </div>

period = tonight.find(class_="period-name").get_text()
# Tonight
short_desc = tonight.find(class_="short-desc").get_text()
# Partly Cloudy
temp = tonight.find(class_="temp").get_text()
# Low: 46 °F
img = tonight.find("img")
desc = img['title']
# Tonight: Partly cloudy, with a low around 46. East northeast wind 5 to 9 mph.

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
# ['Tonight', 'Monday', 'MondayNight', 'Tuesday', 'TuesdayNight', 'Wednesday', 'WednesdayNight', 'Thursday',
# 'ThursdayNight']

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
# []
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

# print(short_descs)
# print(temps)
# print(descs)

weather = pd.DataFrame({
        "period": periods,
        "short_desc": short_descs,
        "temp": temps,
        "desc": descs
})

temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
# 0    46
# 1    55
# 2    49
# 3    54
# 4    50
# 5    54
# 6    50
# 7    57
# 8    48
# Name: temp_num, dtype: object

weather["temp_num"].mean()
# 54.44444444444444444

is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
# 0     True
# 1    False
# 2     True
# 3    False
# 4     True
# 5    False
# 6     True
# 7    False
# 8     True
# Name: temp, dtype: bool







