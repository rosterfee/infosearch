from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from spacy.tokens import Token

import math
import re
import spacy


def get_token_tf(token: str, page_num: int):
    return doc_tokens_index[page_num][token] / doc_tokens_count[page_num]


def get_token_idf(token: str):
    return math.log10(100 / token_in_docs[token])


def get_lemma_tf(lemma: str, page_num: int):
    return doc_lemmas_index[page_num][lemma] / doc_tokens_count[page_num]


def get_lemma_idf(lemma: str):
    return math.log10(100 / lemma_in_docs[lemma])


def fillIndexes():
    for page_num in range(1, 101):
        with open(f'../{page_num}.txt', 'r', encoding='utf-8') as page_file:

            html = BeautifulSoup(page_file, 'html.parser')
            doc = nlp(html.get_text(" ").lower().strip())

            used_tokens = set()
            used_lemmas = set()
            doc_tokens_count[page_num] = len(doc)
            doc_tokens_index[page_num] = dict()
            doc_lemmas_index[page_num] = dict()

            for token in doc:

                if token_is_right(token):

                    if doc_tokens_index.__contains__(token.text):
                        doc_tokens_index[page_num][token.text] += 1
                    else:
                        doc_tokens_index[page_num][token.text] = 1
                    if token.text not in used_tokens:
                        if token_in_docs.__contains__(token.text):
                            token_in_docs[token.text] += 1
                        else:
                            token_in_docs[token.text] = 1
                        used_tokens.add(token.text)

                    lemma = token.lemma_
                    token_count_in_doc = doc_tokens_index[page_num][token.text]
                    if doc_lemmas_index.__contains__(lemma):
                        doc_lemmas_index[page_num][lemma] += token_count_in_doc
                    else:
                        doc_lemmas_index[page_num][lemma] = token_count_in_doc
                    if lemma not in used_lemmas:
                        if lemma_in_docs.__contains__(lemma):
                            lemma_in_docs[lemma] += token_count_in_doc
                        else:
                            lemma_in_docs[lemma] = token_count_in_doc
                        used_lemmas.add(lemma)


def token_is_right(token: Token):
    return token.is_alpha and not token.like_num and not token.is_punct and re.match('[а-яА-Я]', token.text) \
           and token.text not in stopwords


stopwords = stopwords.words('russian')
nlp = spacy.load('ru_core_news_sm')

doc_tokens_count = defaultdict(int)
doc_tokens_index = defaultdict(dict)
doc_lemmas_index = defaultdict(dict)
token_in_docs = defaultdict(int)
lemma_in_docs = defaultdict(int)

if __name__ == '__main__':

    fillIndexes()

    for page_num in range(1, 101):

        with open(f'../{page_num}.txt', 'r', encoding='utf-8') as page_file:

            html = BeautifulSoup(page_file, 'html.parser')
            doc = nlp(html.get_text(" ").lower().strip())

            tokens_tf_idf_file = open(f'tokens/{page_num}_tokens_tf-idf.txt', 'w+', encoding='utf-8')
            lemmas_tf_idf_file = open(f'lemmas/{page_num}_lemmas_tf-idf.txt', 'w+', encoding='utf-8')

            used_tokens = []
            used_lemmas = []
            for token in doc:

                if token_is_right(token):

                    if token.text not in used_tokens:

                        token_tf = get_token_tf(token.text, page_num)
                        token_idf = get_token_idf(token.text)
                        token_tf_idf = token_tf * token_idf
                        tokens_tf_idf_file.write(f'{token.text} {token_idf} {token_tf_idf}\n')

                        used_tokens.append(token.text)

                        lemma = token.lemma_
                        if lemma not in used_lemmas:
                            lemma_tf = get_lemma_tf(lemma, page_num)
                            lemma_idf = get_lemma_idf(lemma)
                            lemma_tf_idf = lemma_tf * lemma_idf
                            lemmas_tf_idf_file.write(f'{lemma} {lemma_idf} {lemma_tf_idf}\n')
                            used_lemmas.append(lemma)
                        else:
                            continue
                    else:
                        continue

            tokens_tf_idf_file.close()
            lemmas_tf_idf_file.close()
