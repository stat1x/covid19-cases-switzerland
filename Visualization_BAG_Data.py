import pandas as pd
import numpy
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def exponential_func(x, a, b, c):
    return a*numpy.exp(-b*x)+c


def scatterplot(datesincezero, poscasearray):
    plt.scatter(datesincezero, poscasearray)
    plt.xlabel("# of days since 06. March 2020")
    plt.ylabel('# of positive tests (BAG)')


data = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_cases_switzerland.csv", sep=';')
canton = input('Which canton do you want to check?')
data = data.filter(items=['Date', canton])  # only keep data for one canton (or whole CH) in dataframe
data.rename(columns={canton: "TotalPosTests1"}, inplace=True)
switzerland_data = data
newdata = switzerland_data
startrow = 0
for x in switzerland_data['TotalPosTests1']:
    if x == 0:
        startrow+=1
newdata = newdata.iloc[startrow:]
inhabitantsCH = 8570000
datearray = newdata['Date'].to_numpy()
for x in datearray:
    x = datetime.strptime(x, '%Y-%m-%d')
datetimearray = [datetime.strptime(x, '%Y-%m-%d').date() for x in datearray]
firstdate = datetimearray[1]
datesincezero = [(x - firstdate).days + 1 for x in datetimearray]
poscasearray = newdata['TotalPosTests1'].to_numpy().tolist()
scatterplot(datesincezero, poscasearray)
x = datesincezero
y = poscasearray
try:
    popt, pcov = curve_fit(exponential_func, x, y, p0=(1, -1e-6, 1))
    xx = numpy.linspace(1, len(newdata.index), 1000)
    yy = exponential_func(xx, *popt)
    plt.plot(xx, yy, 'g--', label='{}-curve-fit: a=%5.3f, b=%5.3f, c=%5.3f'.format(canton) % tuple(popt))
except RuntimeError:  # if no exponential fit can be found, do not try to plot it and pass
    pass
plt.legend()
plt.xticks(x, datetimearray, rotation='vertical')
plt.tight_layout()  # larger bottom margin for readability of dates
plt.show()
plt.close()


while True:
    try:
        futuredays = input('How many days in the future?')
        postestedindividuals = int(round(exponential_func(int(futuredays)+datesincezero[-1], *popt)))
    except ValueError:  # if the user input is not an integer number
        continue
    if postestedindividuals > inhabitantsCH:
        print('Number is higher than all CH inhabitants:')
        print(str(postestedindividuals) + ' COVID19 tested individuals in {} \n'.format(canton))
    else:
        print(str(postestedindividuals)+' COVID19 tested individuals in {} \n'.format(canton))
