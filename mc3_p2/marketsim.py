"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import os

pd.options.mode.chained_assignment = None  # default='warn'


from util import get_data, plot_data
from analysis import get_portfolio_stats, plot_normalized_data, get_portfolio_value

def compute_portvals(start_date, end_date, orders_file, start_val):
    """Compute daily portfolio value given a sequence of orders in a CSV file.

    Parameters
    ----------
        start_date: first date to track
        end_date: last date to track
        orders_file: CSV file to read orders from
        start_val: total starting cash available

    Returns
    -------
        portvals: portfolio value for each trading day from start_date to end_date (inclusive)
    """
    # TODO: Your code here
    # Step 1: read csv file into pandas dataframe
    orders  = pd.read_csv(orders_file,delimiter=',', encoding="utf-8-sig")

    # print "ORDERS ",orders.ix[0,'Order']

    # Get symbols needed
    distinct_symbols = orders['Symbol'].unique()
    distinct_symbols = np.append(distinct_symbols,'SPY')

    # print "look " , distinct_symbols



    # Step 2: read adjusted close prices into a dataframe
    # IBM | GOOG | AAPL | cash (all filled with 1.0
    #Dt price | price | price |1.0

    prices = get_data(symbols=distinct_symbols,
                      dates=pd.date_range(start=start_date,end=end_date))




    prices['cash'] = 1.0

    # print "Prices!! ", prices

    #this represents changes in our holdings
    trades = pd.DataFrame(0, index = prices.index.values, columns = distinct_symbols)

    trades['cash'] = 0.0

    #print "trades!! ", trades

    # Step 3: loop through orders file
    for i in orders.index:
         #date and symbol in the trades file
        if orders.ix[i,'Order'] == 'BUY':
            trades.ix[orders.ix[i][0],orders.ix[i]['Symbol']] += orders.ix[i]['Shares']
            trades.ix[orders.ix[i][0],['cash']] += prices.ix[orders.ix[i][0],orders.ix[i]['Symbol']] * \
                                                  orders.ix[i]['Shares']

        else:
            trades.ix[orders.ix[i][0],orders.ix[i]['Symbol']] += -1*orders.ix[i]['Shares']
            trades.ix[orders.ix[i][0],['cash']]  +=  -1*prices.ix[orders.ix[i][0],orders.ix[i]['Symbol']] * \
                                                   orders.ix[i]['Shares']

    # Step 4: holdings dataframe
    #fill in first row with 0s and starting cash (which is 1mm)
    holdings = pd.DataFrame(0, index = prices.index.values, columns = distinct_symbols)
    holdings['cash'] = 0.0
    holdings['cash'][0] = start_val
    # print "holdings" , holdings
    for i in range(0,len(holdings.index)):

        if i == 0:
            for symbol in distinct_symbols:
                holdings.ix[i,symbol] = holdings.ix[i,symbol] + trades.ix[i,symbol]

            holdings.ix[i,'cash'] = holdings.ix[i,'cash'] + -1*trades.ix[i,'cash']

        else:
            for symbol in distinct_symbols:
                # print "symbol is " , symbol
                # print "prev holdings", holdings.ix[i,symbol]
                # print "current trade" , trades.ix[i,symbol]
                holdings.ix[i,symbol] = holdings.ix[i-1,symbol] + trades.ix[i,symbol]

            holdings.ix[i,'cash'] = holdings.ix[i-1,'cash'] + -1*trades.ix[i,'cash']

    # print "HOLDINGS YO: ", holdings

    # Step 5: df value, which is holdings * prices

    vals = pd.DataFrame(holdings.values*prices.values, columns=holdings.columns, index=holdings.index)

    # print "vals!! ", vals

    port_vals = vals.sum(axis=1)

    # populate trades with num of shares | price
    #print "updated trades!! ", trades

    # normed = prices / prices.ix[0]
    # alloced = normed * allocs
    # pos_vals = alloced * start_val
    # port_val = pos_vals.sum(axis=1)

    # print "portfolio vals" , port_vals
    return port_vals
    # return portvals


def test_run(order_file,start_date,end_date):
    """Driver function."""
    # Define input parameters
    start_date = start_date
    end_date = end_date
    # orders_file = os.path.join("orders", "orders.csv")
    orders_file = order_file
    start_val = 10000

    # Process orders
    portvals = compute_portvals(start_date, end_date, orders_file, start_val)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # if a DataFrame is returned select the first column to get a Series
    
    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals)

    # Simulate a $SPX-only reference portfolio to get stats
    prices_SPX = get_data(['$SPX'], pd.date_range(start_date, end_date))
    prices_SPX = prices_SPX[['$SPX']]  # remove SPY
    portvals_SPX = get_portfolio_value(prices_SPX, [1.0])
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = get_portfolio_stats(portvals_SPX)

    # Compare portfolio against $SPX
    print "Data Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX: {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX: {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX: {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX: {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

    # Plot computed daily portfolio value
    df_temp = pd.concat([portvals, prices_SPX['$SPX']], keys=['Portfolio', '$SPX'], axis=1)
    plot_normalized_data(df_temp, title="Daily portfolio value and $SPX")


if __name__ == "__main__":
    test_run('orders_in_sample.csv','2008-01-01','2009-12-31')
    test_run('orders_out_of_sample.csv','2010-01-01','2010-12-31')
