from twitter import Twitter
from twitter import OAuth
from twitter import TwitterHTTPError
from twitter import TwitterStream

#import numpy and pandas
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import newspaper

url = 'https://www.bloomberg.com/news/articles/2018-02-22/if-you-believe-quants-nothing-happened-in-markets-this-month'
article = newspaper.Article(url)
article.download()
article.parse()
article.title
article.nlp()
article.keywords
article.summary
blob2 = TextBlob(article.text)
blob2.sentences[1]

wordlist = pd.DataFrame()
ssList=[]
for t in blob2.sentences:
    ww = []
    for word, tag in t.tags:
        if tag in ('NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'):
            ww.append(word.lemmatize())
    ss = ' '.join(ww)
    ssList.append(ss.lower())
wordlist = wordlist.append(ssList, ignore_index=True)    

wordlist
len(blob2.sentences)
wordlist.to_csv('summary.csv')

