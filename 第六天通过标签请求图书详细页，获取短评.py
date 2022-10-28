
import requests                  #引入 requests 库
from bs4 import BeautifulSoup    #引入 BeautifulSoup 库
import random     #引入random库

# 通过豆瓣 Top250 的 <a> 标签，请求图书详细页，获取前 10 本书的短评，并保存至本地文件。

#ua列表
ua_list=[
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.31',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
]
headers={'User-Agent':random.choice(ua_list)} #随机生成协议头
url="https://book.douban.com/top250"
response=requests.get(url,headers=headers).content.decode('utf-8')
soup=BeautifulSoup(response,'html.parser') #bs4解析网页
divs=soup.find('div',class_="article").find_all('div',class_="pl2")
i=1
for div in divs[:10]: # 切片 获取前十本节点内容
    href=div.find('a')['href']
    print(href)
    book_response = requests.get(href, headers=headers).content.decode('utf-8') #访问书籍详情页
    book_soup = BeautifulSoup(book_response, 'html.parser')  # bs4解析网页
    h1=book_soup.find('div',id="wrapper").find('h1').get_text()  #获取标题
    h1=h1.replace('\n','')
    h1='Top%d:%s'%(i,h1)
    print(h1)
    comment_infos=''
    lis=book_soup.find('div',id="comment-list-wrapper").find('ul').find_all('li')
    for li in lis:
        author=li.find('span',class_="comment-info").find('a').get_text()
        conment=li.find('p',class_="comment-content").get_text()
        comment_info='%s%s%s%s%s%s'%('author:','\n',author,'\n','conment:',conment)
        print(comment_info)
        comment_infos='%s%s%s'%(comment_infos,'\n',comment_info)
    print(comment_infos)
    with open('top10_book.txt','a+',encoding='utf-8') as f:
        f.write('%s%s%s%s'%(h1,'\n',comment_infos,'\n'))
    i=i+1