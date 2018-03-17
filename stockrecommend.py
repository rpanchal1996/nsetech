import json
import csv
import random
import pandas as pd 

with open('elonmuskpersonality.json') as json_data:
    d = json.load(json_data)
    #print(d)
    df = []
    df.append(d['personality'][0]['children'][0])
    df.append(d['personality'][1]['children'][1])
    df.append(d['needs'][5])
    df.append(d['needs'][8])
    df.append(d['needs'][10])
    df.append(d['values'][0])
    print(df)
    risk_taking = (df[0]['percentile'] + 1-df[1]['percentile'] + 1-df[2]['percentile'] + df[3]['percentile'] + 1-df[4]['percentile'] + 1-df[5]['percentile'])/6 * 100


print(risk_taking)

df = pd.read_csv("dss/static/volatility.csv")
riskystocks = risk_taking/100*5
safestocks = 5 - riskystocks
count = 0;
random.seed(a = 7)

while count<5:
	randomno = random.randint(0,624)
	print(randomno)
	if(df.iloc[[randomno]].Risk.values > 0):
		if(riskystocks>0):
			print(df.iloc[[randomno]])
			riskystocks = riskystocks -1
			count = count + 1

	else:
		if(safestocks>0):
			print(df.iloc[[randomno]])
			safestocks = safestocks -1
			count = count + 1