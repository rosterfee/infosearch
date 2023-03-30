from collections import defaultdict

from bs4 import BeautifulSoup
import re
import spacy
from nltk.corpus import stopwords

stopwords = stopwords.words('russian')
nlp = spacy.load('ru_core_news_sm')

revert_index = defaultdict(set)


def gen_invert_index():
    for page_num in range(1, 101):

        file = open(f'../{page_num}.txt', 'r', encoding='utf-8')
        html = BeautifulSoup(file, 'html.parser')

        doc = nlp(html.get_text(" ").lower().strip())
        for token in doc:
            if token.is_alpha and not token.like_num and not token.is_punct and re.match('[а-яА-Я]', token.text) \
                    and token.text not in stopwords:
                revert_index[token.text].add(page_num)

    # сортирую индекс по токенам
    sorted_revert_index = dict(sorted(revert_index.items()))
    # сортирую индекс по номерам страниц
    for token, page__nums in sorted_revert_index.items():
        sorted_revert_index[token] = sorted(page__nums)

    with open('invert_index.txt', 'w+', encoding='utf-8') as revert_index_file:
        for token, page__nums in sorted_revert_index.items():
            revert_index_file.write(token + ' ' + ' '.join(map(str, page__nums)) + '\n')
    revert_index_file.close()


def search_and(word1, word2):
    print(revert_index[word1].intersection(revert_index[word2]))


def search_or(word1, word2):
    print(revert_index[word1].union(revert_index[word2]))


def search_not(word1, word2):
    all_page_ids = set(range(1, 101))
    print(all_page_ids - revert_index[word1] - revert_index[word2])


gen_invert_index()

word1 = 'атлетов'
word2 = 'атлетика'
search_and(word1, word2)
search_or(word1, word2)
search_not(word1, word2)
