from django.http import JsonResponse
from app_news_sentiment.views import get_sentiment_proba
from app_news_sentiment.views import api_get_sentiment
import json
import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence
import pickle
import jieba
import numpy as np

jieba.set_dictionary('jieba_big_chinese_dict/dict.txt.big')

# We don't use GPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

model = load_model('app_news_classify/news_classify_model/news_cnn.hdf5')

# Load tokenizer news_classify_tokenizer.pickle
# app_news_classify\news_classify_model\news_classify_tokenizer.pickle
#tokenizer = pickle.load(open('app_news_classify/news_classify_model/news_classify_tokenizer.pickle', 'rb'))
tokenizer = pickle.load(open(
    'app_news_classify/news_classify_model/news_classify_tokenizer.pickle', 'rb'))

# category index
news_categories = ['政治', '科技', '運動', '證卷',
                   '產經', '娛樂', '生活', '國際', '社會', '文化', '兩岸']
idx2cate = {i: item for i, item in enumerate(news_categories)}

# home


def home(request):
    return render(request, "app_news_classify/home.html")


# import sentiment

# api: get news class given user input text


@csrf_exempt
def api_get_news_cate(request):

    new_text = request.POST.get('input_text')
    # print(new_text)

    news_cate = get_cate_proba(new_text)

    # Get sentiment: call sentiment app
    # (1) method 1: call sentiment api,
    senti = api_get_sentiment(request)
    # The format of return data is json format
    # we should use json.loads()
    sentiment = json.loads(senti.content)

    # print return data
    # print(senti.content)
    # print(senti.items()) # doesn't work

    # (2) method 2: easy way
    # sentiment = get_sentiment_proba(new_text)

    response = {
        'news_cate': news_cate,
        'news_sentiment': sentiment
    }

    return JsonResponse(response)


# get category probability
def get_cate_proba(new_text):
    tokens = jieba.lcut(new_text, cut_all=False)
    tokens = [tokens]
    # print(tokens)
    new_text_seq = tokenizer.texts_to_sequences(tokens)
    new_text_pad = sequence.pad_sequences(new_text_seq, maxlen=250)

    result = model.predict(new_text_pad)
    result_label = np.argmax(result, axis=-1)

    label = idx2cate[result_label[0]]
    proba = round(float(max(result[0])), 2)
    # Note that result is numpy format and it should be convert to float

    return {'label': label, 'proba': proba}


print("app news classification was loaded!")
