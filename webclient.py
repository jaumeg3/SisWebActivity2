#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :
import sys
import urllib2
from bs4 import BeautifulSoup

api_key = None


class WeatherClient(object):
    """docstring for WeatherClient."""
    url_base = "http://api.wunderground.com/api/"
    url_service = {
        "almanac": "/almanac/almanac/q/CA/"
    }

    def __init__(self, api_key):
        super(WeatherClient, self).__init__()
        self.api_key = api_key

    def get_web_page(self, location):
        url = self.url_base + self.api_key + self.url_service["almanac"] + \
              location + ".xml"
        f = urllib2.urlopen(url)
        data = f.read()
        f.close()
        return data

    def parse_web_page(self, data):
        soup = BeautifulSoup(data, 'lxml')

        result = {}
        result["maximes"] = {}
        result["minimes"] = {}

        maximes = soup.find("temp_high")
        result["maximes"]["normal"] = maximes.find("normal").find("c").text
        result["maximes"]["record"] = maximes.find("record").find("c").text

        minimes = soup.find("temp_low")
        result["minimes"]["normal"] = minimes.find("normal").find("c").text
        result["minimes"]["record"] = minimes.find("record").find("c").text

        return result

    def almanac(self, location):
        """Get the web-page, read and return the results"""
        data = self.get_web_page(location)
        data = self.parse_web_page(data)
        return data


if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
            wc = WeatherClient(api_key)
            result = wc.almanac("Lleida")
            print result
        except IndexError:
            print "Error, No API key"
