import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import database

def create_perc(data):
    perc = {'0-10':0,'10-20':0,'20-30':0,'30-40':0,'40-50':0,'50-60':0,'60-70':0,'70-80':0,'80-90':0,'90-100':0}
    score = data['overall_score']

    for i in score:
        if ((i >= np.percentile(score,0))&(i < np.percentile(score,10))):
            perc['0-10'] += 1
        elif ((i >= np.percentile(score,10))&(i < np.percentile(score,20))):
            perc['10-20'] += 1
        elif ((i >= np.percentile(score,20))&(i < np.percentile(score,30))):
            perc['20-30'] += 1
        elif ((i >= np.percentile(score,30))&(i < np.percentile(score,40))):
            perc['30-40'] += 1
        elif ((i >= np.percentile(score,40))&(i < np.percentile(score,50))):
            perc['40-50'] += 1
        elif ((i >= np.percentile(score,50))&(i < np.percentile(score,60))):
            perc['50-60'] += 1
        elif ((i >= np.percentile(score,60))&(i < np.percentile(score,70))):
            perc['60-70'] += 1
        elif ((i >= np.percentile(score,70))&(i < np.percentile(score,80))):
            perc['70-80'] += 1
        elif ((i >= np.percentile(score,80))&(i < np.percentile(score,90))):
            perc['80-90'] += 1
        elif ((i >= np.percentile(score,90))&(i < np.percentile(score,100))):
            perc['90-100'] += 1

    data_perc = pd.DataFrame.from_dict(perc,orient='index',columns=['count'])
    return data_perc

def create_doj(data):
    doj = {'this_week':0,'next_week':0,'this_month':0,'next_month':0}
    dates = data['Date_Of_Joining']

    for d in dates:
        # d_obj = datetime.datetime.strptime(d,'%Y-%m-%d %H:%M:%S.%f').date()
        d_obj = d
        today = datetime.datetime.now().date()
        diff = (d_obj - today).days

        if ((diff>=0) & (diff<7)):
            doj['this_week'] += 1
        elif ((diff>=7) & (diff<14)):
            doj['next_week'] += 1
        elif ((today.month == d_obj.month) & (diff>=14)):
            doj['this_month'] += 1
        elif ((today.month != d_obj.month) & (diff>=14)):
            doj['next_month'] += 1

    data_doj = pd.DataFrame.from_dict(doj,orient='index',columns=['num_days'])

    return data_doj

def create_yoe (df):
    df = df.sort_values("Year_of_Experience",ascending=True)
    df = df.groupby(["Year_of_Experience"]).mean()
    df = df.reset_index()
    
    return df

def create_ski (df):
    # [print(x) for x in df['Skill'].values]
    df['Skill'] = [x.split(", ") for x in df['Skill'].values]
    from sklearn.preprocessing import MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    mlb.fit_transform(df['Skill'])
    mlb.classes_
    ski = pd.DataFrame(mlb.fit_transform(df['Skill']), columns=list(mlb.classes_))
    num_skills = []
    # [print(ski[col].value_counts()[1]) for col in ski.columns]
    for col in list(ski.columns):
        # print(ski[col].value_counts().values)
        num_skills.append(ski[col].value_counts()[1])

    return num_skills, list(ski.columns)