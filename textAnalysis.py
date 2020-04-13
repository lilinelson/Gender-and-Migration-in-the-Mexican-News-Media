import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from cucco import Cucco
import seaborn as sns
from collections import Counter
import matplotlib.pyplot as plt

# goal:get headline of web page
# inputs: url
# return: headline
def get_page_headline (url):
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    headline = soup.find('h1').get_text().strip()
    return headline

# goal: get page sentences
# inputs: url
# return: list of sentences
def get_page_sentences(url):
    stripped_sentences, final_sentences = ([] for i in range(2))
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    list_paragraphs = soup.find_all('p')
    stripped_sentences = [tag.get_text().strip() for tag in list_paragraphs]
    norm_esp = Cucco()
    norms = ['replace_punctuation', 'remove_extra_whitespaces']
    for sentence in stripped_sentences:
        if len(sentence) > 0:
            final_sentences.append(norm_esp.normalize(sentence, norms))
    return final_sentences

# goal: get tokenized sentences
# inputs: sentence_list
# return: list of token sentences (list of list)
def get_token_sentences(sentence_list):
    return [word_tokenize(word) for word in sentence_list]

# goal: create corpus of sentences to analyze
# inputs:
# return: list of sentences
def create_corpus_by_url(url_list):
    corpus = []
    for url in url_list:
        headline = get_page_headline(url)
        sentence_list = get_page_sentences(url)
        for sentence in sentence_list:
            corpus.append(sentence)
        # TODO: Save in file and remove the print part
    return corpus

# goal: search for related words in specific (keyword) sentences
# inputs: sentence_list, keyword_list
# return:  list of related words
def search_related_words (sentence_list, keyword_list):
    token_sentences, matched_sentences, related_words_list = ([] for i in range(3))
    new_stopwords = set(stopwords.words('spanish')) - {'ella', 'ellas', 'una', 'unas', 'él'}
    quotations = ['“', '”', 'así', 'hace', 'Por']
    new_stopwords.update(quotations)

    # token sentences
    token_sentences = get_token_sentences(sentence_list)

    # get matched sentences
    for sentence in token_sentences:
        for keyword in keyword_list:
            if (keyword in sentence) and (sentence not in matched_sentences):
                matched_sentences.append(sentence)

    # get related words in matched sentences that are not initial keywords and stopwords
    for sentence in matched_sentences:
        for word in sentence:
            if (word not in new_stopwords) and (word not in keyword_list):
                related_words_list.append(word)
    return related_words_list

# goal: show the frequency
# inputs:
# return:
def show_word_frequency (word_list, title):
    counter = Counter(word_list)
    most = counter.most_common()
    x, y = [], []
    for word, count in most[:15]:
        x.append(word)
        y.append(count)
    sns.barplot(x=y, y=x, color='cyan').set_title(title)
    plt.show()


# inputs: keyword_list
# return: url_list
def generate_urls_google (keyword_list):
    # todo: selenium lio
    return 0