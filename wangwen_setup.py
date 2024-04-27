# -*- coding: utf-8 -*-
import requests
from lxml import html
import json,os

urls = []
def parse_urls():
    urls = requests.get("https://www.caiwenxiu.cn/wangwen.txt").text.split("\n")
    data = []
    for url in urls:
        if url.startswith("#"): continue
        html_data = requests.get(url.replace("\n", "")).text
        parse_html = html.fromstring(html_data)
        # 纵横中文网
        if url.startswith("https://www.zongheng.com"):
            data.append(domain_zongheng(url, parse_html))
        if url.startswith("https://weread.qq.com"):
            data.append(domain_wxread(url, parse_html))
    return data

def domain_wxread(url, parse_html):
    title = parse_html.xpath('//h2[@class="bookInfo_right_header_title_text"]/text()')[0]
    author = parse_html.xpath('//div[@class="bookInfo_author_container"]/a/text()')[0]
    icon = parse_html.xpath('//div[@class="wr_bookCover bookInfo_cover"]/img/@src')[0]
#    desp = parse_html.xpath('//div[@class="bookInfo_intro"]/text()')
    desp = parse_html.xpath('//meta[@name="description"]/@content')[0]
    return to_string(url=url, title=title, author=author, icon=icon, desp=desp)

def domain_zongheng(url, parse_html):
    # 纵横中文网
    title = parse_html.xpath('//div[@class="book-info--title"]/span/text()')[0]
    author = parse_html.xpath('//div[@class="author-info--name"]/text()')[0].replace("\n", "")
    icon = parse_html.xpath('//div[contains(@class,"book-info--coverImage-cover")]/img/@src')[0]
    script = parse_html.xpath('//script/text()')[0].replace("window.__NUXT__=(function(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u){return", "")
    begin_index = script.index("description")+12
    end_index = script.index("totalWords")-1
    desp = script[begin_index+1:end_index-1].replace("\\u003Cbr\\u003E", "")
    return to_string(url=url, title=title, author=author, icon=icon, desp=desp)
       
def to_string(url, title, icon,author, desp):
    title = title.replace(" ", "")
    author = author.replace(" ", "")
    return {
        "subject": 
            {
            "pic":{ "large" : icon},
            "id" : title+"_"+author,
            "url": url,
            "title" : title,
            "author": [author],
            "intro"  : desp
            }   
        }
    
def save_file():
    file = "data/wangwen/books.json"
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    with open("data/wangwen/book.json","w") as fs:
        json.dump(parse_urls(), fs, indent=4)

save_file()
