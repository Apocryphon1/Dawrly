import pandas as pd
import re
import string
import time

import nltk
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer

from river.naive_bayes import MultinomialNB
from river.feature_extraction import BagOfWords
from river.compose import Pipeline 
from river.metrics import ClassificationReport, Accuracy

nltk.download('stopwords')

encoding = "ISO-8859-1"
colNames = ["target", "ids", "date", "flag", "user", "text"]
df = pd.read_csv('./data/DataSet/tweets.csv', encoding=encoding ,names = colNames)

#print(df.head())
#print(df.count())

df = df.drop_duplicates('text')
#print(df.shape)

def processText(Text): 
    # Remove HTML special entities (e.g. @amp;)
    Text =re.sub(r'\&\w*;',' ', str(Text)) 
    #Convert @username to AT USER 
    Text = re.sub('@[^\s]+',' ',Text) 
    # Remove tickers 
    Text = re.sub(r'\$\w*', ' ', Text)
    # To Lowercase 
    Text = Text.lower() 
    # Remove hyperLinks 
    Text =re.sub(r'https?:\/\/.*\/\w*', ' ', Text) 
    # Remove hashtags 
    Text =re.sub(r'#\w*', ' ', Text) 
    # Remove Punctuation and split 's, 't,'ye with a space for filter 
    Text = re.sub(r'[' + string.punctuation.replace('@', ' ') + ']+', ' ', Text) 
    # Remove words with 2 or fewer Letters 
    Text = re.sub(r'\b\w{1,2}\b', ' ', Text) 
    # Remove whitespace (including new Line characters)
    Text =re.sub(r'\s\s+', ' ', Text) 
    # Remove single space remaining at the front of the Text. 
    Text = Text.lstrip(' ') 
    # Remove characters beyond Basic Multilingual Plane (BMP) of Unicode, 
    Text = ''.join(c for c in Text if c <= '\uffff') 
    return Text 

df['text'] = df['text'].apply(processText) 
#print(df.head())

stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")

def preprocess(text, stem=False):
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)

df['text']= df['text'].apply(lambda x: preprocess(x)) 

#decode_map = {0: "NEGATIVE", 2: "NEUTRAL", 4: "POSITIVE"}
decode_map = {0: -1, 2: 0, 4: 1}
def decode_sentiment(label):
    return decode_map[int(label)]

df.target = df.target.apply(lambda x: decode_sentiment(x))
#print(df.head())


model = Pipeline(('vectorizer',BagOfWords(lowercase=True)),('nb',MultinomialNB))

for index, row in df.iterrows():
    model = model.learn_one(row['text'],row['target'])
    
model.predict_one("i am happy")

test_predict = []
for index, row in df.iterrows():
    result= model.predict_one(row['text']) 
    test_predict.append(result)
    
df['predict'] = test_predict

report = ClassificationReport()

for index, row in df.iterrows():
    report = report.update(row['target'],row['predict'])
    
print("Classification Report for the model",report)

''' metric_accuracy = Accuracy()

for index, row in df.iterrows():
    test_predict_before = model.predict_one(row.text) 
    metric_accuracy = metric_accuracy.update(row.target,test_predict_before)
    model= model.learn_one(row.text,row.target)
    
metric_accuracy '''

NEUTRAL= "NEUTRAL"
NEGATIVE = "NEGATIVE"
POSITIVE = "POSITIVE"
SENTIMENT_THRESHOLDS = (0.4, 0.7)

def decode_sentiment(score, include_neutral=True):
    if include_neutral:        
        label = NEUTRAL
        if score <= SENTIMENT_THRESHOLDS[0]:
            label = NEGATIVE
        elif score >= SENTIMENT_THRESHOLDS[1]:
            label = POSITIVE

        return label
    else:
        return NEGATIVE if score < 0.5 else POSITIVE

def predict(text, include_neutral=True):
    start_at = time.time()
    # Predict
    score = model.predict_proba_one(text)['POSITIVE']
    # Decode sentiment
    label = decode_sentiment(score, include_neutral=include_neutral)

    return {"label": label, "score": float(score),
        "elapsed_time": time.time()-start_at}  
    
def apply_sentiment(rate):
    if rate >= 3:
        return 1
    elif rate < 3:
        return -1
    


def checkSentiment(reviews):
    global model
    predectionList = []
    for review in reviews:
        predection = model.predict_one(review.body)
        predectionList.append(predection)
    
    return predectionList


review_df = pd.read_excel("./data/reviewsData.xlsx")
review_df.rating = review_df.rating.apply(lambda x: apply_sentiment(x))
for index, row in review_df.iterrows():
    predection = model.predict_one(row.body) 
    report2 = report2.update(row.rating,predection)
    
print("Classification Report for the model according to the reviews",report2)

