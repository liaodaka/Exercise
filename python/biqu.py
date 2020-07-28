import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_content(target):
    reqs = requests.get(url=target)
    reqs.encoding = 'utf-8'
    hals = reqs.text
    bf = BeautifulSoup(hals, 'lxml')
    texts = bf.find('div', id='content')
    contents = texts.text.strip().split('\xa0' * 4)
    return contents


keyword = input("输入书名：")
target = 'https://www.xsbiquge.com/search.php?keyword=' + keyword
req = requests.get(url=target)
req.encoding = 'utf-8'
html = req.text
soup = BeautifulSoup(html, 'lxml')
target = soup.a.attrs['href']
print(target)
server = 'https://www.xsbiquge.com/'
book_name = keyword + '.txt'
req = requests.get(url=target)
req.encoding = 'utf-8'
html = req.text
chapter_bs = BeautifulSoup(html, 'lxml')
chapters = chapter_bs.find('div', id='list')
chapters = chapters.find_all('a')
print(chapters)
for chapter in tqdm(chapters):
    chapter_name = chapter.string
    url = server + chapter.get('href')
    content = get_content(url)
    with open(book_name, 'a', encoding='utf-8') as f:
        f.write(chapter_name)
        f.write('\n')
        f.write('\n'.join(content))
        f.write('\n')
