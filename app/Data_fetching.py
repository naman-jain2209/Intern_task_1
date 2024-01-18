# import libraries
import requests
import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sqlalchemy import create_engine
import json
import os
from dotenv import load_dotenv
load_dotenv()
key=os.getenv('News_API_Key')
passwd=os.getenv('DB_Password')
db_name=os.getenv('db_name')
nltk.download('all')
analyzer=SentimentIntensityAnalyzer()


def Sen_Analyze(text):
    Sen_tag=""
    Score=analyzer.polarity_scores(text)['compound']
    if(Score<-0.2):
        Sen_tag="Negative"
    elif (Score>=-0.2 and Score<=0.2):
        Sen_tag="Neutral"
    else:
        Sen_tag="Positive"
    return Sen_tag

def data_fetch(topic, start_date, end_date):
    # Getting Data from NewsAPI
    url="https://newsapi.org/v2/everything?q="+topic+"&from="+start_date+"&to="+end_date+"&sortBy=popularity&language=en&apiKey="+key
    r=requests.get(url)
    df=write_file(r.content)
    # data_frame()
    Data_to_be_sent=more_processing(df)
    connection_string = "mysql+mysqlconnector://root:"+passwd+"@"+db_name+":3306/intern_task"
    engine = create_engine(connection_string)
    Data_to_be_sent.to_sql(name='News', con=engine, if_exists='replace')
    print('done')

# Write bytes to file
def write_file(r):
    # Convert bytes to string
    str_data = r.decode('utf-8')
    # Parse string to JSON
    json_data = json.loads(str_data)
    # print(json_data)
    df = pd.json_normalize(json_data['articles'])
    return df

def preprocess(text):
    # tokenisation
    text=str(text)
    tokens=word_tokenize(text)
    
    #StopWords
    WithoutSW=[x for x in tokens if x not in stopwords.words('english')]

    #lemmatization
    lemetizer=WordNetLemmatizer()
    lemetized_list=[lemetizer.lemmatize(x) for x in WithoutSW]

    # Now that we have our Lemetized List, Join them to form the processed text which would then be analyzed
    processed_text = ' '.join(lemetized_list)

    return processed_text

def more_processing(df):
    df['analyze_component']=df['title']+((df['description'][:200] + '..') if len(df['description']) > 200 else df['description'])
    df['processed_text']=df['analyze_component'].apply(preprocess)
    df = df.drop(df[df['content']=='[Removed]'].index)
    df['Sentiment']=df['processed_text'].apply(Sen_Analyze)
    df['publishedAt'].fillna('2024-01-01')
    dates=[]
    for x in df['publishedAt']:
        dates.append(x[0:10])
    df['Dates']=dates
    #Data_to_be_sent 
    Data_to_be_sent=df[['author','url','title','description','Sentiment','Dates']]
    return Data_to_be_sent


# data_fetch('GazaStrip', '2024-01-01', '2024-01-15')



