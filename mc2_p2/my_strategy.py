from util import *
import pandas as pd
import numpy as np
import csv

def get_portfolio_value(prices, allocs, start_val=1):
    """Compute daily portfolio value given stock prices, allocations and starting value.

    Parameters
    ----------
        prices: daily prices for each stock in portfolio
        allocs: initial allocations, as fractions that sum to 1
        start_val: total starting value invested in portfolio (default: 1)
    Returns
    -------
        port_val: daily portfolio value
    """

    normed = prices / prices.ix[0]
    alloced = normed * allocs
    pos_vals = alloced * start_val
    port_val = pos_vals.sum(axis=1)

    # print port_val
    return port_val


def plot_bollinger_data(symbol, start_date,end_date):
    """Normalize given stock prices and plot for comparison.

    Parameters
    ----------
        df: DataFrame containing stock prices to plot (non-normalized)
        title: plot title
        xlabel: X-axis label
        ylabel: Y-axis label
    """

    dates = pd.date_range(start_date, end_date)

    symbol_prices = get_data(symbol,dates)

    symbol_prices = symbol_prices.drop('SPY', 1)

    #TODO append std and mean to dataframe

    symbol_prices_std = pd.rolling_std(symbol_prices,20)

    symbol_prices_mean_30 = pd.rolling_mean(symbol_prices,30)
    symbol_prices_mean_10 = pd.rolling_mean(symbol_prices,10)


    symbol_prices_mean_30 = symbol_prices_mean_30.ix[29:,:]
    symbol_prices_mean_10 = symbol_prices_mean_10.ix[10:,:]



    ax =  symbol_prices.plot(title="SMA Crossover", fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    # ax.plot(symbol_prices_mean.ix[20:,:],  label='Google-Bollinger')

    #symbol_prices_mean.plot(label = "Upper Band", ax= ax,color = 'cyan')
    # upper_band.plot(Label= "Lower band", ax=ax,color = 'cyan')


#THis works, edit the code to show all bands
    plt.plot(symbol_prices_mean_30.index, symbol_prices_mean_30, "k-", label='SMA 30')
    plt.plot(symbol_prices_mean_10.index, symbol_prices_mean_10, "g-", label='SMA 10')
    plt.legend(loc=2)


    current_status = "Neutral"
    print "LOOK ", symbol_prices_mean_30.ix[0]
    print "LOOK ", symbol_prices_mean_10.ix[19]
    print "LOOK ", symbol_prices.ix[29]


    with open('orders.csv', 'wb') as csvfile:
        orderwriter = csv.writer(csvfile, delimiter=',')
        orderwriter.writerow(['Date','Symbol','Order','Shares'])
        # Long entry ==> If the price was below the lower band and now crosses back, then buy
        # Long exit ==> Price goes from below SMA to above it
        # Short entry--> price goes from above upper band to below it
        # Short exit--> price goes from above SMA to below it


        for i in range(20,len(symbol_prices_mean_30)):
            print i
            # print len(symbol_prices_mean_30)
            # print len(symbol_prices_mean_10)
            if current_status == "Neutral":
                if (symbol_prices_mean_10['IBM'].ix[i-1] < symbol_prices_mean_30['IBM'].ix[i-20]) and \
                        (symbol_prices_mean_10['IBM'].ix[i] > symbol_prices_mean_30['IBM'].ix[i-19]) and \
                        (symbol_prices['IBM'].ix[i+9] > max(symbol_prices_mean_30['IBM'].ix[i-19],
                symbol_prices_mean_10['IBM'].ix[i])):
                    current_status = "Long"
                    ax.vlines(x=symbol_prices_mean_10.index[i],ymin=-20,ymax=140, color='g')
                    orderwriter.writerow([symbol_prices_mean_10.index[i],'IBM','BUY',100])

                if (symbol_prices_mean_10['IBM'].ix[i-1] >  symbol_prices_mean_30['IBM'].ix[i-20]) and \
                        (symbol_prices_mean_10['IBM'].ix[i] < symbol_prices_mean_30['IBM'].ix[i-19]) and \
                        symbol_prices['IBM'].ix[i+9] < min(symbol_prices_mean_30['IBM'].ix[i-19],
                                                           symbol_prices_mean_10['IBM'].ix[i-19]):
                    current_status = "Short"
                    # print " IBM at %r, and bollinger at %r " \
                    #       %(symbol_prices['IBM'].ix[i],upper_bollinger['IBM'].ix[i-19] )
                    ax.vlines(x=symbol_prices_mean_10.index[i],ymin=-20,ymax=140, color='r')
                    orderwriter.writerow([symbol_prices_mean_10.index[i],'IBM','SELL',100])

            elif current_status == "Long":
                if (symbol_prices_mean_10['IBM'].ix[i-1] >  symbol_prices_mean_30['IBM'].ix[i-20]) and \
                        (symbol_prices_mean_10['IBM'].ix[i] < symbol_prices_mean_30['IBM'].ix[i-19]) and \
                        symbol_prices['IBM'].ix[i+9] < min(symbol_prices_mean_30['IBM'].ix[i-19],
                                                           symbol_prices_mean_10['IBM'].ix[i-19]):
                    current_status = "Short"
                    ax.vlines(x=symbol_prices_mean_10.index[i],ymin=-20,ymax=140, color='r')
                    orderwriter.writerow([symbol_prices_mean_10.index[i],'IBM','SELL',200])
            # Short
            elif current_status == "Short":
                if (symbol_prices_mean_10['IBM'].ix[i-1] < symbol_prices_mean_30['IBM'].ix[i-20]) and \
                        (symbol_prices_mean_10['IBM'].ix[i] > symbol_prices_mean_30['IBM'].ix[i-19])  and \
                        (symbol_prices['IBM'].ix[i+9] > max(symbol_prices_mean_30['IBM'].ix[i-19],
                symbol_prices_mean_10['IBM'].ix[i])):
                    current_status = "Long"
                    ax.vlines(x=symbol_prices_mean_10.index[i],ymin=-20,ymax=140, color='g')
                    orderwriter.writerow([symbol_prices_mean_10.index[i],'IBM','BUY',200])

    plt.show()

def test_run():
    """Driver function."""
    # Define input parameters
    start_date = '2007-12-31'
    end_date = '2009-12-31'

    plot_bollinger_data(['IBM'],start_date,end_date)




    # Get daily portfolio value
    #port_val = get_portfolio_value(prices, allocs, start_val)
    #plot_data(port_val, title="Daily Portfolio Value")

    # Get portfolio statistics (note: std_daily_ret = volatility)
    # cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)





if __name__ == "__main__":
    test_run()

