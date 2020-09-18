# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 21:11:32 2020

@author: Esdra

by Bruno Vermeulen on StackOverflow
"""

import feedparser
import webbrowser



feed = feedparser.parse("https://rss.weatherzone.com.au/?u=12994-1285&lt=twcid&lc=160258&obs=1&fc=1")

# feed_title = feed['feed']['title']  # NOT VALID
feed_entries = feed.entries
rss_text = open("rsstext.txt", 'w+')

for entry in feed.entries:

    article_title = entry.title
    article_link = entry.link
    article_description = entry.description # Unicode string
    #article_description_at_parsed = entry.description_parsed # Time object
    # article_author = entry.author  DOES NOT EXIST
    content = entry.summary
    
    print ("{}[{}]".format(article_title, article_link))
    print ("Published at {}".format(article_description))
    print("Content {}".format(content))
    
    

