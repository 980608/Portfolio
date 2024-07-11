간단한 프로젝트를 진행(4.12~13)
나이브베이징을 사용하여 분석을 해보자
from pandas import Series,DataFrame
import pandas as pd
import datetime
import time
import re
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from urllib.error import URLError, HTTPError
from fake_useragent import UserAgent
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from konlpy.tag import Okt
import operator
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter
네이버 영화 장르 분석


url = 'https://movie.naver.com/movie/sdb/browsing/bmovie_genre.naver'
driver =  webdriver.Chrome('c:/data/chromedriver.exe')
driver.get(url)
driver.implicitly_wait(2)

movie = DataFrame(columns=['name','genre','text'])
failed_url = []

# 판타지 / 공포
for i in range(2,5,2):
    driver.find_element(By.CSS_SELECTOR,'table.directory_item_other > tbody > tr:nth-of-type(1) > td:nth-of-type('+str(i)+') > a').click() # 장르 선택
    
    for u in range(2,7): # 페이지 이동 for문
        for j in range(1,21): # 자료 수집 for문     
            try:
                driver.find_element(By.CSS_SELECTOR,'ul.directory_list > li:nth-of-type('+str(j)+') > a').click() # 제목클릭
                html = driver.page_source
                soup = bs(html,'html.parser')
                time.sleep(2)
                name = soup.select_one('h3.h_movie > a').text # 제목
                genre = soup.select_one('dl.info_spec > dd > p > span > a:nth-of-type(1)').text # 장르
                text = soup.select_one('p.con_tx').text # 줄거리
                movie = movie.append({'name' : name,'genre':genre,'text':text},ignore_index = True)
                time.sleep(2)
                driver.back() # 뒤로가기
                time.sleep(2)
                
            except:
                failed_url.append(i) # 오류 페이지 저장
                driver.back()
        
        if u == 2:
            driver.find_element(By.CSS_SELECTOR,'div.pagenavigation > table > tbody > tr > td:nth-of-type('+str(u)+') > a').click()
        else:
            driver.find_element(By.CSS_SELECTOR,'div.pagenavigation > table > tbody > tr > td:nth-of-type('+str(u+1)+') > a').click()

    driver.find_element(By.CSS_SELECTOR,'div.tab_type_6 > ul > li:nth-of-type(4)').click() # 장르 페이지로 가기
    time.sleep(2)


movie.to_csv('c:/data/movie_1.csv',index=False)
movie_1 = pd.read_csv('c:/data/movie_1.csv')

# 멜로, 스릴
for i in range(1,4,2):
    driver.find_element(By.CSS_SELECTOR,'table.directory_item_other > tbody > tr:nth-of-type(2) > td:nth-of-type('+str(i)+') > a').click() # 장르 선택
    
    for u in range(2,7): # 페이지 이동 for문
        for j in range(1,21): # 자료 수집 for문     
            try:
                driver.find_element(By.CSS_SELECTOR,'ul.directory_list > li:nth-of-type('+str(j)+') > a').click() # 제목클릭
                html = driver.page_source
                soup = bs(html,'html.parser')
                time.sleep(2)
                name = soup.select_one('h3.h_movie > a').text # 제목
                genre = soup.select_one('dl.info_spec > dd > p > span > a:nth-of-type(1)').text # 장르
                text = soup.select_one('p.con_tx').text # 줄거리
                movie_1 = movie_1.append({'name' : name,'genre':genre,'text':text},ignore_index = True)
                time.sleep(2)
                driver.back() # 뒤로가기
                time.sleep(2)
                
            except:
                failed_url.append(i) # 오류 페이지 저장
                driver.back()
        
        if u == 2:
            driver.find_element(By.CSS_SELECTOR,'div.pagenavigation > table > tbody > tr > td:nth-of-type('+str(u)+') > a').click()
        else:
            driver.find_element(By.CSS_SELECTOR,'div.pagenavigation > table > tbody > tr > td:nth-of-type('+str(u+1)+') > a').click()


    #driver.find_element(By.CSS_SELECTOR,'ul.navi_sub > li:nth-of-type(2) > a').click()
    driver.find_element(By.CSS_SELECTOR,'div.tab_type_6 > ul > li:nth-of-type(4)').click() # 장르 페이지로 가기
    time.sleep(2)


# 다큐멘터리, 가족
for i in range(2,5,2):
    driver.find_element(By.CSS_SELECTOR,'table.directory_item_other > tbody > tr:nth-of-type(3) > td:nth-of-type('+str(i)+') > a').click() # 장르 선택
    
    for u in range(2,7): # 페이지 이동 for문
        for j in range(1,21): # 자료 수집 for문     
            try:
                driver.find_element(By.CSS_SELECTOR,'ul.directory_list > li:nth-of-type('+str(j)+') > a').click() # 제목클릭
                html = driver.page_source
                soup = bs(html,'html.parser')
                time.sleep(2)
                name = soup.select_one('h3.h_movie > a').text # 제목
                genre = soup.select_one('dl.info_spec > dd > p > span > a:nth-of-type(1)').text # 장르
                text = soup.select_one('p.con_tx').text # 줄거리
                movie_1 = movie_1.append({'name' : name,'genre':genre,'text':text},ignore_index = True)
                time.sleep(2)
                driver.back() # 뒤로가기
                time.sleep(2)
                
            except:
                failed_url.append(i) # 오류 페이지 저장
                driver.back()
        
        if u == 2:
            driver.find_element(By.CSS_SELECTOR,'div.pagenavigation > table > tbody > tr > td:nth-of-type('+str(u)+') > a').click()
        else:
            driver.find_element(By.CSS_SELECTOR,'div.pagenavigation > table > tbody > tr > td:nth-of-type('+str(u+1)+') > a').click()


    #driver.find_element(By.CSS_SELECTOR,'ul.navi_sub > li:nth-of-type(2) > a').click()
    driver.find_element(By.CSS_SELECTOR,'div.tab_type_6 > ul > li:nth-of-type(4)').click() # 장르 페이지로 가기
    time.sleep(2)

movie_1.to_csv('c:/data/naver_movie.csv',index=False)
movie = pd.read_csv('c:/data/naver_movie.csv')

movie[movie['text'].isnull() != False]
movie = movie.drop(305, axis=0)
movie.to_csv('c:/data/naver_movie.csv',index=False)
movie = pd.read_csv('c:/data/naver_movie.csv')


# 1차 전처리 작업
movie['text'][0]
re.findall('\d+\w',movie['text'][0])

re.sub('\(\w+\)',' ',movie['text'][0])

movie['text'] = movie['text'].apply(lambda x : re.sub('\xa0',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('\n|\t+',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('\{“I Think, Therefore I am \(나는 생각한다, 고로 존재한다\)” - Descartes \(데가르트\), 1596-1650\}',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('\s{2,}',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('\(.+?\)',' ',x))
movie['text'] = movie['text'].apply(lambda x : x.strip())
movie['text'] = movie['text'].apply(lambda x : re.sub('\(.+?\)',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('[,‘’.]',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('\d+\w',' ',x))

movie.to_csv('c:/data/text_movie.csv',index=False)
movie = pd.read_csv('c:/data/text_movie.csv')

movie['text'][21]
re.findall("['|']",movie['text'][8])

re.sub('[""]','',movie['text'][13])

movie['text'] = movie['text'].apply(lambda x : re.sub('\[.+?\]',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('\s{2,}',' ',x))
movie['text'] = movie['text'].apply(lambda x : x.strip())
movie['text'] = movie['text'].apply(lambda x : re.sub('…',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('[”|-|?|<|>|!]',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('MEM:',' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub("['|']",' ',x))
movie['text'] = movie['text'].apply(lambda x : re.sub('[""]','',x))



okt_pos(movie_1['text'][0])


okt = Okt()

def okt_pos(arg):
    token_cpr = []
    for i in okt.pos(arg):
        if i[1] in ['Noun','Adjective']:
            token_cpr.append(i[0])
    token_cpr = [j for j in token_cpr if len(j) >= 2]
    return token_cpr
tokenizer = okt_pos

x_train,x_test,y_train,y_test= train_test_split(movie['text'],movie['genre'],test_size = 0.2)

cv = CountVectorizer(tokenizer = okt_pos)
cv = CountVectorizer(ngram_range=(2,2))
x_train = cv.fit_transform(x_train)
cv.get_feature_names()
x_train.toarray()

x_test = cv.transform(x_test)
x_test.toarray()

nb = MultinomialNB()
nb.fit(x_train,y_train)

y_predict = nb.predict(x_test)
accuracy_score(y_test,y_predict)

■ 혼동행렬(confusion matrix)
from sklearn.metrics import confusion_matrix, classification_report
confusion_matrix(y_test,y_predict)
print(classification_report(y_test,y_predict))

































































































































































































































































































































































































































































































































































