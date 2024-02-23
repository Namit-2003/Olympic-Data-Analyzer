import pandas as pd

def preprocess(df,reg_df):

    df = df[df['Season'] == 'Summer']

    df = df.merge(reg_df,on='NOC',how='left')

    df.drop_duplicates(inplace=True)

    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)

    return df