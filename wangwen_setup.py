import requests
from lxml import html
import json,os

urls = []
def parse_urls():
    with open("wangwen.txt", "r") as fs:
       urls = fs.readlines()
    data = []
    for url in urls:
        if not url.startswith("http"): continue
        html_data = requests.get(url).text
        parse_html = html.fromstring(html_data)
        # 纵横中文网
        id= url.split("/")[-1]
        title = parse_html.xpath('//div[@class="book-info--title"]/span/text()')[0]
        author = parse_html.xpath('//div[@class="author-info--name"]/text()')[0].replace(" ", "")
        icon = parse_html.xpath('//div[contains(@class,"book-info--coverImage-cover")]/img/@src')[0]
        desp = parse_html.xpath('//div[@id="pane-bookinfo"]/text()')
        script = parse_html.xpath('//script/text()')[0].replace("window.__NUXT__=(function(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u){return", "")
        begin_index = script.index("description")+12
        end_index = script.index("totalWords")-1
        desp = script[begin_index:end_index]
    
    data.append({
        "subject": 
            {
            "pic":{ "large" : icon},
            "id" : id,
            "title" : title,
            "author": [author],
            "intro"  : desp
            }   
        })
    return data

def save_file():
    file = "data/wangwen/books.json"
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    with open("data/wangwen/book.json","w") as fs:
        fs.write(json.dumps(parse_urls()))

save_file()