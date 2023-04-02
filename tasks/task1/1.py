import requests

index = open('../index.txt', 'w+')

headers = {'User-Agent': 'Mozilla/task5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/111.0.0.0 Safari/537.36'
           }
with open('../links.txt', 'r') as links:
    links = links.readlines()
    error_links = []
    for i in range(100):

        link = links[i]
        response = requests.get(link.strip(), headers=headers)

        with open(f'../{i + 1}.txt', 'w+', encoding='utf-8') as file:
            file.write(response.text)
            file.close()

        index.write(f"{i + 1} : {link}")

index.close()

