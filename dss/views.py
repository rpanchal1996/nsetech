from django.shortcuts import render
from .pyfiles import stockrecommend , sentiment
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.http import HttpResponse
from .models import *
# Create your views here.

def index (request):
	return render(request, 'base.html')

def risk (request):
	risk = stockrecommend.func()
	print(risk)
	RiskValues = []
	TickerId = []
	Stocks = []
	lenth = len(risk)
	for i in range(1,lenth):
		T_id = risk[i]['Ticker']
		R_num = risk[i]['Risk']
		TickerId.append(list(T_id.values())[0])
		RiskValues.append("{0:2.3f}".format(list(R_num.values())[0]))
		Stocks.append({"T_id" : str(list(T_id.values())[0]), "Risk":"{0:2.3f}".format(list(R_num.values())[0])})
	print(TickerId)
	return render(request, 'risk.html', {"Stocks" : Stocks,"TickerId" : TickerId, "RiskValues" : RiskValues, "RiskCap" : risk[0]})

def news (request):
	obj = stock.objects.all()
	return render(request, 'news_based.html', {"stocks" : obj})

@csrf_exempt
def tweet (request, id):
	if request.method == "GET":
		obj = stock.objects.get(id=id)
		stock_tweets = sentiment.tweet_sentiment(obj.stock_name)
		print(stock_tweets)
		url = '/stock/'+ str(id)
		return render(request, 'stock_detail.html', {"StockName" : stock_tweets, "StockData" : obj, "url":url})
	elif request.method == "POST":
		ticker = request.POST.get("StockName")
		stock_tweets = sentiment.tweet_sentiment(ticker)
		return HttpResponse(json.dumps(stock_tweets), content_type="application/json")

@csrf_exempt
def getTweetFeeds(request):
	ticker = request.POST.get("StockName")
	stock_tweets = sentiment.tweet_sentiment(obj.stock_name)
	return HttpResponse(json.dumps(stock_tweets), content_type="application/json")	