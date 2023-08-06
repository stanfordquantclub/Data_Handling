# measures the maximum profit that can be made given the sequential nature of pricing
# this is the maximum upwards unidirectional change in price 
def maxProfit(prices):
        maxprofit = 0
        low_price = prices[0]

        for ind in range(1, len(prices)):
            if prices[ind] < low_price:
                low_price = prices[ind]
                
            if prices[ind] - low_price > maxprofit:
                maxprofit = prices[ind] - low_price
        
        return maxprofit
# measures the maximum profit that can be made given the sequential nature of pricing
# this is the maximum downwards unidirectional change in price
def maxLoss(prices):
     maxloss = 0
     high_price = prices[0]
     
     for ind in range(1, len(prices)):
            if prices[ind] > high_price:
               high_price = prices[ind]

            if high_price - prices[ind] > maxloss:
                maxloss = high_price - prices[ind]
            
     return maxloss

# finds the maximum upwards unidirectional change over a given window
def maxProfit_list(prices, window):
     fin_list = [maxProfit(prices[x:x+window]) for x in range(len(prices) - window)]
     zeros = [0 for x in range(window)]
     fin_list = fin_list + zeros
     return fin_list

# finds the maximum downwards unidirectional change over a given window
def maxLoss_list(prices, window):
     fin_list = [maxLoss(prices[x:x+window]) for x in range(len(prices) - window)]
     zeros = [0 for x in range(window)]
     fin_list = fin_list + zeros
     return fin_list

