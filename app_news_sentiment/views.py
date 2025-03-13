'''
requirements:
tensorflow==2.3
'''
import re
from django.http import JsonResponse
import json
import os
from django.shortcuts import render

import pickle
import jieba

from tensorflow.keras.models import load_model

from tensorflow.keras.preprocessing import sequence

from django.views.decorators.csrf import csrf_exempt


jieba.set_dictionary('jieba_big_chinese_dict/dict.txt.big')

# We don't use GPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


# Read tokenizer
tokenizer = pickle.load(
    open('app_news_sentiment/sentiment_model/sentiment_tokenizer.pickle', 'rb'))


# Read CNN model
model = load_model(
    'app_news_sentiment/sentiment_model/sentiment_best_model.hdf5')

# home


def home(request):
    return render(request, "app_news_sentiment/home.html")


# api get sentiment score


@csrf_exempt
def api_get_sentiment_v0(request):
    new_text = request.POST['input_text']
    btn_source = request.POST['btn_source']

    if btn_source == 'btn_deep':  # cnn or mlp model
        sentiment_prob = get_sentiment_proba(new_text)
    elif btn_source == 'btn_baidu':
        sentiment_prob = get_sentiment_baidu(new_text)

    return JsonResponse(sentiment_prob)


chinese_word_regex = re.compile(r'[\u4e00-\u9fa5]+')


# api get sentiment score
@csrf_exempt
def api_get_sentiment(request):
    new_text = request.POST['input_text']
    btn_source = request.POST['btn_source']

    if btn_source == 'btn_deep':  # cnn or mlp model
        sentiment_prob = get_sentiment_proba(new_text)
    elif btn_source == 'btn_baidu':
        sentiment_prob = get_sentiment_baidu(new_text)

    return JsonResponse(sentiment_prob)


# get sentiment probability
def get_sentiment_proba(new_text):
    tokens = jieba.lcut(new_text, cut_all=False)
    # remove some characters
    tokens = [x for x in tokens if chinese_word_regex.match(x)]
    tokens = [tokens]
    # print(tokens)

    # Index the document
    new_text_seq = tokenizer.texts_to_sequences(tokens)
    # Pad the document
    max_document_length = 350
    new_text_pad = sequence.pad_sequences(
        new_text_seq, maxlen=max_document_length)

    result = model.predict(new_text_pad)

    response = {'Negative': round(
        float(result[0, 0]), 2), 'Positive': round(float(result[0, 1]), 2)}
    # Note that result is numpy format and it should be convert to float

    return response

# 百度NLP
# 需安裝套件
# pip install baidu-aip


'''
from aip import AipNlp
APP_ID = 'xxxx'
API_KEY = '????'
SECRET_KEY = '????'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def get_sentiment_baidu( new_text ):
    res = client.sentimentClassify(new_text)
    neg = res['items'][0]['negative_prob']
    pos = res['items'][0]['positive_prob']
    sentiment_prob = {'Negative': round(float(neg), 2), 'Positive': round(float(pos), 2)}
    return sentiment_prob
'''


# Public Restful API: get sentiment score
# 這一支Restful API可以給網頁、手機、平板、或其他程式呼叫
# 寫法比較複雜些，不過只是加上一些格式的檢查而已
# Your website must adapt CORS你必須讓網站可以允許跨站資源共享
@csrf_exempt
def api_restful_get_sentiment(request):

    # See the content_type and body
    print(request.content_type)
    print(request.body)  # byte format

    if request.content_type == "application/x-www-form-urlencoded":
        print("Content type: application/x-www-form-urlencoded")
        new_text = request.POST['input_text']  # or get('input_text')
    elif request.content_type in ["application/json", "text/plain"]:
        print("Content type: text/plain or application/json")
        # json.load can load data with json format
        request_json = json.loads(request.body)
        new_text = request_json['input_text']

    sentiment_prob = get_sentiment_proba(new_text)

    return JsonResponse(sentiment_prob)


print("app_news_sentiment was loaded!")
