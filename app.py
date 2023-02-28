from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from lxml import etree

import re

app = Flask(__name__)
@app.route('/', methods=["GET","POST"])



 

def index():
    blog_data = []
    html_text = requests.get('https://blog.medium.com/latest')
    soup = BeautifulSoup(html_text.content, 'html.parser')
    dom = etree.HTML(str(soup))
    
    news_article = soup.find('div', class_="js-postListHandle")

    articles = set(map(lambda x:x.get('href'), news_article.find_all("a" , class_="button button--smaller button--chromeless u-baseColor--buttonNormal",attrs={'href': re.compile("^https://")}) ))
    count = 0
    for article in articles:
        if count >= 10:  
            break
        url = article 
        print (url)
        res = requests.get (article)
        soup = BeautifulSoup(res.text, "html.parser")

        title = (soup.find("h1", {"class":"pw-post-title"}).text if soup.find("h1", {"class": "pw-post-title"}) else "")
        author = (soup.find("div", {"class":"ab q"}).text if soup.find("div", {"class": "ab q"}) else "")
        link = article
        #content = (soup.find("p", {"class":"pw-post-body-paragraph"}).text if soup.find("p", {"class": "pw-post-body-paragraph"}) else "")
        content = ''
        content_tags = soup.find_all("p", {"class":"pw-post-body-paragraph"})
        for content_tag in content_tags:
            content += content_tag.text + '\n'
        #tags = [tag.text for tag in soup.find("div", class_="mq di dt ")]
        responses = (soup.find("p", {"class":"bd b be z dw"}).text if soup.find("p", {"class": "bd b be z dw"}) else "")
        
        if author and title:
            blog_post = {
                'title': title,
                'link' : link,
                'author': author,
                'content': content,
                #'tags': tags,
                'responses': responses,
              
                
                
            }  
            blog_data.append(blog_post)
            count += 1
        
        
    return render_template("index.html", Blogs= blog_data)

@app.route('/blog_post/<title>/<author>/<content>/<responses>')
def blog_post(title, author, content, responses):
    return render_template('blog_post.html', title=title, author=author, content=content, responses=responses)









