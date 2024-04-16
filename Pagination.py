from bs4 import BeautifulSoup
import requests

root = 'https://subslikescript.com'
website = f'{root}/movies_letter-A'
response = requests.get(website)
content = response.text
soup = BeautifulSoup(content, 'html.parser')

#pagination
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

links=[]

for page in range(1, int(last_page)+1):
    # https://subslikescript.com/movies_letter-A?page=1
    response = requests.get(f'{website}?page={page}')
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    box = soup.find('article', class_='main-article')


    for link in box.find_all('a', href=True):
        links.append(link['href'])

    # print(links)

    for link in links:
        try:
            print(link)
            response = requests.get(f'{root}/{link}')
            content = response.text

            soup = BeautifulSoup(content, 'html.parser')
            box = soup.find('article', class_= 'main-article')

            title = box.find('h1').get_text()

            transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')
            with open(f'{title}.txt', 'w', encoding='UTF-8') as file:
                file.write(transcript)

        except:
            print('-----Link not working-----')
            print(link)

