########
## Name: Patrick Dunleavy and Aleks Hremonic
## 

import pandas as pd

df = pd.read_excel('player_injury_data_2012-13.xlsx')
df['Accumulated_Minutes_5_Games'] = df['MIN'].rolling(window=5, min_periods=1).sum()

df.to_excel('new_player_injury_data.xlsx')