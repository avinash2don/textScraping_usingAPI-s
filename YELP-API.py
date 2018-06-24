
# coding: utf-8

# In[1]:

import pip
import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize




# In[6]:

pip.main(["install","yelp3"])


# In[19]:

from yelp3.client import Client

apikey='FGMU22xaV1_98Pwz4dJTmJ9CGiQqQcRVRXFA22B--jnc5GbG6H0fwAXv_NC43G-7vQ3STBQQOljpWpeD776KItOFdeEte5Vj7Ps71Ox2pinPS_tUGTmg80qemx2PWnYx'

api = Client(apikey)


# In[20]:

params={'term':'Indian','limit':50,'offset':0}
val = api.business_search(location='New Jersey',**params)
df = json_normalize(val,'businesses')
df2 = json_normalize(val)


# In[21]:

#pip.main(['install','uszipcode'])
from uszipcode import ZipcodeSearchEngine

search = ZipcodeSearchEngine()
res = search.by_state(state='New Jersey',returns=0)
resdf = json_normalize(res)

zcode = resdf[0]
za = zcode.values
zc=za[-10:].tolist()
zc


# In[23]:

mdf = pd.DataFrame()
for i in zc:
    params={'term':'Indian','limit':50,'offset':0}
    val = api.business_search(location=i,**params)
    df = json_normalize(val)
    df2 = json_normalize(val,'businesses')
    t = df.loc[0,'total']
    mdf = mdf.append(df2,ignore_index=True)
    cnt=50
    while t>0:
        params={'term':'Indian','limit':50,'offset':cnt}
        val = api.business_search(location=i,**params)
        df2 = json_normalize(val,'businesses')
        mdf = mdf.append(df2,ignore_index=True)
        t = t-50
        cnt=cnt+50

mdf.shape


# In[24]:

mdf.columns


# In[25]:

#pip.main(['install','textblob'])
from textblob import TextBlob

idlist = mdf.id
idlist


# In[28]:

idlist = mdf['id'].tolist()

ps = []
for i in idlist:
    rev = api.review(i)
    dfrev = json_normalize(rev,'reviews')
    textlist = dfrev['text'].tolist()
    polarity = []
    for t in textlist:
        tx = TextBlob(t)
        polarity.append(tx.sentiment.polarity)
    pol = np.array(polarity)
    ps.append(pol.mean())  
    
ps


# In[27]:

mdf['pol']=pd.Series(ps)
mdf['location']


# In[29]:

mdf2 = mdf.location.apply(pd.Series)
mdf2['id']=mdf['id']
mdf2['pol']=mdf['pol']


gdf = mdf2.groupby(['id','zip_code'])['pol'].mean()
gdf2 = gdf.reset_index(True)




gdf2 = gdf.reset_index()
mdf2.shape
gdf2.shape

gdf2.columns


# In[30]:

mdf2.columns


# In[31]:

mdf['pol']=pd.Series(ps)
mdf['location']



# In[32]:

dictyelp = dict(zip(mdf2.id,mdf2.zip_code))

gdf2['zip_code']=gdf2['id'].map(dictyelp)    
gdf2.shape


# In[33]:

gdf4 = gdf2.groupby('zip_code')['pol'].mean()
gd5 = gdf4.reset_index()
gd5.sort_values('pol',ascending=False)


# In[34]:

resdf[resdf[0]=='07866']
resdf


# In[ ]:



