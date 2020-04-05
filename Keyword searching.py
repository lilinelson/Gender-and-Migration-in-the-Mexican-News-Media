# Imports
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk import FreqDist
import nltk.data
from cucco import Cucco


# Parameters/ Variables
keywords1 = ['inmigrante', 'migrante', 'migración', 'inmigrantes', 'migrantes', 'migratoria']
keywords2 = ['hombre', 'padre', 'niños', 'esposo', 'hombres', 'padres', 'esposos', 'masculina', 'masculino'
                                                                                                'mujer', 'niñas',
             'niña', 'madre', 'mujeres', 'esposa', 'esposas', 'madres', 'femenino', 'femenina'
                                                                                    'género', 'adolescente', 'adulta']

urls_list = [
    'https://www.capitalmexico.com.mx/cdmx/crisis-en-derechos-humanos-acarrea-retos-nuevos-a-la-antropologia-social-especialistas/',
    'https://sintesis.com.mx/puebla/2020/01/07/nelly-maceda-pide-castigo-a-funcionarios-que-propicien-la-trata-de-personas-o-el-trafico-ilegal-de-migrantes/']


# function 1: get the tokenized text
def load_sentences(list_urls):
    paragraphs_normalized = []
    token_paragraphs = []
    token_sentences = []
    normEsp = Cucco()
    norms = ['replace_punctuation', 'remove_extra_whitespaces']
    spanish_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
    for i in range(len(list_urls)):
        url = urls_list[i]
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        # headline = soup.find('h1').get_text()
        paragraphs = soup.find_all('p')
        stripped_paragraph = [tag.get_text().strip() for tag in paragraphs]
        for sentence in stripped_paragraph:
            paragraphs_normalized.append(normEsp.normalize(sentence, norms))
        for j in paragraphs_normalized:
            token_paragraphs.append(word_tokenize(j))
    return token_paragraphs


# function 2: search the text for keywords
def keyword_search(text, keyword_list):
    matched_sentences = []
    for sentence in text:
        for word in keyword_list:
            # if sentence.find(word) != -1 and sentence not in matched_sentences:
            if word in sentence and sentence not in matched_sentences:
                matched_sentences.append(sentence)
    return matched_sentences


# third function: clean the text and find the frequency
def load_freq(text):
    new_stopwords = set(stopwords.words('spanish')) - {'ella', 'ellas', 'una', 'unas', 'él'}
    quotations = ['“', '”']
    new_stopwords.update(quotations)
    filtered = []
    # flatList = [word for sentList in text for word in sentList]
    # print("Flat list: ", flatList)
    for sentence in text:
        for word in sentence:
            if word not in new_stopwords:
                filtered.append(word)
    print("Filtered: ", filtered)
    freqdist = nltk.FreqDist(filtered)
    freqdist.plot(10)


# run the first function
loaded_urls = load_sentences(urls_list)


# run the second function
searched_text = keyword_search(loaded_urls, keywords1)


# run the third function
load_freq(searched_text)
