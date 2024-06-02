# -*- coding: utf-8 -*-
import requests
from lxml import html
import json,os
from urllib.parse import urlparse
 
def url_to_path(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    # 移除path开头的'/'，并将其他的'/'替换为操作系统的路径分隔符
    return path.lstrip('/').replace('/', os.sep)
    #return path.lstrip('/').replace('/', os.sep)

def if_cache_path(url):
    cache_root = ".cache"
    # cache html
    domain = url.split("//")[1].split("/")[0]
    path = url_to_path(url)
    cache_path = os.path.join(cache_root, domain, path)
    return cache_path
    
def cache_html(url, html_data):
    cache_path = if_cache_path(url)
    cache_dir = os.path.dirname(cache_path)
    if not os.path.exists(cache_dir) : os.makedirs(cache_dir)
    with open(cache_path, "w") as fs:
        fs.write(html_data)  
    
def get_html(url):
    if os.path.exists(if_cache_path(url)):
        with open(if_cache_path(url), "r") as fs:
            html_data = fs.read()
    else:
        html_data = requests.get(url).text
        cache_html(url, html_data) 
    return html_data 
    
def parse_urls():
    res = requests.get("https://www.caiwenxiu.cn/wangwen.txt")
    res.encoding = res.apparent_encoding
    data = []
    for url in res.text.split("\n"):
        if url.startswith("#"): continue
        html_data = get_html(url) 
        parse_html = html.fromstring(html_data)
        # 纵横中文网
        if url.startswith("https://www.zongheng.com"):
            data.append(domain_zongheng(url, parse_html))
        if url.startswith("https://weread.qq.com"):
            data.append(domain_wxread(url, parse_html))
        if url.startswith("https://fanqienovel.com"):
            data.append(domain_fanqienovel(url, parse_html))
    return data

def domain_wxread(url, parse_html):
    title  = parse_html.xpath('//h2[@class="bookInfo_right_header_title_text"]/text()')[0]
    author = parse_html.xpath('//div[@class="bookInfo_author_container"]/a/text()')[0]
    icon   = parse_html.xpath('//div[@class="wr_bookCover bookInfo_cover"]/img/@src')[0]
#    desp  = parse_html.xpath('//div[@class="bookInfo_intro"]/text()')
    desp   = parse_html.xpath('//meta[@name="description"]/@content')[0]
    return to_string(url=url, title=title, author=author, icon=icon, desp=desp)

def domain_fanqienovel(url, parse_html):
    title  = parse_html.xpath('//div[@class="info-name"]/h1/text()')[0]
    author = parse_html.xpath('//span[@class="author-name-text"]/text()')[0]
    icon   = parse_html.xpath('//script/text()')[0]
    icon   = json.loads(icon.replace("\n", "").replace(" ", "")).get("image")[0]
    desp   = parse_html.xpath('//div[@class="page-abstract-content"]/p/text()')[0]
    return to_string(url=url, title=title, author=author, icon=icon, desp=desp)

def domain_zongheng(url, parse_html):
    # 纵横中文网
    title  = parse_html.xpath('//div[@class="book-info--title"]/span/text()')[0]
    author = parse_html.xpath('//a[@class="author-info--name"]/text()')[0].replace("\n", "").replace(" ", "")
    icon   = parse_html.xpath('//div[contains(@class,"book-info--coverImage-cover")]/img/@src')[0]
    script = parse_html.xpath('//script/text()')[0].replace("window.__NUXT__=(function(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u){return", "")
    begin_index = script.index("description")+12
    end_index   = script.index("totalWords")-1
    desp        = script[begin_index+1:end_index-1].replace("\\u003Cbr\\u003E", "")
    return to_string(url=url, title=title, author=author, icon=icon, desp=desp)
       
def to_string(url, title, icon,author, desp):
    title = title.replace(" ", "")
    author = author.replace(" ", "")
    return {
        "subject": 
            {
            "pic"   : { "large" : icon},
            "id"    : title+"_"+author,
            "url"   : url,
            "title" : title,
            "author": [author],
            "intro" : desp,
            "type"  : "wangwen",
            "rating": { "value" : 6.6 },
            "cover_url" : icon
            }   
        }
    
def save_file():
    file = "data/wangwen/books.json"
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    with open("data/wangwen/book.json","w") as fs:
        json.dump(parse_urls(), fs, indent=4, ensure_ascii=False)

save_file()
