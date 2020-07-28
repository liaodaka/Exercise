import requests, re
from bs4 import BeautifulSoup
from lxml import etree
from queue import PriorityQueue
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time


class Spider():
    keyword = input("输入书名：")
    target = 'https://www.xsbiquge.com/search.php?keyword=' + keyword
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    url = soup.a.attrs['href']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }

    def get_page_urls(self):
        rsp = requests.get(self.url, headers=self.headers)
        html = etree.HTML(rsp.content)
        titles = html.xpath('//dd/a/text()')[0]
        links = html.xpath('//dd/a/@href')
        links = ['https://www.xsbiquge.com/' + i for i in links]
        return links


class PageJob():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }

    def __init__(self, priority, url):
        self.priority = priority
        self.url = url
        self.GetContent()
        return

    def __lt__(self, other):
        return self.priority < other.priority

    def GetContent(self):
        rsp = requests.get(self.url, headers=self.headers)
        if rsp.status_code == 503:
            rsp = requests.get(self.url, headers=self.headers)
        html = etree.HTML(rsp.content)
        title = html.xpath('//h1/text()')[0]
        content = html.xpath('//div[@id="content"]/text()')[:-3]
        while '\r' in content:
            content.remove('\r')
        content = [re.sub('\xa0\xa0\xa0\xa0', '', i) for i in content]
        content = [re.sub('\r', '\n', i) for i in content]
        self.title = '\n\n' + title + '\n\n'
        self.content = content


def PutPageJob(para):
    q = para[0]
    i = para[1]
    links = para[2]
    q.put(PageJob(i, links[i]))


def get_content(target):
    reqs = requests.get(url=target)
    reqs.encoding = 'utf-8'
    hals = reqs.text
    bf = BeautifulSoup(hals, 'lxml')
    texts = bf.find('div', id='content')
    contents = texts.text.strip().split('\xa0' * 4)
    return contents


if __name__ == '__main__':
    start_time = time()
    spider = Spider()
    links = spider.get_page_urls()
    keyword = spider.keyword
    q = PriorityQueue()
    with ThreadPoolExecutor(max_workers=1000) as t:  # 创建一个最大容纳数量为1000的线程池
        obj_list = []
        links = links[0:]
        for i in range(len(links)):
            para = (q, i, links)
            p = t.submit(PutPageJob, para)
            obj_list.append(p)
        for future in as_completed(obj_list):
            data = future.result()
    while not q.empty():
        next_job = q.get()  # 可根据优先级取序列
        with open(keyword + '.txt', 'a', encoding='utf-8') as f:
            f.write(next_job.title)
            f.writelines(next_job.content)
    print('花费时间:', time() - start_time)
