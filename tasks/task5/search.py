from collections import defaultdict
from vectors_generator import get_all_tokens
from numpy import dot
from numpy.linalg import norm
import spacy
import ast

nlp = spacy.load('ru_core_news_sm')
lemmas = defaultdict()


def init_lemmas_dict():
    with open('../task2/lemmas.txt', encoding='utf-8') as lemmas_file:
        lines = lemmas_file.readlines()
        for line in lines:
            split = line.strip().split(' ')
            lemmas[split[0]] = [split[i] for i in range(1, len(split))]
        return lemmas


def gen_query_vector(query: str):
    tokens = get_all_tokens()
    query_vector = [0.0 for _ in range(len(tokens))]

    split = query.split(' ')
    split = [word.lower() for word in split]
    split = set(split)

    for word in split:
        if word in tokens:
            token_index = tokens.index(word)
            query_vector[token_index] = 1
        else:
            continue

    return query_vector


def gen_pages_vectors_dict():
    pages_vectors = dict()
    with open('vectors.txt', 'r', encoding='utf-8') as vectors_file:
        lines = vectors_file.readlines()
        for line in lines:
            split = line.split(' ', maxsplit=1)
            page_num = int(split[0])
            vector = ast.literal_eval(split[1])
            pages_vectors[page_num] = vector
    return pages_vectors


def get_search_results(query: str):
    query_vector = gen_query_vector(query)
    pages_vectors = gen_pages_vectors_dict()

    pages_rank = defaultdict(int)
    for page_num, vector in pages_vectors.items():
        similarity = dot(vector, query_vector) / (norm(vector) * norm(query_vector))
        similarity = similarity if str(similarity) != 'nan' else 0.0
        pages_rank[page_num] = similarity
    pages_rank = dict(sorted(pages_rank.items(), key=lambda item: item[1], reverse=True))

    with open('../links.txt', 'r', encoding='utf-8') as links_file:
        links = links_file.readlines()
        result_links = dict()
        for page_num in pages_rank.keys():
            result_links[page_num] = links[page_num - 1].strip()
        return result_links


lemmas_dict = init_lemmas_dict()
