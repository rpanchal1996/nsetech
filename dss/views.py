from django.shortcuts import render
from .pyfiles import stockrecommend
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
	return render(request, 'news_based.html')