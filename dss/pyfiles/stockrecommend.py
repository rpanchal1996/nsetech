import json
import csv
import random
import pandas as pd
import sys

def func():
	with open('dss/pyfiles/elonmuskpersonality.json') as json_data:
	    d = json.load(json_data)
	    df = []
	    df.append(d['personality'][0]['children'][0])
	    df.append(d['personality'][1]['children'][1])
	    df.append(d['needs'][5])
	    df.append(d['needs'][8])
	    df.append(d['needs'][10])
	    df.append(d['values'][0])
	    risk_taking = (df[0]['percentile'] + 1-df[1]['percentile'] + 1-df[2]['percentile'] + df[3]['percentile'] + 1-df[4]['percentile'] + 1-df[5]['percentile'])/6 * 100


	df = pd.read_csv("dss/static/volatility.csv")
	riskystocks = risk_taking/100*9
	safestocks = 9 - riskystocks
	count = 0;
	stockslist = []
	stockslist.append("{0:2.3f}".format(risk_taking))
	random.seed(a = 7)
	while count<9:
		randomno = random.randint(0,624)
		if(df.iloc[[randomno]].Risk.values > 0):
			if(riskystocks>0):
				riskystocks = riskystocks -1
				count = count + 1
				stockslist.append(df.loc[[randomno]].to_dict())

		else:
			if(safestocks>0):
				safestocks = safestocks -1
				count = count + 1
				stockslist.append(df.loc[[randomno]].to_dict())
	return stockslist