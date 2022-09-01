from django.shortcuts import render
from . import forms
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer,WordNetLemmatizer
nltk.download('wordnet')
import pickle
import joblib
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Create your views here.
def base(request):
    return render(request,"index/base.html")


def result(request):
    c=44535
    form = forms.testp()
    if request.method == "POST":
        model = joblib.load("modelsvc.sav")
        tfi = pickle.load(open("tfidf.pkl","rb"))
        lemmi = WordNetLemmatizer()
        cv = TfidfVectorizer(lowercase=True,stop_words="english",vocabulary = tfi.vocabulary_)        
        form = forms.testp(request.POST)
        data = []
        if form.is_valid():
            temp = []
            pos = 0
            neg = 0
            prediction = "Neutral or Hold"
            c+=1
            date = datetime.now()
            year = date.year
            month = date.month
            #url = "https://economictimes.indiatimes.com"
            url = "https://economictimes.indiatimes.com/archivelist/year-{},month-{},starttime-{}.cms".format(year,month,c)
            req = requests.get(url)
            soup = BeautifulSoup(req.content,'html.parser')
            las = soup.find_all('li')
            company = form.cleaned_data['text']
            for i in las:
                if str(company) in i.text.lower() :
                    data.append(i.text.lower())
            data = list(set(data))
            if len(data)>0:
                for i in data:
                    t = re.sub("[^a-zA-Z]"," ",str(i))
                    t = t.lower()
                    t = t.split()
                    t = [lemmi.lemmatize(word) for word in t]
                    temp.append(" ".join(t))
                X = (cv.fit_transform(temp)).toarray()
                pred = model.predict(X)
                for i in pred:
                    if i == 1:
                        pos+=1
                    if i ==-1:
                        neg+=1
                if pos>neg:
                    prediction = "Buy or Positive"
                if neg>pos:
                    prediction = "Sell or Negative"
                
                

                return render(request,"index/result.html",{"pred":prediction,"data":temp,"company":company})
            else:
                return render(request,"index/result.html",{"pred":"Neutral","company":company})

            
            

            
            

            
    return render(request,"index/result.html",{})



def test(request):
    form = forms.news_company()
    if request.method == "POST":
        form = forms.news_company(request.POST)
        if form.is_valid():
            url = "https://economictimes.indiatimes.com"
            req = requests.get(url)
            soup = BeautifulSoup(req.content,'html.parser')
            las = soup.find_all('a')
            company = form.cleaned_data['text']
            data = []
            link = []
            for i in las:
                if company in i.text.lower() :
                    data.append(i.text)
                    if i["href"][0]=="/":
                        link.append(url+i["href"])
                    else:
                        link.append(i["href"])
            return render(request,"index/test.html",{"news":zip(data,link),"company":company})
    return render(request,"index/test.html",{"form":form})













def index(request):
    form = forms.testp()
    p = ""
    if request.method == "POST":
        form = forms.testp(request.POST)
        model = joblib.load("modelsvc.sav")
        tfi = pickle.load(open("tfidf.pkl","rb"))
        lemmi = WordNetLemmatizer()
        cv = TfidfVectorizer(lowercase=True,stop_words="english",vocabulary = tfi.vocabulary_)
        if form.is_valid():
            return result(request)

    return render(request,"index/index.html",{"form":form,"prediction":p})












