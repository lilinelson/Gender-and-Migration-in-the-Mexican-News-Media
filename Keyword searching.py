# Imports
import requests
from bs4 import BeautifulSoup
import numpy as np

#Parameters/ Variables
keywords1 = ['inmigrante', 'migrante', 'migración', 'inmigrantes','migrantes']
keywords2 = ['mujer', 'mujeres', 'femenina', 'ella']

headline = ""

urls_list = ['https://heraldodepuebla.com/2020/01/23/ampliaran-programas-de-apoyo-a-migrantes/', 'https://sintesis.com.mx/puebla/2020/01/07/nelly-maceda-pide-castigo-a-funcionarios-que-propicien-la-trata-de-personas-o-el-trafico-ilegal-de-migrantes/']

#scrape article
number_rows = len(urls_list)
number_cols = 3
array_data = np.empty(shape=(number_rows,number_cols),dtype='object')
fulltext = ""

for i in range(number_rows):
    url = urls_list[i]
    array_data[i][0] = url
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    array_data[i][1] = soup.find('h1').get_text()
    list_paragraphs = soup.find_all('p')
    for elt in list_paragraphs:
        fulltext += elt.get_text()
    list_sentences = fulltext.split(".")
    i= 0
    for sentence in list_sentences:
        temp = sentence + "."
        list_sentences[i] = temp
        i += 1
    array_data[i][2] = list_sentences


result = ""
for i in range(number_rows):
    for sentence in array_data[i][2]:
        for word in keywords2:
             if (sentence.find(word) != -1) and (result.find(sentence) == -1):
                 print("Match")
                 result += sentence


# save results into text file
file = open("Testing" + "_newfile.txt", "a+")
file.write("\n Headline: " + headline)
file.write("\n Result: " + result)
file.close()