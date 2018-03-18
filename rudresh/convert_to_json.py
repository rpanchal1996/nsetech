import json
def convert_sentiment_to_json():
	base = '/home/rudresh/Desktop/nse-tech/GIT_FOLDER_DO_NOT_MESS/nsetech/rudresh/sentiment/models/outputs_buy_sell/'
	stock_values = []
	with open(base+'stock_value.csv') as myfile:
		stock_values = myfile.readlines()
		stock_values = [float(str(value).strip()) for value in stock_values]
		print stock_values
		print len(stock_values)
	buy_dates = []

	with open(base+'buy_date.csv') as myfile:
		buy_dates = myfile.readlines()
		buy_dates = [int(str(value).strip()) for value in buy_dates]
		print buy_dates
		print len(buy_dates)
	with open(base+'sell_date.csv') as myfile:
		sell_dates = myfile.readlines()
		sell_dates = [int(str(value).strip()) for value in sell_dates]
		print sell_dates
		print len(sell_dates)
	master_data = []
	for idx, value in enumerate(stock_values):
		idx_copy = idx+1
		
		if idx_copy in sell_dates:
			val = {}
			val['period'] = idx_copy
			val['stock'] = value
			val['sell'] = value
			val['buy'] = 'Null'
			master_data.append(val) 

		else:
			if idx_copy in buy_dates:
				val = {}
				val['period'] = idx_copy
				val['stock'] = value
				val['buy'] = value
				val['sell'] = 'Null'
				master_data.append(val)

			else:
				val = {}
				val['period'] = idx_copy
				val['stock'] = value
				val['buy'] = 'Null'
				val['sell'] = 'Null'
				master_data.append(val)
	#print(len(master_data)) 
	print(master_data)
	with open('sentiment.json','w') as myfile:
		json.dump(master_data,myfile)

convert_sentiment_to_json()

