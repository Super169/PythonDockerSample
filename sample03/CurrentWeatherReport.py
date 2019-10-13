import requests
import os
import re
import MyUtil as mu

url = "http://rss.weather.gov.hk/rss/CurrentWeather.xml"
patterns = {
    'cdata': "<![\[]CDATA[\[](.*)]]>",
    'update_dtm': r"<title>Bulletin updated at (.*?)</title>",
    'icon': r" src=\"http://rss.weather.gov.hk/img/pic(\d+)[.]png\" ",
    'warning': r"<SPAN id=\'warning_message\' >(.*)</SPAN>",
    'temperature': r"<br/>[ ]*?Air temperature : (\d+) degrees Celsius<br/>",
    'humidity': r"<br/>[ ]*?Relative Humidity : (\d+(?:\.\d+)?) per cent<br/>",
    'UV Index': r"<br/>[ ]*?During the past hour the mean UV Index recorded at King''s Park : (\d+(?:\.\d+)?)<br/>",
    'UV Radiation': r"<br/>[ ]*?Intensity of UV radiation : ([^<]*)<br/>",
    'distTable': r"<tr>.*?<\/tr>",
    'distRow': r"<td><font size=\"-1\">(.*?)</font></td><td width=\"100\" align=\"right\"><font size=\"-1\">(\d+(?:\.\d+){0,1}) degrees [\.;]</font></td>",
}
#
# It seems that regular expression is much and much faster than XML
#
# Data source: http://rss.weather.gov.hk/rss/CurrentWeather.xml
#
def getData() -> object:

    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''

    data = {}

    response = requests.get(url)

    if response is None or response.text is None:
        return data

    xml = mu.RE.cleanResult(response.text)

    data['Update time'] = mu.RE.getFirst(xml, patterns.get('update_dtm'))

    result = re.search(patterns.get('cdata'), xml)

    if result is None:
        return data

    cdata = result.group()

    data['icon'] = mu.RE.getFirst(cdata, patterns.get('icon'))
    data['warning'] = mu.RE.getFirst(cdata, patterns.get('warning'))
    data['Temperature'] = mu.RE.getFirst(cdata, patterns.get('temperature'))
    data['Humidity'] = mu.RE.getFirst(cdata, patterns.get('humidity'))
    data['UV Index'] = mu.RE.getFirst(cdata, patterns.get('UV Index'), None)
    data['UV Radiation'] = mu.RE.getFirst(cdata, patterns.get('UV Radiation'), None)

    distTable = re.findall(patterns.get('distTable'), cdata)
    distData = {}
    for dist in distTable:
        distRow = re.findall(patterns.get('distRow'), dist)
        if distRow is not None and len(distRow) == 1 and len(distRow[0]) == 2:
            distData[distRow[0][0]] = distRow[0][1]

    data['distict temperture'] = distData

    return data


