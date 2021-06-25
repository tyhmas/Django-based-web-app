from django.shortcuts import render
from django.http import JsonResponse
from .twitter_analysis import authenticate, tweet_list_compose, \
							tweet_preprocess, tweet_sentiment_process

# Create your views here.
def index(request):
	"""View function for home page of site."""
	print(f"Here in index")
	return render(request, 'index.html', context = None)

def init_list():
	"""Twitter API authentication and tweets preprocessing."""
	keyword = "certikorg"
	count = 200
	api = authenticate()
	tweets = api.search(q=keyword, count=count)
		
	# compose a tweet list
	tweet_list = tweet_list_compose(tweets)
	tweet_list = tweet_preprocess(tweet_list)
	return tweet_list

def sentimental_analysis(tweet_list):
	tweet_list = tweet_sentiment_process(tweet_list)
	print(f"Done sentimental_analysis")
	# tweet_list is DataFrame
	# print(f"type of tweet_list is {type(tweet_list)}")
	response = JsonResponse(tweet_list.to_json(), safe=False)
	print(f"response is {response}")
	return response

def word_cloud(tweet_list):
	print(f"Done word_cloud")
	return JsonResponse(tweet_list["text"].values, safe=False)

def sa_process(request):
	tweet_list = init_list()
	return sentimental_analysis(tweet_list)
	# return [sentimental_analysis(tweet_list), word_cloud(tweet_list)]

def wc_process(request):
	print(f"Hahahah")
	# tweet_list = init_list()
	# return word_cloud(tweet_list)