# load.py
import os

#Save cleaned datafrane to csv
def save_to_csv(df, filename ='clean_movies.csv', folder = 'output'):
  os.makedirs(folder, exist_ok = True)
  filepath = os.path.join(folder, filename)
  df.to_csv(filepath, index = False)
  print(f"Saved file: {filepath}")
