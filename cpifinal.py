# -*- coding: utf-8 -*-
"""CPIFinal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KnH25QuDE64j0PTBRkBfqrID8m-_VNS1
"""

### Program to compare an asset's performance to inflation.
import pandas as pd

# Function that takes raw prices and turns them into percentages to measure performance.
def get_change(asset):
  change = []
  for row in asset.index:
    if row == 0:
      continue
    print(asset["Close"][row], asset["Close"][row-1])
    change.append(str(((asset["Close"][row] - asset["Close"][row-1]) / asset["Close"][row-1])*100) + "%")
  dataframe = pd.concat([asset, pd.DataFrame(change)], axis=1)
  dataframe = dataframe.drop(index=[len(dataframe.index)-1])
  dataframe.reset_index(inplace=True)
  dataframe = dataframe.set_axis(['index', "Date", "Close", "Change"], axis=1, inplace=False)
  return dataframe


# Function that uses asset performace and inflation to determine how the asset performes during low, moderate, and high inflation.
def compare_to_cpi(cpi, asset):
  cpi = cpi.drop(index=[num for num in range((len(cpi.index)-len(asset.index)))])
  cpi.reset_index(inplace=True)

  data = pd.concat([cpi, asset], axis=1)

  low_inflation = []
  moderate_inflation = []
  high_inflation = []

  for row in range(len(data.index)):
      if float(data["Inflation"][row][:-1]) > 5.9:
          high_inflation.append(float(data["Change"][row][0:-1])-float(data["Inflation"][row][:-1]))
      elif float(data["Inflation"][row][:-1]) > 2.9:
          moderate_inflation.append(float(data["Change"][row][0:-1])-float(data["Inflation"][row][:-1]))
      else:
          low_inflation.append(float(data["Change"][row][0:-1])-float(data["Inflation"][row][:-1]))
  print('Low Inflation', sum(low_inflation)/len(low_inflation), len([num for num in low_inflation if num < 0]) / len(low_inflation))
  print('Medium Inflation', sum(moderate_inflation)/len(moderate_inflation), len([num for num in moderate_inflation if num < 0]) / len(moderate_inflation))
  print('High Inflation', sum(high_inflation)/len(high_inflation), len([num for num in high_inflation if num < 0]) / len(high_inflation))


# Results 
if __name__ == __main__:

  # Loading Consumer Price Index (CPI) data into a pandas dataframe.
  df = pd.read_csv('CPI.csv')
  df = df.drop(index=0)
  df.reset_index(inplace=True)

  # Loading asset data into a dataframe
  df2 = pd.read_csv('SP500.csv')

  # get results
  compare_to_cpi(df, df2)