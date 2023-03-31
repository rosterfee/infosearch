from collections import defaultdict
from bs4 import BeautifulSoup
import spacy
import re
from nltk.corpus import stopwords


nlp = spacy.load('ru_core_news_sm')

stopwords = stopwords.words('russian')
tokens = set()
lemmas = defaultdict(set)

with open('tokens.txt', 'w+', encoding='utf-8') as tokens_file:
    for i in range(1, 101):
        with open(f'../{i}.txt', 'r', encoding='utf-8') as file:

            html = BeautifulSoup(file, 'html.parser')
            doc = nlp(html.get_text(" ").lower().strip())

            for token in doc:

                word = token.text
                if token.is_alpha and not token.like_num and not token.is_punct and re.match('[а-яА-Я]', word) \
                        and word not in stopwords:
                    tokens.add(word)
                    lemmas[token.lemma_].add(word)

    for token in tokens:
        tokens_file.write(token + '\n')

    with open('lemmas.txt', 'w+', encoding='utf-8') as lemmas_file:
        for lemma, tokens in lemmas.items():
            line = str(lemma) + ' ' + ' '.join(map(str, tokens))
            lemmas_file.write(line + '\n')

tokens_file.close()
lemmas_file.close()
