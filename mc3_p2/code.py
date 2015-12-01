__author__ = 'jfalkson'

import KNNLearner as knn

from util import *

import pandas as pd
import numpy as np
import csv


# CONFIG

# Training dates
start_date = '2008-01-01'
end_date = '2009-12-31'
symbol = ['ML4T-399']
symbol_str = 'ML4T-399'

dates = pd.date_range(start_date, end_date)
symbol_prices = get_data(symbol,dates)


# GET ALL DATA SO THAT WE CAN QUERY PREDICTIONS
symbol_prices_out_of_sample = get_data(symbol,pd.date_range('2008-01-01','2010-12-31'))
five_day_return_all = (symbol_prices_out_of_sample[symbol].values[5:]/symbol_prices_out_of_sample[symbol][:-5])-1
symbol_prices_mean_all = pd.rolling_mean(symbol_prices_out_of_sample[symbol],20)
symbol_price_stdev_all = pd.rolling_std(symbol_prices_out_of_sample[symbol],20)
# Feature 1, bollinger band value
bb_value_all = (symbol_prices_out_of_sample[symbol] - symbol_prices_mean_all.ix[19:,:])/(2 * symbol_price_stdev_all)

# Feature 2, momentum
momentum_all = (symbol_prices_out_of_sample[symbol][3:] /symbol_prices_out_of_sample[symbol].ix[:-3].values)-1

# Feature 3, 3 day 20day-volatility change
volatility_all = (symbol_price_stdev_all[3:] / symbol_price_stdev_all[:-3].values ) - 1
x_test_all = pd.concat([volatility_all, momentum_all, bb_value_all[2:]], axis=1)[20:]

x_test_all = x_test_all.loc['2010-01-01':'2010-12-31']

symbol_prices_out_of_sample_only  = symbol_prices_out_of_sample.loc['2010-01-01':'2010-12-31']

'''
STEP 1: COMPUTE THE 3 X FEATURES WE WILL USE TO TRAIN OUR MODEL

'''


five_day_return = (symbol_prices[symbol].values[5:]/symbol_prices[symbol][:-5])-1
symbol_prices_mean = pd.rolling_mean(symbol_prices[symbol],20)
symbol_price_stdev = pd.rolling_std(symbol_prices[symbol],20)

# Feature 1, bollinger band value
bb_value = (symbol_prices[symbol] - symbol_prices_mean.ix[19:,:])/(2 * symbol_price_stdev)

# Feature 2, momentum
momentum = (symbol_prices[symbol][3:] /symbol_prices[symbol].ix[:-3].values)-1

# Feature 3, 3 day 20day-volatility change
volatility = (symbol_price_stdev[3:] / symbol_price_stdev[:-3].values ) - 1

# print volatility

x_train = pd.concat([volatility, momentum, bb_value[2:]], axis=1)[20:]

y_train = five_day_return[22:]


# We train on the data 2/4/2008 and later,
# since with 20 day averages that is the earliest date for which we have data
# since we have a 3-day volatility change as a metric....thus 23 (index 0:22)
# are not valid training data
# print y_train

'''
STEP 2: INSTANTIATE AND TRAIN OUR MODEL

'''
# Step 1, use KNN with 3 x features (normalized from -1 to 1)
learner = knn.KNNLearner(k=2)


# Step 2, train
learner.addEvidence(x_train.values[:-5],y_train.values)

y_train_df = pd.DataFrame(list(y_train.values), index = y_train.index)
y_train_df.columns = [symbol]

y_test_df = pd.DataFrame(list(learner.query(x_train.values[:-5])), index = y_train.index)
y_test_df.columns = [symbol]

# print y_test_df

y_test_all = pd.DataFrame(list(learner.query(x_test_all.values)), index = x_test_all.index)


# print y_test_all


'''
STEP 3: PLOT TRAINING AND PREDICTED Y VALUES
'''
data = pd.concat([symbol_prices[symbol].ix[22:-5],
    (y_train_df+1)*symbol_prices[symbol].ix[22:-5],
           (y_test_df+1)*symbol_prices[symbol].ix[22:-5]],axis=1)



data.columns = [symbol_str,'Training','Predicted']

# print data

plot_data(data,title="Training vs Predicted Prices")


#### PLOT ENTRY/EXIT POINTS, AND GENERATE ORDER CSV FILE
ax =  symbol_prices.plot(title="KNN Enter & Exit Strategy", fontsize=12)
ax.set_xlabel("Date")
ax.set_ylabel("Price")


'''
IN SAMPLE ENTRY/EXIT STRATEGY AND ORDER GENERATION

'''


with open('orders_in_sample.csv', 'wb') as csvfile:
    orderwriter = csv.writer(csvfile, delimiter=',')
    orderwriter.writerow(['Date','Symbol','Order','Shares'])
    # Long entry ==> If the price was below the lower band and now crosses back, then buy
    # Long exit ==> Price goes from below SMA to above it
    # Short entry--> price goes from above upper band to below it
    # Short exit--> price goes from above SMA to below it

    # 22 days into our data we have enough information to construct volatility stats
    for i in range(22,len(symbol_prices)-5):
       #  print i
        # If predicted return is greater than 2%, hold for 5 days then sells


        if y_test_df.ix[i-22].values > .02:
            ax.vlines(x=symbol_prices.index[i],ymin=-20,ymax=140, color='g')
            orderwriter.writerow([symbol_prices.index[i],symbol_str ,'BUY',100])
            orderwriter.writerow([symbol_prices.index[i+5],symbol_str ,'SELL',100])
            i+=5

        elif (y_test_df.ix[i-22].values <= -.02):
            ax.vlines(x=symbol_prices.index[i],ymin=-20,ymax=140, color='r')
            orderwriter.writerow([symbol_prices.index[i],symbol_str ,'SELL',100])
            orderwriter.writerow([symbol_prices.index[i+5],symbol_str ,'BUY',100])
            i+=5
        else:
            pass

plt.show()



'''
OUT OF SAMPLE ENTRY/EXIT STRATEGY AND ORDER GENERATION

'''


with open('orders_out_of_sample.csv', 'wb') as csvfile:
    orderwriter = csv.writer(csvfile, delimiter=',')
    orderwriter.writerow(['Date','Symbol','Order','Shares'])
    # Long entry ==> If the price was below the lower band and now crosses back, then buy
    # Long exit ==> Price goes from below SMA to above it
    # Short entry--> price goes from above upper band to below it
    # Short exit--> price goes from above SMA to below it

    for i in range(0,len(x_test_all)-5):
       #  print i
        # If predicted return is greater than 2%, hold for 5 days then sells


        if y_test_all.ix[i].values > .02:
            ax.vlines(x=symbol_prices_out_of_sample_only.index[i],ymin=-20,ymax=140, color='g')
            orderwriter.writerow([symbol_prices_out_of_sample_only.index[i],symbol_str ,'BUY',100])
            orderwriter.writerow([symbol_prices_out_of_sample_only.index[i+5],symbol_str ,'SELL',100])
            i+=5

        elif (y_test_all.ix[i].values <= -.02):
            ax.vlines(x=symbol_prices_out_of_sample_only.index[i],ymin=-20,ymax=140, color='r')
            orderwriter.writerow([symbol_prices_out_of_sample_only.index[i],symbol_str ,'SELL',100])
            orderwriter.writerow([symbol_prices_out_of_sample_only.index[i+5],symbol_str ,'BUY',100])
            i+=5
        else:
            pass

