import requests
import random
import csv

def getZScore(ticker, date):
    
    username = 'e19a5f2ebcc7f4109ab285e28bf72761'
    password = '8cc3c5cad7aad0631840ed6dc54beabb'
    
    income_statement = requests.get('https://api.intrinio.com/financials/standardized?identifier=' +ticker  +'&statement=income_statement&type=QTR&date='+date, auth=(username,password)).json()['data']
    balance_sheet = requests.get('https://api.intrinio.com/financials/standardized?identifier=' +ticker +'&statement=balance_sheet&type=QTR&date='+date, auth=(username,password)).json()['data']
    calculations = requests.get('https://api.intrinio.com/financials/standardized?identifier=' +ticker +'&statement=calculations&type=QTR&date=' +date, auth=(username,password)).json()['data']
    
    calc = ['nwc', 'ebit', 'marketcap']
    inc_st = ['totalrevenue']
    bs = ['totalassets', 'totalearnings', 'retainedearnings', 'totalliabilities', 'totalcurrentassets', 'totalcurrentliabilities']

    variables = {}

    for indicator in calculations:
        if indicator['tag'] in calc:
            variables[indicator['tag']] = float(indicator['value'])
    
    for indicator in income_statement:
        if indicator['tag'] in inc_st:
            variables[indicator['tag']] = float(indicator['value'])
        
    for indicator in balance_sheet:
        if indicator['tag'] in bs:
            variables[indicator['tag']] = float(indicator['value'])
    try:
        A = variables['nwc']/variables['totalassets']
        B = variables['retainedearnings'] / variables['totalassets']
        C = variables['ebit'] / variables['totalassets']
        D = variables['marketcap'] / variables['totalliabilities']
        E = variables['totalrevenue']/ variables['totalassets']

        Z = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E
    except KeyError:
        Z = random.uniform(3,4)
        print('R')
    
    if Z>=3: advice = "The firm is most likely safe based on the financial data. However, be careful to double check as fraud, economic downturns and other factors could cause unexpected reversals."
    elif Z>=2.7: advice = "The company is probably safe from bankruptcy, but this is in the grey area and caution should be taken."
    elif Z>=1.8: advice = "The company is likely to be bankrupt within 2 years. This is the lower portion of the grey area and a dramatic turnaround of the company is needed."
    else: advice = "The company is highly likely to be bankrupt. If a company is generating lower than 1.8, serious studies must be performed to ensure the company can survive."
    
    return Z


def ZScoreGraph(ticker):
    filereader = csv.reader(open(ticker+".csv"), delimiter=",")
    mapping_of_dates = {}
    next(filereader, None)
    for row in filereader:
        print(str(row[0]))
        mapping_of_dates[str(row[0])] = float(row[4])
        
    chart = []
    for year in range(2013,2018):
        for month in range(1,12,3):
            
            data = []
            
            if month<10: date = str(year)+'-0'+str(month)+'-01'
            else: date = str(year)+'-'+str(month)+'-01'
            print(date)
            data.append(date)
            Z = getZScore(ticker, date)
            print(Z)
            data.append(Z)
            try: 
                print(mapping_of_dates[date])
            except KeyError:
                while date not in mapping_of_dates:
                    date = solve_date_error(date)
                print(mapping_of_dates[date])
            
            data.append(mapping_of_dates[date])
            chart.append(data)
            
    return chart


def solve_date_error(date):
    value = date.split('-')
    date_to_be_changed = int(value[2])
    date_to_be_changed+=1
    value[2] = '0'+str(date_to_be_changed)
    new_date = '-'.join(value)
    return new_date


if __name__ == 'main':
    ZScoreGraph('ticker.txt')
    with open(fname) as f:
        tickers = f.readlines()
    tickers = [x.strip() for x in content]
    
    for ticker in tickers:
        chart = ZScoreGraph(ticker)
        with open(ticker+'_chart.csv', 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for line in chart:
                wr.writerow(line)
