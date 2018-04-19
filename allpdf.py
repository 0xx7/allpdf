import requests
import random
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse, parse_qs

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
BLACK_DOMAIN = ['www.google.gf', 'www.google.io', 'www.google.com.lc']

DOMAIN = 'www.google.com'
URL_SEARCH = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1"
URL_NUM = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1&num={num}"
URL_NEXT = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1&num={num}&start={start}"



def get_random_user_agent():
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    return random.choice(get_data('user_agents.txt', USER_AGENT))

def get_random_domain():
    """
    Get a random domain.
    :return: Random user agent string.
    """
    domain = random.choice(get_data('all_domain.txt', DOMAIN))
    if domain in BLACK_DOMAIN:
        self.get_random_domain()
    else:
        return domain

def get_data(filename, default=''):
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(__file__)
    user_agents_file = os.path.join(
        os.path.join(root_folder, 'data'), filename)
    try:
        with open(user_agents_file) as fp:
            data = [_.strip() for _ in fp.readlines()]
    except:
        data = [default]
    return data

def search_page(query, language=None, num=None, start=0, pause=2):
    """
    Google search
    :param query: Keyword
    :param language: Language
    :return: result
    """
    time.sleep(pause)
    domain = get_random_domain()
    if start > 0:
        url = URL_NEXT
        url = url.format(
            domain=domain, language=language, query=quote_plus(query), num=num, start=start)
    else:
        if num is None:
            url = URL_SEARCH
            url = url.format(
                domain=domain, language=language, query=quote_plus(query))
        else:
            url = URL_NUM
            url = url.format(
                domain=domain, language=language, query=quote_plus(query), num=num)
    if language is None:
        url = url.replace('hl=None&', '')
    # Add headers
    headers = {'user-agent': get_random_user_agent()}
    try:
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        r = requests.get(url=url,
                        headers=headers,
                        allow_redirects=False,
                        verify=False,
                        timeout=30)
        content = r.text
        return content
    
    except Exception as e:
        print('error')
        return None

def download_file(url, type): 
    if 'www.' not in url:
        url = 'http://www.' + url
    name = url.split('/')[-1]
    local_filename = os.path.join('./', type + '-files/', name)
    time.sleep(4) 
    headers = {'user-agent': get_random_user_agent()}
    try:
        r = requests.get(url, headers=headers, stream=True)
        print('Donwloading %-30s' % name, end = '')
        with open(local_filename, 'wb') as f: 
            for chunk in r.iter_content(chunk_size=1024):  
                if chunk: # filter out keep-alive new chunks 
                    f.write(chunk) 
                    f.flush()
            f.close()
        print('   Done')
    except Exception as e:
        pass

if __name__ == '__main__':
    if not os.path.exists('pdf-files'):
        os.mkdir('pdf-files')
    print('Downloading pdf files...........')
    start = 0
    while True:
        content = search_page(query='site:paychex.com filetype:pdf', start=start)
        soup = BeautifulSoup(content, "html.parser")
        items = soup.select('cite')
        start += len(items)
        for i in items:
            download_file(i.get_text(), 'pdf')
        if len(items) < 10:
            break
