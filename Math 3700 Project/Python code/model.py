########
## Name: Patrick Dunleavy and Aleks Hremonic
## 

import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('2012-13_PLAYERDATA_GAMELOGS.csv')

df.sort_values(by=['Player_ID', 'GAME_DATE'], inplace=True)

df['Accumulated_Minutes'] = df.groupby('Player_ID')['MIN'].cumsum().shift(1)

df['Game_Date'] = pd.to_datetime(df['GAME_DATE'])
df['Days_of_Rest'] = df.groupby('Player_ID')['Game_Date'].diff().dt.days.shift(1)

season_averages = df.groupby('Player_ID')[['REB', 'FGA']].mean().rename(columns={'REB': 'Avg_REB', 'FGA': 'Avg_FGA'})
df = df.merge(season_averages, on='Player_ID')

df['Mean_Centered_REBs'] = df['REB'] - df['Avg_REB']
df['Mean_Centered_FGAs'] = df['FGA'] - df['Avg_FGA']


df['Cumulative_REBs'] = df.groupby('Player_ID')['Mean_Centered_REBs'].cumsum().shift(1)
df['Cumulative_FGAs'] = df.groupby('Player_ID')['Mean_Centered_FGAs'].cumsum().shift(1)
df['Accumulated_Minutes_5_Games'] = df['MIN'].rolling(window=5, min_periods=1).sum()


df.to_excel('first_output.xlsx_new.xlsx')

df = pd.read_excel('first_output.xlsx')
