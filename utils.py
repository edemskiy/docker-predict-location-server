import requests as rq
from bs4 import BeautifulSoup

def get_git_folder_files(url, ext=None):
    data = rq.get(url)
    parser = BeautifulSoup(data.text, 'lxml')
    tags = parser.findAll(lambda tag: tag.name=='a' and
                          tag.has_attr('href') and
                          tag.has_attr('title') and
                          tag.contents[0] == tag['href'][tag['href'].rfind('/')+1:])
    links = []
    for tag in tags:
        links.append('https://github.com' + tag.get('href') + '?raw=true')
    return links

