import pickle
import pandas as pd
import ast
import json
import numpy as np
from inspire_reduce import cleanname

centrality = pickle.load(open('../../inspirecentrality2'))

author_info = {}

for line in file('../../inspirereduce2'):
  parts = line.split('\t')
  author = ast.literal_eval(parts[0])
  links = json.loads(parts[1])
  a_pub = sum(links.values())
  a_col = len(links.values())
  a_cen = centrality[author]
  author_info[author] = [a_pub, a_col, a_cen]

def inspire_measures(row):
  author_str = row['Author']
  author_list = ast.literal_eval(author_str)
  author_list = [cleanname(a) for a in author_list]
  pubs = []
  cols = []
  cens = []

  missing = False

  for a in author_list:
    if a in author_info.keys():
      info = author_info[a]
      pubs.append(info[0])
      cols.append(info[1])
      cens.append(info[2])
    else:
      missing = True
    # else abandon?
  if pubs and not missing:
    return pd.Series({'Min_Pubs': min(pubs), 'Avg_Pubs': np.mean(pubs), 'Max_Pubs': max(pubs), 'Min_Cols': min(cols), 'Avg_Cols': np.mean(cols), 'Max_Cols': max(cols), 'Min_Cens': min(cens), 'Avg_Cens': np.mean(cens), 'Max_Cens': max(cens)})
  else:
    nanfloat = float('nan')
    return pd.Series({'Min_Pubs': nanfloat, 'Avg_Pubs': nanfloat, 'Max_Pubs': nanfloat, 'Min_Cols': nanfloat, 'Avg_Cols': nanfloat, 'Max_Cols': nanfloat, 'Min_Cens': nanfloat, 'Avg_Cens': nanfloat, 'Max_Cens': nanfloat})


arxiv = pd.read_csv('../ADS_joined_data.csv')

arxiv_merge = arxiv.merge(arxiv.apply(inspire_measures, axis=1), left_index=True, right_index=True)

arxiv_merge.to_csv('../INSPIRE_merged_data.csv', index=False)
