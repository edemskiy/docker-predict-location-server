import os
import requests as rq
from bs4 import BeautifulSoup

models_folder_url = 'https://github.com/edemskiy/docker-predict-location-server/tree/master/models'
scalers_models_folder_url = 'https://github.com/edemskiy/docker-predict-location-server/tree/master/scalers'
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

def download_by_url(url, name):
    with open(name, 'wb') as f:  
        f.write(rq.get(url).content)

def download_folder_from_git(url, to_subfolder=True):
    urls = get_git_folder_files(url)
    if to_subfolder:
        folder_name = url[url.rfind('/') + 1:]
        os.mkdir(folder_name)
    
    for url in urls:
        name = url[url.rfind('/') + 1:-9]
        if to_subfolder:
            name = folder_name + '/' + name
        download_by_url(url, name)
