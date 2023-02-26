from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
@app.route('/', methods=["GET","POST"])

def index():
    blog_data = []
    html_text = requests.get('https://blog.medium.com/latest')
    soup = BeautifulSoup(html_text.content, 'html.parser')

   
    articles= soup.find_all('div', class_="u-paddingTop20 u-paddingBottom25 u-borderBottomLight js-block", limit=10)
   
    for article in articles:
        title = article.h3.text
        author = article.find('a', class_="ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken is-touched")
        #link = "https://medium.com"+article.find('a', class_="ae af ag ah ai aj ak al am an ao ap aq ar as")['href']
        blog_post = {
                'title': title,
                #'link' : link,
                'author': author,
                
            }  
        blog_data.append(blog_post)
        
    return render_template("index.html", Blogs= blog_data)









