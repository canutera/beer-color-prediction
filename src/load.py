import pandas as pd
from re import sub
def column_name_to_snake_case(s):
    # change chars for undescore
    s = sub(r"[\/( \- ) ]", '_', s)
    # make undescores unique
    s = sub(r"(___)|(__)", '_', s).lower()
    return s if s[-1] != '_' else s[:-1]

def shift(x)-> int:
    if x >= 7 and x <15: return 1
    if x >= 15 and x <23: return 2
    else: return 3


def get_raw_data():
    df = pd.read_csv(r'..\data\raw\Heineken - Data Science Use Case.csv', parse_dates=['Date/Time'])
    df = (df.drop(columns=df.columns[0]) # drop csv index
            .rename(columns={col:column_name_to_snake_case(col) for col in df.columns[1:]})        
        )
    return df

def dropped_columns_features()-> pd.DataFrame:
    '''load dropped column features
    - last_was_hnk:

        flag indicating whether last product batch was heineken or not

    - shift:
        
        int indicator considering hour of the day. the day was split in 3 shifts. check shift function in load.py file

    - other features (dat, day_of_week, hour):

        extracted from date_time columns

    
    '''
    raw = get_raw_data()
    a = raw[['job_id','date_time', 'product']].sort_values('job_id')
    a = (a.assign(last_was_hnk=a['product'].shift().apply(lambda x: 1 if x == "HNK" else 0))
          .assign(day_of_week = a['date_time'].dt.day_of_week)  
          .assign(day = a['date_time'].dt.day)  
          .assign(hour = a['date_time'].dt.hour)  
          .assign(shift = a['date_time'].dt.hour.apply(lambda x: shift(x)))  
        )
    return a.drop(['date_time', 'product'], axis=1)