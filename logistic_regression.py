import pandas as pd
import statsmodels.api as sm
import math

loansData = pd.read_csv('loansData_clean.csv')

def colAdder(data):

    def percCheck(dataCol, amt):
        def perCheckMapFunc(val):
            return 1 if val >= amt else 0

        percArr = map(perCheckMapFunc, dataCol)
        return percArr


    data['IR_TF'] = percCheck(data['Interest.Rate'], (12.0/100))

    data['Const'] = [1 for x in data['IR_TF']]

    return data

loansData = colAdder(loansData)

ind_vars = [
    'FICO.Score',
    'Amount.Requested',
    'Const'
]

print loansData

logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])

result = logit.fit()

coeff = result.params
print coeff

def logistic_function(coeff, ficoScore, loanAmt, inv):
    coeffConst = coeff['Const'] if not inv else coeff['Const'] * -1
    coeffFico = coeff['FICO.Score'] if not inv else coeff['FICO.Score'] * -1
    coeffLoan = coeff['Amount.Requested'] if not inv else coeff['Amount.Requested'] * -1

    return 1 / (1 + math.exp(coeffConst + coeffFico * ficoScore + coeffLoan * loanAmt))

p1 = logistic_function(coeff, 720, 10000, True)
p2 = logistic_function(coeff, 720, 10000, False)
p3 = logistic_function(coeff, 780, 10000, False)

print p1, p2, p3