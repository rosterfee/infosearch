import requests
from bs4 import BeautifulSoup


def get_html(link):

    page = requests.get(link)
    html = page.text
    content = BeautifulSoup(html, 'html.parser')

    scripts = content.findAll("script")
    for script in scripts:
        script.decompose()

    links = content.findAll(attrs={'rel': 'stylesheet'})
    for link in links:
        link.decompose()

    return content.prettify(encoding='utf-8')


index = open('index.txt', 'w+')

with open('links.txt', 'r') as links:
    links = links.readlines()
    for i in range(len(links)):

        link = links[i]
        html = get_html(link)

        print(link, end='')

        page = open(f'{i + 1}.txt', 'w+')
        page.write(str(html))
        page.close()

        index.write(f"{i + 1} : {link}")

index.close()



