from collections import defaultdict

from numpy import empty


def get_all_tokens():
    tokens = []
    with open('../2/tokens.txt', 'r', encoding='utf-8') as tokens_file:
        lines = tokens_file.readlines()
        for line in lines:
            token = line.strip()
            tokens.append(token)
    return tokens


def get_tokens_tf_idf(filename: str):
    tokens_tf_idf = dict()
    with open(filename, 'r', encoding='utf-8') as tf_idf_file:
        lines = tf_idf_file.readlines()
        for line in lines:
            split = line.split(' ')
            token = split[0]
            tf_idf = split[2]
            tokens_tf_idf[token] = tf_idf
    return tokens_tf_idf


def gen_vectors():
    vectors = defaultdict(list)
    for page_num in range(1, 101):
        page_vector = empty(len(tokens))
        filename = f'../4/tokens/{page_num}_tokens_tf-idf.txt'
        tokens_with_tf_idf = get_tokens_tf_idf(filename)
        for token in tokens:
            token_index = tokens.index(token)
            if token in tokens_with_tf_idf:
                page_vector[token_index] = tokens_with_tf_idf[token]
            else:
                page_vector[token_index] = 0
        vectors[page_num] = list(page_vector)
        print(page_num)
    return vectors


def write_pages_vectors(page_vectors: dict[int]):
    with open('vectors.txt', 'w+', encoding='utf-8') as vectors_file:
        for page_num, vector in page_vectors.items():
            vectors_file.write(f'{page_num} {vector}\n')


tokens = get_all_tokens()
# vectors = gen_vectors()
# write_pages_vectors(vectors)

