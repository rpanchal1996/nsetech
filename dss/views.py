from django.shortcuts import render
from .pyfiles import stockrecommend , sentiment
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.http import HttpResponse
from .models import *
import csv
import pandas
import os
from django.contrib.staticfiles.templatetags.staticfiles import static
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

def reportAnalysis(request):
	root_path = r'C:\Users\Jarvis\Desktop\Projects\NSEhackathon\nse_tech\dss\static\yash\\'
	# root_path = static('yash/')
	# root_path = '/home/rudresh/Desktop/nse-tech/GIT_FOLDER_DO_NOT_MESS/nsetech/dss/static/yash/'
	filepaths = os.listdir(root_path)
	to_send_master = []
	for filepath in filepaths:
		to_send = []
		filepath = root_path+filepath
		with open(filepath,'r') as myfile:
			reader = csv.reader(myfile, delimiter=',')
			for row in reader:
				dict_to_add = {}
				dict_to_add['period'] = row[0]
				dict_to_add['zscore'] = "{0:2.3f}".format(float(row[1]))
				dict_to_add['stock'] = "{0:2.3f}".format(float(row[2])/10)
				to_send.append(dict_to_add)
		to_send_master.append(to_send)
	print (to_send_master)
	return render(request, 'zScore.html',{'to_send':to_send_master})

def portfolio(request):
	# root_path = '/home/rudresh/Desktop/nse-tech/GIT_FOLDER_DO_NOT_MESS/nsetech/dss/static/'
	# filepaths = os.listdir(root_path)
	# to_send_master = []
	# for filepath in filepaths:
	to_send = []
	labels = []
	data1 = []
	data2 = []
	# 	filepath = root_path+filepath
	with open('dss/static/investor.csv','r') as myfile:
		reader = csv.reader(myfile, delimiter=',')
		for row in reader:
			labels.append(row[0])
			data1.append(row[1])
			data2.append(float(row[2])*10)
	print(labels)
	return render(request, 'portfolio.html', {"labels" : labels, 'data1':data1,'data2' :data2})

def sentiment_prediction(request):
	sentiment =[]
	print("rUFBG")
	route = str(os.path.dirname(os.path.realpath(__file__)))
	with open(route +'/sentiment.json') as myfile:
		sentiment = json.load(myfile)
	print(sentiment)
	return render(request, 'sentiment_prediction.html',{'sentiment' : sentiment} )


def rnn_prediction(request, id):
	obj = stock.objects.get(id=id)
	route = str(os.path.dirname(os.path.realpath(__file__)))
	predictions = []
	yvalues = []
	prediction_file= route+'/results/'+ obj.stock_name + '_prediction.json'
	yvalue_file =  route+'/results/'+ obj.stock_name + '_yvalue.json'
	with open(prediction_file,'r') as myfile:
		predictions = json.load(myfile)
	with open(yvalue_file,'r') as myfile:
		yvalues = json.load(myfile)
	to_render = []
	index = 1
	for index,prediction in enumerate(predictions):
		startvalue = index*50
		endvalue = startvalue + 50
		for pred,y in zip(prediction,yvalues[startvalue:endvalue]):
			to_send = {}
			to_send['yvalues']= str(y)
			to_send['pred'] = str(pred)
			to_send['index'] = str(index)
			index+=1
			to_render.append(to_send)
	print(to_render)
	return render(request, 'rnn_prediction.html', {"graphpoints" : to_render})
	# return HttpResponse("ok")


def reuters_prediction(request, id):
	obj = stock.objects.get(id=id)
	route = str(os.path.dirname(os.path.realpath(__file__)))
	predictions = []
	yvalues = []
	prediction_file= route+'/sentiment-headlines/'+ obj.stock_name + '.json'
	with open(prediction_file,'r') as myfile:
		predictions = json.load(myfile)
	print(type(predictions))
	predictions = json.loads(predictions)
	'''
	to_render = []
	index = 1
	for index,prediction in enumerate(predictions):
		startvalue = index*50
		endvalue = startvalue + 50
		for pred,y in zip(prediction,yvalues[startvalue:endvalue]):
			to_send = {}
			to_send['yvalues']= str(y)
			to_send['pred'] = str(pred)
			to_send['index'] = str(index)
			index+=1
			to_render.append(to_send)
	print(to_render)
	'''
	return render(request, 'reuters_prediction.html', {"graphpoints" : predictions[100:500]})


def summarization(request):
	route = str(os.path.dirname(os.path.realpath(__file__)))
	filepath = route+'/static/aapl.txt'
	text = ''
	with open(filepath,'r',encoding="utf8") as myfile:
		text = myfile.read()
	print (text)
	return render(request,'report_summarization.html', {'context' : text})

	#f = open(os.path.join(root_path, 'aapl.txt'))
