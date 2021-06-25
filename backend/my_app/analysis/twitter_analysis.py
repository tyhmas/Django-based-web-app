# Import Libraries
from textblob import TextBlob
import sys
import tweepy
# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

def authenticate():
	consumerKey = ""
	consumerSecret = ""
	accessToken = ""
	accessTokenSecret = ""
	auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
	auth.set_access_token(accessToken, accessTokenSecret)
	api = tweepy.API(auth)
	return api

def tweet_list_compose(tweets):
	tweet_list = []
	for tweet in tweets:    
		tweet_list.append(tweet.text)
		analysis = TextBlob(tweet.text)
		scores = SentimentIntensityAnalyzer().polarity_scores(tweet.text)

	tweet_list = pd.DataFrame(tweet_list)
	tweet_list["text"] = tweet_list[0]
	return tweet_list

# deduplicate and remove stop symbols
def tweet_preprocess(tw_list):
	tw_list.drop_duplicates(inplace = True)
	tw_list = pd.DataFrame(tw_list)
	tw_list["text"] = tw_list[0]

	remove_rt = lambda x: re.sub('RT @\w+: ', " ", x)
	rt = lambda x: re.sub("(@[A-Za-z0–9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x)
	tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
	tw_list["text"] = tw_list.text.str.lower()
	return tw_list

def count_values_in_column(data,feature):
    total=data.loc[:,feature].value_counts(dropna=False)
    percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
    return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])


def tweet_sentiment_process(tweet_list):
	tweet_list[['polarity', 'subjectivity']] = tweet_list['text'].apply(lambda Text: \
		pd.Series(TextBlob(Text).sentiment))
	for index, row in tweet_list['text'].iteritems():
		scores = SentimentIntensityAnalyzer().polarity_scores(row)
		neg_scores = scores['neg']
		neu_scores = scores['neu']
		pos_scores = scores['pos']
		comp_scores = scores['compound']
    	
		if neg_scores > pos_scores:
			tweet_list.loc[index, 'sentiment'] = "negative"
		elif pos_scores > neg_scores:
			tweet_list.loc[index, 'sentiment'] = "positive"
		else:
			tweet_list.loc[index, 'sentiment'] = "neutral"
   		
		tweet_list.loc[index, 'neg'] = neg_scores
		tweet_list.loc[index, 'neu'] = neu_scores
		tweet_list.loc[index, 'pos'] = pos_scores
		tweet_list.loc[index, 'compound'] = comp_scores

	return tweet_list


if __name__ == "__main__":
	keyword = "certikorg"
	count = 200
	
	api = authenticate()
	
	# compose a tweet list
	tweets = api.search(q=keyword, count=count)
	tweet_list = tweet_list_compose(tweets)

	tweet_list = tweet_preprocess(tweet_list)
	tweet_list = tweet_sentiment_process(tweet_list)
	draw_piechart(tweet_list)
	create_wordcloud(tweet_list["text"].values)