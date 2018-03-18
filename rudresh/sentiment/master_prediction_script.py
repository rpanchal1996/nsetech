from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model
from sklearn import preprocessing
from datetime import datetime, timedelta
import time
from collections import Counter
import os
import json
os.chdir('..')


##### HELPERS #####
def prettify_ax(ax):
    ''' make an axis pretty '''
    for spine in ax.spines.itervalues():
        spine.set_visible(False)
    ax.set_frameon=True
    ax.patch.set_facecolor('#eeeeef')
    ax.grid('on', color='w', linestyle='-', linewidth=1)
    ax.tick_params(direction='out')
    ax.set_axisbelow(True)
    
def simple_ax(figsize=(6,4), **kwargs):
    ''' single prettified axis '''
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, **kwargs)
    prettify_ax(ax)
    return fig, ax

def earliest_date_after(query_date, date_list):
    ''' find the earliest date after a query date from ordered list of dates '''
    for i in range(len(date_list)):
        if query_date < date_list[i].date():
            return date_list[i].date()
    print '\nQUERY DATE ERROR WITH:', query_date, '\n'
    raise Exception('No values after query date')

def latest_date_before(query_date, date_list):
    ''' find the latest date before a query date from ordered list of dates '''
    for i in range(len(date_list)):
        if query_date < date_list[i].date():
            if i==0:
                print '\nQUERY DATE ERROR WITH:', query_date, '\n'
                raise Exception('No values before query date in list')
            return date_list[i-1].date()
        
def inv_price_transform(normalized_data, scaler):
    ''' inverse from normalized price to raw price '''
    m = scaler.mean_[0]
    s = scaler.scale_[0]
    return s*np.array(normalized_data)+m



def prep_data(ticker,
              stock_file = 'data/stock/prices-split-adjusted.csv', \
              news_directory = 'data/news/', \
              econ_file = 'data/market/economic_indicators.csv', \
              reddit_file = 'data/market/reddit_sentiments.csv'):
    ''' merge stock closing price data, sec filing data, and newspaper sentiment into one dataframe '''
    
    # load data
    stock_df = pd.read_csv(stock_file, index_col=0)
    stock_df = stock_df[stock_df.symbol==ticker].close
    stock_df.index = pd.to_datetime(stock_df.index)
    news_df = pd.read_csv(news_directory+ticker+'.csv', index_col=0)
    news_df.index = pd.to_datetime(news_df.index)
    econ_df = pd.read_csv(econ_file, index_col=0)
    econ_df.index = pd.to_datetime(econ_df.index)
    reddit_df = pd.read_csv(reddit_file, index_col=0)
    reddit_df.index = pd.to_datetime(reddit_df.index)
    return_df = pd.DataFrame(columns=[stock_df.name]+['stock_'+a for a in list(news_df.columns)]+\
                             list(econ_df.columns)+['market_'+a for a in list(reddit_df.columns)])
    
    # clip price data that doesn't have news coverage or reddit coverage
    d0, d1 = news_df.index[0].date(), news_df.index[1].date()
    startdate = d0-(d1-d0)
    stock_df = stock_df.loc[startdate:]
    
    # iterate through rows, aggregating all data and appending to return_df
    for row_num in range(stock_df.shape[0]):
        new_row = []
        stock_date = stock_df.index[row_num].date()
        new_row += [stock_df.iloc[row_num]]
        new_row += list(news_df.loc[earliest_date_after(stock_date, news_df.index),:])
        new_row += list(econ_df.loc[latest_date_before(stock_date, econ_df.index),:])
        new_row += list(reddit_df.loc[earliest_date_after(stock_date, reddit_df.index),:])
        return_df.loc[stock_date] = new_row
        if row_num % 100 == 0:
            print "%i/%i rows done." % (row_num, stock_df.shape[0]),
    print "\n%s dataframe prepped. %i timepoints, each with %i features." % \
          (ticker, return_df.shape[0], return_df.shape[1])
    return return_df

# practice with AAPL stock data
aapl_df = prep_data('AAPL')
print(aapl_df.head())

def load_stock(df, lookback=25):
    ''' scale data and split into training/test sets '''
    data = df.values
    n_train = list(df.index).index(df.index[-1]+timedelta(-365))
    scaler = preprocessing.StandardScaler() #normalize mean-zero, unit-variance
    scaler.fit(data[:n_train,:])
    data = scaler.transform(data)
    dataX, dataY = [], []
    for timepoint in range(data.shape[0]-lookback):
        dataX.append(data[timepoint:timepoint+lookback,:])
        dataY.append(data[timepoint+lookback,0])
    X_train, X_test = dataX[:n_train], dataX[n_train:]
    y_train, y_test = dataY[:n_train], dataY[n_train:]
    return np.array(X_train), np.array(y_train), np.array(X_test), np.array(y_test), scaler

# load practice stock, AAPL
lookback = 25
X_train, y_train, X_test, y_test, scaler = load_stock(df=aapl_df, lookback=lookback)

print "%i training examples, %i test examples" % (len(y_train), len(y_test))

'''
f,a = simple_ax(figsize=(10,6))
a.plot(range(len(y_train)), inv_price_transform(y_train, scaler), c='b', label='Training Data')
a.plot(range(len(y_train),len(y_test)+len(y_train)), inv_price_transform(y_test, scaler), c='r', label='Test Data')
a.set_title('AAPL Normalized Stock Price Data')
a.set_xlabel('Day')
a.set_ylabel('Closing price')
plt.legend()
plt.show()
'''
# build model
'''
model = Sequential()
model.add(LSTM(128, input_shape=(X_train.shape[1],X_train.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=False))
model.add(Dropout(0.2))
#model.add(Dense(32, kernel_initializer="uniform", activation='relu'))        
model.add(Dense(1, activation='linear'))
model.compile(loss='mse', optimizer='rmsprop')
#model.summary()

t0 = time.time()
history = model.fit(
            X_train,
            y_train,
            batch_size=512,
            epochs=200,
            validation_split=0.05,
            verbose=0)
print "TRAINING DONE. %i seconds to train." % int(time.time()-t0)
'''
'''
f,a = simple_ax(figsize=(10,6))
a.plot(history.history['loss'], label='loss')
a.plot(history.history['val_loss'], label='val_loss')
a.set_title('Training Losses')
a.set_xlabel('Epoch')
a.set_ylabel('MSE Loss')
plt.legend()
plt.show()
'''
save_folder_base = '/home/rudresh/Desktop/nse-tech/Stock-Prediction/models/outputs_buy_sell/'


model = load_model('/home/rudresh/Desktop/nse-tech/Stock-Prediction/models/model1.h5')
predictions = model.predict(X_test)

print "RMSE: ", np.sqrt(np.mean((predictions-y_test)**2))

with open(save_folder_base+'predictions.csv','w') as myfile:
    for value in predictions:
        myfile.write(str(value[0])+'\n')

'''
f, a = simple_ax(figsize=(10,6))
a.plot(predictions, c='b', label='predictions')
a.plot(y_test, c='r', label='actual')
a.set_ylabel('Normalized closing price')
a.set_xlabel('Day')
a.set_title('AAPL Test Set Predictions')
plt.legend()
plt.show()
'''

def predict_days(startday, days_topredict, data, model):
    ''' starting from startday predict days_topredict stock prices '''
    curr_data = data[startday,:,:]
    predictions = []
    for day in range(days_topredict):
        prediction = model.predict(curr_data.reshape(1,curr_data.shape[0],curr_data.shape[1]))[0][0]
        predictions.append(prediction)
        new_row = curr_data[-1,:]
        new_row[0] = prediction
        curr_data = np.vstack((curr_data[1:,:], new_row))
    return predictions

days = 30
predictions_json = []
f, a = simple_ax(figsize=(10,6))
a.plot(inv_price_transform(y_test,scaler), c='k')
for segment in range(int(len(y_test)/days)):
    predictions = predict_days(segment*days, days, X_test, model)
    predictions_json.append(predictions)
    a.plot(range(segment*days, segment*days+days), inv_price_transform(predictions, scaler))
    a.axvline(segment*days, c='k', linestyle='dashed', linewidth=1)
    a.axvline(segment*days+days, c='k', linestyle='dashed', linewidth=1)
a.set_xlabel('Day')
a.set_ylabel('Price')
a.set_title('AAPL Test Set 30 Day Lookahead')
#plt.show()

predictions_json = [[np.asscalar(val) for val in sublist] for sublist in predictions_json]
print predictions_json

with open(save_folder_base+'prediction_list.json','w') as myfile:
    json.dump(predictions_json,myfile)

def decide_buy_sell(startpoint, days_topredict, data, model, return_threshold):
    '''
    predict future prices and return a market decision
    - returns True: "buy long"
    - returns False: "sell short"
    - returns None: "do nothing"
    '''
    predictions = predict_days(startpoint, days_topredict, data, model)
    startprice, maxprice, minprice = predictions[0], max(predictions), min(predictions)
    buyreturn = (maxprice-startprice)/startprice
    sellreturn = (startprice-minprice)/startprice
    if buyreturn>=sellreturn and buyreturn>=return_threshold:
        return True
    elif sellreturn>buyreturn and sellreturn>=return_threshold:
        return False
    return None

def walk_buy_sell(data, model, return_threshold=.05, days_topredict=30):
    ''' walk data making buy/sell decisions '''
    buy_dates, sell_dates = [], []
    for t in range(len(y_test)):
        decision = decide_buy_sell(t, days_topredict, data, model, return_threshold)
        if decision is True:
            buy_dates.append(t)
        elif decision is False:
            sell_dates.append(t)
        if t%20==0:
            print "%i/%i timepoints calculated." % (t+1,len(y_test)),
    print "Data walk complete."
    return buy_dates, sell_dates

buy_dates, sell_dates = walk_buy_sell(X_test, model, return_threshold=0.5, days_topredict=30)


save_folder_base = '/home/rudresh/Desktop/nse-tech/Stock-Prediction/models/outputs_buy_sell/'

with open(save_folder_base+'stock_value.csv','w') as myfile:
    for value in y_test:
        myfile.write(str(value)+'\n')

print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
print sell_dates
print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
print buy_dates
print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

with open(save_folder_base+'buy_date.csv','w') as myfile:
    for value in buy_dates:
        myfile.write(str(value)+'\n')
with open(save_folder_base+'sell_date.csv','w') as myfile:
    for value in sell_dates:
        myfile.write(str(value)+'\n')

f,a = simple_ax(figsize=(10,6))
a.plot(inv_price_transform(y_test, scaler), c='k')
a.scatter(buy_dates, inv_price_transform(y_test[buy_dates],scaler), c='b')
a.scatter(sell_dates, inv_price_transform(y_test[sell_dates],scaler), c='y')
a.set_xlabel('Day')
a.set_ylabel('Price')
a.set_title('Buy/Sell Decisions for AAPL Test Set')
recs = [mpatches.Rectangle((0,0),1,1,fc='b'), mpatches.Rectangle((0,0),1,1,fc='y')]
a.legend(recs,['buy', 'sell'], loc=2, prop={'size':14})
plt.show()