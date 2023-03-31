import os
import numpy as np

import spacy
from numpy import linalg as la


def fill_vectors():
    with open('../2/lemmas.txt') as lemmas_file:
        for line in lemmas_file:
            lemma = line.split(' ')[0]
            null_vector_lemmas.append(lemma)
            null_vector.append(0)


null_vector_lemmas = []
null_vector = []

nlp = spacy.load("ru_core_news_sm")
fill_vectors()
pages = {}

for file in os.listdir('../4/lemmas'):
    with open(f'../4/lemmas/{file}', 'r') as f:
        page_num = file.split("_")[1].strip(".txt")
        pages[page_num] = [0] * len(null_vector_lemmas)
        for line in f:
            word, _, tf_idf = line.split()
            try:
                pages[page_num][null_vector_lemmas.index(nlp(word)[0].lemma_)] = float(tf_idf)
            except Exception as e:
                pass
while True:
    request = input("Введите запрос: ")

    word_weight = len(request.split()) / len(null_vector_lemmas)
    word_vector = [0] * len(null_vector)
    for word in request.split():
        try:
            word_vector[null_vector_lemmas.index(nlp(word)[0].lemma_)] = word_weight
        except Exception as e:
            pass

    result_array = []
    for key in pages:
        page_vector = pages.get(key)

        scalar_product = np.dot(word_vector, page_vector)
        similarity = scalar_product / (la.norm(word_vector) * la.norm(page_vector))
        result_array.append((key, similarity))

    print(sorted(result_array, key=lambda x: x[1], reverse=True))
