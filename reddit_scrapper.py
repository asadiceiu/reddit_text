# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 19:17:52 2020

@author: azaman
"""
import praw
import pandas as pd
import datetime as dt
import numpy as np
import json, requests, re


def get_date(created):
    return dt.datetime.fromtimestamp(created)

def preprocess_text(txt):
    txt.lower()
    # convert all urls into "URL"
    txt = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',txt)
    #correct all multispace white spaces to single one
    txt = re.sub('[\s]+', ' ', txt)
    # convert all newlines into single spaces
    txt = txt.replace("\n"," ").replace("\r"," ")
    return txt.encode('ascii', 'ignore').decode('ascii') ## converts all non-ascii characters to ascii


keywords = ['vulnerability','cybersecurity', 'cyber-crime', 'cybercrime', 'cyber crime', 'CVE', 'CVEs', 'CVE-', 'cyber attack']

for q in keywords:
    print('\nKeyword: ', q)
    url = 'https://api.pushshift.io/reddit/search/submission/?q={}&after=2071d&aggs=subreddit&size=500'.format(q)
    subs_r = requests.get(url)
    subs = pd.DataFrame(subs_r.json()["aggs"]['subreddit'])
    for sub in subs['key']:
        print("\nSUBREDDIT:",sub)
        data_dict = {"topic":[],"subreddit":[],"title":[],"score":[],"id":[],"url":[],"created":[],"body":[]}
        for d in range(1,2071,30):
            try:
                url_submission = "https://api.pushshift.io/reddit/search/submission/?q={}&subreddit={}&after={}d&before={}d&size=500".format(q,sub,d+30,d)
                response = requests.get(url_submission)
                json_data = response.json()["data"]
                for submission in json_data:
                    print(submission['author'],end=' ')
                    txt = preprocess_text(submission['selftext'])
                    if len(txt)<20: continue
                    data_dict['topic'].append(q)
                    data_dict['subreddit'].append(sub)
                    data_dict['title'].append(preprocess_text(submission['title']))
                    data_dict['score'].append(submission['score'])
                    data_dict['id'].append(submission['id'])
                    data_dict['url'].append(submission['url'])
                    data_dict['created'].append(get_date(submission['created_utc']))
                    data_dict['body'].append(txt)
            except:
                continue

        sub_data = pd.DataFrame(data_dict)
        sub_data.to_csv("grabbed_data/keyword/"+sub+"-data-"+q.replace(" ",'_')+".csv")


'''
#### Read Json From Pushshift API
## Getting data from 1 January 2015 onward
#https://api.pushshift.io/reddit/search/submission/?q=cybersecurity&after=1500d&before=1250d&aggs=subreddit

## 1st Task: Get all subreddits with submissions for he keyword "cybersecurity" 
url = 'https://api.pushshift.io/reddit/search/submission/?q=vulnerability&after=2071d&aggs=subreddit&size=0'
r = requests.get(url)
v_subs = pd.DataFrame(r.json()["aggs"]["subreddit"])
r = requests.get('https://api.pushshift.io/reddit/search/submission/?q=cybersecurity&after=2071d&aggs=subreddit&size=0')
cybersecurity_subs = pd.DataFrame(r.json()["aggs"]["subreddit"])



combined = pd.concat([v_subs, cybersecurity_subs]).groupby(["key"], as_index=False)["doc_count"].sum()


## 2nd Task get submissions day by day
data_dict = {"topic":[],"subreddit":[],"title":[],"score":[],"id":[],"url":[],"created":[],"body":[]}
url= 'https://api.pushshift.io/reddit/search/submission/?q=cybersecurity&subreddit=cybersecurity'
q_list = ['vulnerability','cybersecurity']
for sub in np.array(combined['key'])[1:len(combined)]:
    print("\nSUBREDDIT:",sub)
    data_dict = {"topic":[],"subreddit":[],"title":[],"score":[],"id":[],"url":[],"created":[],"body":[]}
    for q in q_list:
        for d in range(1,2071,30):
            try:
                url = "https://api.pushshift.io/reddit/search/submission/?q={}&subreddit={}&after={}d&before={}d&size=500".format(q,sub,d+30,d)
                response = requests.get(url)
                json_data = response.json()["data"]
                for submission in json_data:
                    print(submission['author'],end=' ')
                    txt = preprocess_text(submission['selftext'])
                    if len(txt)<20: continue
                    data_dict['topic'].append(q)
                    data_dict['subreddit'].append(sub)
                    data_dict['title'].append(preprocess_text(submission['title']))
                    data_dict['score'].append(submission['score'])
                    data_dict['id'].append(submission['id'])
                    data_dict['url'].append(submission['url'])
                    data_dict['created'].append(get_date(submission['created_utc']))
                    data_dict['body'].append(txt)
            except:
                continue
    sub_data = pd.DataFrame(data_dict)
    sub_data.to_csv("grabbed_data/"+sub+"-data-all.csv")

'''


