# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 19:17:52 2020

@author: azaman
"""
import praw
import pandas as pd
import datetime as dt

pds = pd.read_csv('appdata.secret',header=None)
pds.columns = ['Key','Value']

reddit = praw.Reddit(client_id=pds.Value[0], \
                     client_secret=pds.Value[1], \
                     user_agent=pds.Value[2], \
                     username=pds.Value[3], \
                     password=pds.Value[4])
    
subreddit = reddit.subreddit('cybersecurity')
top_subreddit = subreddit.top(limit=10)

topics_dict = { "title":[], "score":[], "id":[], "url":[], "comms_num": [], "created": [], "body":[]}

for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)
    
topics_data = pd.DataFrame(topics_dict)

def get_date(created):
    return dt.datetime.fromtimestamp(created)
_timestamp = topics_data["created"].apply(get_date)
topics_data = topics_data.assign(timestamp = _timestamp)    
topics_data.to_csv('grabbed_data/cybersecurity-top-1000-20200831.csv', index=True)