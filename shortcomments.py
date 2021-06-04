# coding:utf-8
import requests
from bs4 import BeautifulSoup
import pandas
import os
import jieba
from wordcloud import WordCloud
import numpy
from PIL import Image

def CrawlShortComments():
    #爬取豆瓣电影短评信息，提取用户名和评论，保存为字典格式。默认爬取前500条短评。
    container={'users':[],'comments':[]}
    for StartItemNumber in range(0,500,20):
        try:
            #完整url示例https://movie.douban.com/subject/26322774/comments?start=0&limit=20&status=P&sort=new_score
            url = 'https://movie.douban.com/subject/33454993/comments'
            HttpHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
            UrlParams = {'start':StartItemNumber,'limit':'20','status':'P','sort':'new_score'}
            Response = requests.get(url,params=UrlParams,headers=HttpHeaders)
            soup = BeautifulSoup(Response.text,'html.parser')
            with open(os.getcwd()+'\\response.html','w',encoding='utf-8') as f:
                f.write(Response.text)
            # print(soup)
            for user in soup.find_all('a',title=True):
                #print(user.get('title'))
                container['users'].append(user.get('title'))
            for comment in soup.find_all('span',class_='short'):
                #print(comment.string)
                container['comments'].append(comment.string)
        except Exception as e:
            print('Error!')
            print(e)
    return container
def SaveData(d):
    # 利用pandas保存完整短评信息为csv格式并存储在当前目录
    CommentsPandas = pandas.DataFrame(d)
    CurrentDir = os.getcwd()
    CommentsPandas.to_csv(CurrentDir + '\\doubancomments.csv', encoding='utf_8_sig')
def CutWords():
    #利用分词库jieba对评论进行分词，并利用停用词库过滤掉无意义的词
    df = pandas.read_csv("doubancomments.csv")
    RowsNumber = df.shape[0]-1
    for i in range(0,RowsNumber):
        value = df.loc[i,'comments']
        with open(os.getcwd()+'\\comments.txt','a',encoding='utf-8') as f:
            f.write(value)
    with open(os.getcwd()+'\\comments.txt', 'r', encoding='utf-8') as f:
        comments = f.read()
    with open(os.getcwd()+'\\stop.txt',encoding='utf-8') as stopf:
        StopWords = stopf.read().splitlines()
    words = []
        # 过滤无意义的词语
    for word in jieba.cut(comments):
        if word not in StopWords:
            words.append(word)
    words = ' '.join(words)
    return(words)
def GenerateWordCloud(cword):
    #制作词云
    word_cloud = WordCloud(
        background_color='white',
        font_path=os.getcwd()+'\\pingfang.ttf',  # 显示中文
        mask=numpy.array(Image.open(os.getcwd()+'\\kenan.jpg')),
        max_font_size=100
    )
    word_cloud.generate(cword)
    word_cloud.to_image().show()
    word_cloud.to_file('kenanwordcloud.jpg')


if __name__ == '__main__':
   Data = CrawlShortComments()
   SaveData(Data)
   cutedword = CutWords()
   GenerateWordCloud(cutedword)