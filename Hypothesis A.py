

# imports
import numpy as np
import requests
# import pandas as pd
from bs4 import BeautifulSoup
from cucco import Cucco
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import word_tokenize

# list of urls
urls_list = []
number_urls = int(input("Enter number of articles: "))
for i in range(0, number_urls):
    url_first = input("Enter the article url: ")
    urls_list.append(url_first)

#get article content and turn it into an array with headlines and p tags
number_rows =len(urls_list)
number_cols = 3
array_data = np.empty(shape=(number_rows,number_cols),dtype='object')

for i in range(number_rows):
    url_second = urls_list[i]
    array_data[i][0] = url_second
    p_tags = BeautifulSoup(requests.get(url_second).text).find_all('p')
    array_data[i][1] = BeautifulSoup(requests.get(url_second).text).find_all('h1')
    array_data[i][2] = [tag.get_text().strip() for tag in p_tags]
#save to csv if wanted
#pd.DataFrame(arra_data).to_csv("HypothesisA.csv")

#Cleaning the text
normEsp = Cucco()
norms = ['replace_punctuation', 'remove_extra_whitespaces']
new_stopwords = set(stopwords.words('spanish')) - {'ella', 'ellas', 'una', 'unas', 'él'}
for i in range(number_rows):
    p_tags_text = [normEsp.normalize(sentence, norms) for sentence in array_data[i][2]]
    espTokens = [word_tokenize(text) for text in p_tags_text]
    flatList = [word for sentList in espTokens for word in sentList]
    filtered = [word for word in flatList if word not in new_stopwords]
    array_data[i][2] = filtered

espFreq = FreqDist(word for word in array_data[0][2])
for word, frequency in espFreq.most_common(20):
    print(u'{}: {}'.format(word, frequency))

