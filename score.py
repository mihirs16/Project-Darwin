# ----- importing configuration ------------------------------------
import os
import sys
# sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_src\\git_data\\'))
# sys.path.insert(2, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_src\\twitter_data\\'))
# ----- imports ----------------------------------------------------
import github_api as git
import fetch as twt
import doc_dist as dd
import datetime
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# ------------------------------------------------------------------
# nltk downloads
nltk.download('stopwords')
nltk.download('wordnet')

# text cleaning function w/ lemmatization
def clean_text(text):
    lemmatizer = WordNetLemmatizer()
    text = re.sub("\'", "", text) 
    text = re.sub("[^a-zA-Z]"," ",text) 
    text = ' '.join(text.split()) 
    text = text.lower()
    _t = ""
    for t in text.split():
        _t += lemmatizer.lemmatize(t, pos='a') + " "
    text = _t
    stop_words = set(stopwords.words('english'))
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    text = ' '.join(no_stopword_text)
    return text

# document distance function
def doc_dist(text1, text2):
    text1 = clean_text(text1)
    text2 = clean_text(text2)
    return dd.documentSimilarity(text1, text2)

# scoring overall candidate for job
def score_candidate(candy_data, ideal_data):
    print(":scoring git")
    git_score = git.gitDistance(ideal_data['gitId'], candy_data['gitId']) * ideal_data['gitId_mul']
    print(":scoring twt")
    big5_val, values_val = twt.twtScore(candy_data['tweetId'])
    big5_score = big5_val * ideal_data['big5_mul']
    values_score = big5_val * ideal_data['values_mul']
    print(":scoring responses")
    self_desc_score = -doc_dist(candy_data['self_desc'], ideal_data['self_desc']) * ideal_data['self_desc_mul']
    job_want_why_score = -doc_dist(candy_data['job_want_why'], ideal_data['job_want_why']) * ideal_data['job_want_why_mul']
    job_req_what_score = -doc_dist(candy_data['job_req_what'], ideal_data['job_req_what']) * ideal_data['job_req_what_mul']
    passion_score = -doc_dist(candy_data['passion'], ideal_data['passion']) * ideal_data['passion_mul']
    job_skills_score = -doc_dist(candy_data['jobskills'], ideal_data['jobskills']) * ideal_data['jobskills_mul']
    yoe_score = abs(ideal_data['yoe'] - candy_data['yoe']) * ideal_data['yoe_mul']
    apt_score = candy_data['apt'] * ideal_data['apt_mul']
    try:
        date_join_score = (datetime.datetime.strptime(str(ideal_data['date_join']), '%Yy-%m-%d') - datetime.datetime.strptime(candy_data['date_join'], '%m-%d-%y')).days * ideal_data['date_join_mul'] 
        print("date added")
    except:
        date_join_score = 0
        print("date not added")
    overall_score = git_score + big5_score + values_score + self_desc_score + job_want_why_score + job_req_what_score + passion_score + yoe_score + date_join_score + apt_score

    return overall_score