

# imports
import numpy as np
import requests
# import pandas as pd
from bs4 import BeautifulSoup
from cucco import Cucco
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import word_tokenize
import urllib.request
from urllib.request import urlopen

# list of urls
urls_list = ['https://sintesis.com.mx/puebla/2020/03/21/armando-prida-huerta-entrega-la-medalla-gilberto/',
             'http://www.diariopuntual.com/internacional/2018/07/18/1843',
             'https://sintesis.com.mx/puebla/2020/01/07/nelly-maceda-pide-castigo-a-funcionarios-que-propicien-la-trata-de-personas-o-el-trafico-ilegal-de-migrantes/']


# get article content and turn it into an array with headlines and p tags
number_rows = len(urls_list)
number_cols = 3
array_data = np.empty(shape=(number_rows,number_cols),dtype='object')


for i in range(number_rows):
    url_second = urls_list[i]
    array_data[i][0] = url_second
    array_data[i][1] = BeautifulSoup(requests.get(url_second).text, "lxml").find_all('h1')
    p_tags = BeautifulSoup(requests.get(url_second).text, "lxml").find_all('p')
    array_data[i][2] = [tag.get_text().strip() for tag in p_tags]
print(array_data[0][2])
print(len(array_data[0][2]))


# Cleaning the text
normEsp = Cucco()
norms = ['replace_punctuation', 'remove_extra_whitespaces']
new_stopwords = set(stopwords.words('spanish')) - {'ella', 'ellas', 'una', 'unas', 'él'}
quotations = ['“', '”']
new_stopwords.update(quotations)
print(new_stopwords)


for i in range(number_rows):
    p_tags_text = [normEsp.normalize(sentence, norms) for sentence in array_data[i][2]]
    espTokens = [word_tokenize(text) for text in p_tags_text]
    flatList = [word for sentList in espTokens for word in sentList]
    filtered = [word for word in flatList if word not in new_stopwords]
    array_data[i][2] = filtered

print(array_data[0][2])
print(len(array_data[0][2]))


for k in range(len(array_data)):
    for string_word in array_data[k][2]:
        espFreq = FreqDist(string_word)

espFreq = FreqDist(word for word in array_data[0][2])
for word, frequency in espFreq.most_common(20):
    print(u'{}: {}'.format(word, frequency))