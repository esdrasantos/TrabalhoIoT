# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:23:25 2020

@author: Esdra
"""

import feedparser

'''NewsFeed = feedparser.parse("https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/3456068")
entry    = NewsFeed.entries[1]
teste    = entry.keys()
print (teste)
'''
NewsFeed = feedparser.parse('https://rss.weatherzone.com.au/?u=12994-1285&lt=twcid&lc=160258&obs=1&fc=1')
print (NewsFeed['feed']['title'])
entry = NewsFeed.entries[1]

print (entry.keys())