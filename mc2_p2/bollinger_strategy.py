from util import *
import pandas as pd
import numpy as np



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

    symbol_prices_mean = pd.rolling_mean(symbol_prices,20)

    symbol_prices_mean = symbol_prices_mean.ix[20:,:]

    upper_bollinger = 2*symbol_prices_std.ix[20:,:]+symbol_prices_mean.ix[20:,:]
    lower_bollinger = -2*symbol_prices_std.ix[20:,:]+symbol_prices_mean.ix[20:,:]



    ax =  symbol_prices.plot(title="Bollinger Bands", fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    # ax.plot(symbol_prices_mean.ix[20:,:],  label='Google-Bollinger')

    #symbol_prices_mean.plot(label = "Upper Band", ax= ax,color = 'cyan')
    # upper_band.plot(Label= "Lower band", ax=ax,color = 'cyan')


#THis works, edit the code to show all bands
    plt.plot(symbol_prices_mean.index, symbol_prices_mean, "k-", label='mean')
    plt.plot(symbol_prices_mean.index, upper_bollinger, "g-", label='Upper band')
    plt.plot(symbol_prices_mean.index, lower_bollinger, "r-", label='Upper band')


    current_status = "Neutral"


    for i in range(20,len(symbol_prices)):
        if current_status == "Neutral":
            if (symbol_prices['IBM'].ix[i-1] < lower_bollinger['IBM'].ix[i-21]) and \
                    (symbol_prices['IBM'].ix[i] > lower_bollinger['IBM'].ix[i-20]):
                current_status = "Long"
                ax.vlines(x=dates[i],ymin=0,ymax=140, color='g')

            if (symbol_prices['IBM'].ix[i-1] > upper_bollinger['IBM'].ix[i-21]) and \
                    (symbol_prices['IBM'].ix[i] < upper_bollinger['IBM'].ix[i-20]):
                current_status = "Short"
                ax.vlines(x=dates[i],ymin=0,ymax=140, color='r')

        elif current_status == "Long":
            if (symbol_prices['IBM'].ix[i-1] < symbol_prices_mean['IBM'].ix[i-21]) and \
        (symbol_prices['IBM'].ix[i] > symbol_prices_mean['IBM'].ix[i-20]):
                current_status = "Neutral"
                ax.vlines(x=dates[i],ymin=0,ymax=140, color='black')
        else:
            if (symbol_prices['IBM'].ix[i-1] > symbol_prices_mean['IBM'].ix[i-21]) and \
        (symbol_prices['IBM'].ix[i] < symbol_prices_mean['IBM'].ix[i-20]):
                current_status = "Neutral"
                ax.vlines(x=dates[i],ymin=0,ymax=140, color='black')






    # Long entry ==> If the price was below the lower band and now crosses back, then buy

    # Long exit ==> Price goes from below SMA to above it

    # Short entry--> price goes from above upper band to below it


    # Short exit--> price goes from above SMA to below it


    plt.show()
    print "hii!" , symbol_prices_mean

    #plt.(symbol_prices_mean)



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

