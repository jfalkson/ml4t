__author__ = 'jfalkson'

import KNNLearner as knn

from util import *

# Config
start_date = '2007-12-31'
end_date = '2009-12-31'
symbol = 'IBM'

# Step 1, use KNN with 3 x features (normalized from -1 to 1)

learner = knn.KNNLearner(k=3)

# define train x and train y
# learner.addEvidence(trainX, trainY)

dates = pd.date_range(start_date, end_date)
symbol_prices = get_data(symbol,dates)

symbol_prices[symbol].ix[i+9]

# predY = learner.query(trainX)



# User future 5 day return as Y value

# Step 2, train on IBM

