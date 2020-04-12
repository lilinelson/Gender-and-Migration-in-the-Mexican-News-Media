# To do
# Make not case sensitive


# Imports
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from cucco import Cucco
import seaborn as sns
from collections import Counter
import matplotlib.pyplot as plt

# Parameters/ Variables
keywords1 = ['inmigrante', 'migrante', 'migración', 'inmigrantes', 'migrantes', 'migratoria']
keywords2 = ['hombre', 'padre', 'niño','niños', 'esposo', 'hombres', 'padres', 'esposos', 'masculina', 'masculino']
keywords3= ['mujer', 'niñas', 'niña', 'madre', 'mujeres', 'esposa', 'esposas', 'madres', 'femenino', 'femenina']
keywords4 = ['género', 'adolescente', 'adulta']


migrantes_list = [
    'https://www.capitalmexico.com.mx/cdmx/crisis-en-derechos-humanos-acarrea-retos-nuevos-a-la-antropologia-social-especialistas/',
    'https://www.capitalmexico.com.mx/estados/se-compromete-sre-a-tomar-medidas-con-los-migrantes-varados-en-la-frontera-para-evitar-brotes-de-covid-19/',
    'https://www.capitalmexico.com.mx/nacional/pandemia-por-covid-19-es-un-reto-mayor-segob/',
    'https://www.capitalmexico.com.mx/estados/tabasco/mnpt-pide-al-inm-medidas-precautorias-luego-del-motin-registrado-en-tenosique-tabasco/',
    'https://www.capitalmexico.com.mx/nacional/cndh-solicita-a-inm-y-comar-implementas-medidas-cautelares-para-personas-en-estaciones-migratorias/',
    'https://sintesis.com.mx/puebla/2020/01/07/nelly-maceda-pide-castigo-a-funcionarios-que-propicien-la-trata-de-personas-o-el-trafico-ilegal-de-migrantes/',
    'http://www.diariopuntual.com/internacional/2018/07/18/1843',
    'https://sintesis.com.mx/puebla/2020/03/26/vences-valencia-pide-proteccion-para-migrantes-ante-pandemia/',
    'https://sintesis.com.mx/puebla/2020/03/21/armando-prida-huerta-entrega-la-medalla-gilberto/',
    'https://sintesis.com.mx/puebla/2019/12/18/pasaportes-menores-retorno-migrantes/',
    'https://sintesis.com.mx/puebla/2019/07/07/inmigrantes-viaje-averno/',
    'https://www.elpopular.mx/2018/11/08/mundo/mexico-tiene-mas-migrantes-de-eu-que-de-centroamerica-193207']


# function 1: get the tokenized text
def load_sentences(list_urls):
    paragraphs_normalized = []
    token_paragraphs = []
    normEsp = Cucco()
    norms = ['replace_punctuation', 'remove_extra_whitespaces']
    for i in range(len(list_urls)):
        url = list_urls[i]
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        # headline = soup.find('h1').get_text()
        paragraphs = soup.find_all('p')
        stripped_paragraph = [tag.get_text().strip() for tag in paragraphs]
        for sentence in stripped_paragraph:
            paragraphs_normalized.append(normEsp.normalize(sentence, norms))
        for j in paragraphs_normalized:
            token_paragraphs.append(word_tokenize(j))
    return token_paragraphs


# function 2: search the text for keywords and clean so that no stop words or keywords appear in the filtered text
def keyword_search(text, keyword_list):
    matched_sentences = []
    new_stopwords = set(stopwords.words('spanish')) - {'ella', 'ellas', 'una', 'unas', 'él'}
    quotations = ['“', '”', 'así', 'hace', 'Por']
    new_stopwords.update(quotations)
    filtered = []
    for sentence in text:
        for word in keyword_list:
            if word in sentence and sentence not in matched_sentences:
                matched_sentences.append(sentence)
    for sentence in matched_sentences:
        for word in sentence:
            if word not in new_stopwords and word not in keyword_list:
                filtered.append(word)
    return filtered


# third function: clean the text and plot the frequency
def load_freq(text, title):
    counter = Counter(text)
    most = counter.most_common()
    x, y = [], []
    for word, count in most[:15]:
        x.append(word)
        y.append(count)
    sns.barplot(x=y, y=x, color='cyan').set_title(title)
    plt.show()


# run the first function
loaded_urls = load_sentences(migrantes_list)


# run the second function
migrant_matched = keyword_search(loaded_urls, keywords1)
male_matched = keyword_search(loaded_urls, keywords2)
female_matched = keyword_search(loaded_urls, keywords3)


# run the third function
load_freq(migrant_matched, 'Migrant Keywords')
load_freq(male_matched, 'Gendered Keywords')
load_freq(female_matched, 'Gendered Keywords')