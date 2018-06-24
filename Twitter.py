import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import twitter
from twitter import Twitter
from twitter import OAuth

ck = "8bJblCJytUjPwL6cjiXLcLFHA"
cs = "zekjX633rs4BBjO1ygKdfkME0xSKdIfvCQq8e5rwfz9tRnFKOA" 
at = "1540262562-Zz8Ojh5Cb6GGtYE7hjbO4hMKaf7yrEapTNdfFPi"
ats = "mQUpJedDsDdlH8cRVHI9o3asgvl6hXSX8F31UZ3Lzlqyy"


oauth = OAuth(at,ats,ck,cs)

api = Twitter(auth=oauth)

df = pd.DataFrame()
mid = 0
for i in range(10):
    if i==0:
        search_result = api.search.tweets(q="Liverpool FC",count = 100)
    else:
        search_result = api.search.tweets(q="Liverpool FC",count = 100, max_id = mid)
    
    dftemp = json_normalize(search_result,'statuses')
    mid = dftemp['id'].min()
    mid = mid - 1
    df = df.append(dftemp,ignore_index=True)

    
tweettext = df['text']    

wordlist = pd.DataFrame()

for u in tweettext:
    wsplit = u.split()
    wordlist = wordlist.append(wsplit, ignore_index = True)

wordlist.head()    

allword = wordlist.groupby(0).size()
allword.head()

top20word = allword.sort_values(0,ascending=False).head(30)
top20word.plot(kind='bar',title='Top 20 words')