from collections import defaultdict
from vectors_generator import get_all_tokens
from numpy import dot
from numpy.linalg import norm

import ast


def gen_query_vector(query: str):
    tokens = get_all_tokens()
    query_vector = [0.0 for _ in range(len(tokens))]

    split = query.split(' ')
    split = [word.lower() for word in split]
    split = set(split)

    for word in split:
        if word in tokens:
            word_index = tokens.index(word)
            query_vector[word_index] = 1
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


if __name__ == '__main__':

    query = input('Введите запрос: ')
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
        counter = 1
        for page_num, rank in pages_rank.items():
            print(f'{counter}: {links[page_num - 1].strip()}')
            counter += 1

