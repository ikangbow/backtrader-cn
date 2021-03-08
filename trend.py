import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.rand(100, 5), pd.date_range('2012-01-01', periods=100))

print(df)
def trend(df):
    df = df.copy().sort_index()
    dates = df.index.to_julian_date().values[:, None]
    x = np.concatenate([np.ones_like(dates), dates], axis=1)
    y = df.values
    return pd.DataFrame(np.linalg.pinv(x.T.dot(x)).dot(x.T).dot(y).T,
                        df.columns, ['Constant', 'Trend'])

df_sample = df
coef = trend(df_sample)
df_sample['trend'] = (coef.iloc[0, 1] * df_sample.index.to_julian_date() + coef.iloc[0, 0])
print(coef)