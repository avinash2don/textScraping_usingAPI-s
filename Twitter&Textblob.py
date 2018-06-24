import pip
pip.main(['install','twitter'])
pip.main(['install','textblob'])

from textblob import TextBlob
from twitter import Twitter
from twitter import OAuth
from twitter import TwitterHTTPError
from twitter import TwitterStream

#import numpy and pandas
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

#twitter keys
ck = "8bJblCJytUjPwL6cjiXLcLFHA"
cs = "zekjX633rs4BBjO1ygKdfkME0xSKdIfvCQq8e5rwfz9tRnFKOA" 
at = "1540262562-Zz8Ojh5Cb6GGtYE7hjbO4hMKaf7yrEapTNdfFPi"
ats = "mQUpJedDsDdlH8cRVHI9o3asgvl6hXSX8F31UZ3Lzlqyy"
oauth = OAuth(at,ats,ck,cs)

#OAuth


#Twitter search
api = Twitter(auth=oauth)



q='StudentsStandUp'
df = pd.DataFrame()
mid = 0
for i in range(10):
    if i==0:
        search_result = api.search.tweets(q=q, count = 100)
    else:
        search_result = api.search.tweets(q=q, count=100, max_id=mid)
        
    dftemp = json_normalize(search_result,'statuses')
    mid = dftemp['id'].min()
    mid = mid - 1
    df = df.append(dftemp, ignore_index = True)

df.shape

tweettext = df['text']


wordlist = pd.DataFrame()
for t in tweettext:
    tx = TextBlob(t)
    ww = []
    for word, tag in tx.tags:
        if tag in ('NN', 'NNS', 'NNP', 'NNPS'):
           ww.append(word.lemmatize())
    if len(ww) !=0:
        wordlist = wordlist.append(ww, ignore_index=True)

allword = wordlist.groupby(0).size()

top20allword = allword.sort_values(0,ascending=False).head(20)
top20allword.plot(kind='bar',title='Top 20 words')

