import lstm
import time
import matplotlib.pyplot as plt
from keras.models import load_model
import json
import numpy as np

def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()

def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    #Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.show()

#Main Run Thread
if __name__=='__main__':
	#hdf5_file_path = '/home/rudresh/Desktop/nse-tech/LSTM-Neural-Network-for-Time-Series-Prediction/model/my_model2.h5'
	
	global_start_time = time.time()
	epochs  = 30
	seq_len = 50

	print('> Loading data... ')
	fname_of_stock = 'MSFT'
	name_of_stock = '/home/rudresh/Desktop/nse-tech/LSTM-Neural-Network-for-Time-Series-Prediction/model/preds/'+fname_of_stock
	X_train, y_train, X_test, y_test = lstm.load_data(fname_of_stock+'.csv', seq_len, True)
	name_of_predictions = name_of_stock + '_prediction.json'
	name_of_yvalue = name_of_stock + '_yvalue.json'
	print('> Data Loaded. Compiling...')

	
	model = lstm.build_model([1, 50, 100, 1])

	model.fit(
	    X_train,
	    y_train,
	    batch_size=512,
	    nb_epoch=epochs,
	    validation_split=0.05)

	#model.save(hdf5_file_path)
	print ' XXXXXXXXXXX'
	print type(X_test)
	print X_test.shape	
	#model = load_model(hdf5_file_path)
	predictions = lstm.predict_sequences_multiple(model, X_test, seq_len, 50)
	#print type(predictions)
	print 'PREDICTIONSSS'
	print (type(predictions))
	print(len(predictions))
	print(len(predictions[0]))
	#predictions_folder = 'predictions.csv'

	#predicted = lstm.predict_sequence_full(model, X_test, seq_len)
	#predicted = lstm.predict_point_by_point(model, X_test)        
	print 'YTESSTTTTT'
	print type(y_test)
	print y_test.shape
	print('Training duration (s) : ', time.time() - global_start_time)
	plot_results_multiple(predictions, y_test, 50)

	predictions = [[np.asscalar(val) for val in sublist] for sublist in predictions]
	y_test = [np.asscalar(val) for val in y_test]
	
	with open(name_of_predictions,'w') as myfile:
		json.dump(predictions,myfile)
	
	with open(name_of_yvalue,'w') as myfile:
		json.dump(y_test,myfile)