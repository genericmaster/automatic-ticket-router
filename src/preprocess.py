import pandas as pd
import numpy as np
import re
import logging
from src.utils.dataset_loader import uncleaned


#removing uneccesary features
uncleaned= uncleaned[['Email Address','Email Content','Category']]

# dealing with null values
def Nullvalues(df:pd.DataFrame):
     for column in df.columns:
          if df[column].isnull().sum()==0:
               continue
          else:
               
               df= df[df.column.dropna()]
     return df

Nullvalues(uncleaned)

#dealing with duplicates
def duplicates(df:pd.DataFrame):
     dupe_count = df.duplicated().sum()
     dupe_ratio = dupe_count / len(df)
     if (dupe_count==0):
          pass
     elif dupe_ratio<=0.05:
          df = df.drop_duplicates().reset_index(drop=True)   
     elif dupe_ratio>0.05:
          logging.critical("too many duplicates")
     return df


