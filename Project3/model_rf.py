"Project_APT"

import os
import json
# %pip install xmltodict
import xmltodict
import xml.etree.ElementTree as ET
import requests
from requests.models import parse_header_links
import csv
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pickle

#라이브러리 import
import numpy as np
import math
import urllib
import sklearn
from numpy import array
from sklearn.metrics import  mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

#!pip install category_encoders
from category_encoders import OneHotEncoder
from category_encoders import OrdinalEncoder
from category_encoders import TargetEncoder


#데이터 불러오기

#웹스크레이핑 - 법정동 코드 
CODE_URL = urlopen("https://inasie.github.io/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D/5/")
source = CODE_URL.read()
CODE_URL.close()
soup = BeautifulSoup(source, "lxml")
table = soup.find_all("table")
df_code = pd.read_html(str(table))[0]


#수도권(서울+경기) 법정동 코드 리스트로 변환
df_code_seoul = df_code[df_code['법정동주소'].str.contains("서울특별시")]
df_code_seoul = df_code_seoul.iloc[1: , :]
code_list = list(df_code_seoul['법정동코드'])

#데이터 수집
#API 호출
API_KEY = "SlBiRDZNAocdsplmITwGOE6xp2oaY4TJ5Dl%2BCtGHGkHni5uF09aIZiaml4KrIVxQzKca%2FAoDfhKjF5JJsXJCmQ%3D%3D"
deal_months = [202109, 202110, 202111]

#전국 데이터 수집을 위한 for loop(code_list - 전국 법정동 코드 리스트 사용)
df_list= []  
for deal_month in deal_months:
  for region_code in code_list:
    API_URL = f"http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?serviceKey={API_KEY}&pageNo=1&numOfRows=1000&LAWD_CD={region_code}&DEAL_YMD={deal_month}"
    try:
      #XML 데이터 추출 및 dict로 변환
      content = requests.get(API_URL).content
      dict_data = xmltodict.parse(content)
      #json 데이터로 변환
      json_str = json.dumps(dict_data['response']['body']['items']['item'], ensure_ascii=False)
      json_data = json.loads(json_str)
      #json df로 변환
      df_str = pd.read_json(json_str)
      df_tr = pd.DataFrame(df_str)
      df_list.append(df_tr)

    except:
      pass

#데이터 수집 완료
df_concat = pd.concat(df_list)

#법정동코드 숫자-> 지역이름으로 변경
df_code = df_code.rename(columns={"법정동코드": "도로명시군구코드"})
df = pd.merge(df_concat, df_code, how="left", on=["도로명시군구코드"])


#EDA
#df.profile_report()

#거래금액 object->int로 변경하기 위한 함수 설정
def toint(string):
  return int(string.replace(',',''))

#eda, feature engineering 함수
def fe(df):
  #건축년도 nan값 채우기
  df['건축년도'] = df['건축년도'].fillna(df['건축년도'].median()).astype(int)
  df['건축년도'] = df['건축년도'].apply(lambda x: "20년이상" if (2021-x) >= 20 else "20년미만" if (2021-x) >= 10 else "10년미만") 
  #거래유형 nan값 채우기
  df['거래유형'] = df['거래유형'].fillna('모르겠음')
  #브랜드아파트 피쳐 생성(10대 브랜드)
  df['브랜드'] = (df['아파트'].str.contains('힐스테이트|자이|푸르지오|더샵|래미안|롯데캐슬|아이파크|sk뷰|e편한세상|e-편한세상|위브|타워팰리스|하이페리온|더샵스타시티', case=False) == True) & (df['아파트'].str.contains("위브센티움") == False)
  #아파트 거래금액 int로 변경
  df['거래금액'] = df['거래금액'].apply(toint)
  #전용면적 평수로 변경
  df['전용면적'] = df['전용면적'] / 3.305785
  df['전용면적'] = df['전용면적'].apply(lambda x: "40평이상" if x >= 40 else "30평대" if x >= 30 else "20평대" if x >= 10 else "20평미만") 
  #column 삭제 및 이름변경
  df.drop(df.columns.difference(['법정동주소', '전용면적',  '거래유형', '건축년도', '거래금액', '브랜드']), 1, inplace=True)
  df['법정동주소'] = df['법정동주소'].str[5:]
  df = df.rename(columns = {'법정동주소': 'location1', '전용면적': 'size', '거래유형':'deal', '건축년도': 'old', '브랜드': 'brand', '거래금액':'price'}, inplace = False)
  
  return df

#train, test 세트 구분
train = df[(df['월'] <= 10)]
test = df[(df['월'] == 11)]

#feature engineering 진행
train = fe(train)
test = fe(test)

#features, target 지정
target = 'price'
features = ['location1', 'size', 'old', 'brand', 'deal']

#x, y(features, targe) 데이터셋 구분
X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]


#기준모델(y = average)
predict = y_train.mean()
y_pred = [predict] * len(y_train)

#기준모델 성능
print('*기준모델 성능')
print('mae :', mean_absolute_error(y_train, y_pred))
print('mse :', mean_squared_error(y_train, y_pred))
print('r2  :', r2_score(y_train, y_pred))

#모델3 - random forest regressor (target)
pipe = make_pipeline(
  OneHotEncoder(),
  RandomForestRegressor(max_depth=10, n_estimators=10))

k = 3

pipe.fit(X_train, y_train)
scores_mae = cross_val_score(pipe, X_train, y_train, cv=k, scoring='neg_mean_absolute_error')
scores_mse = cross_val_score(pipe, X_train, y_train, cv=k, scoring='neg_mean_squared_error')
scores_r2 = cross_val_score(pipe, X_train, y_train, cv=k, scoring='r2')

print(f'mae:', scores_mae)
print('평균 mae:', scores_mae.mean())
print(f'mse:', scores_mse)
print('평균 mse:', scores_mse.mean())
print(f'r2:', scores_r2)
print('평균 r2:', scores_r2.mean())

y_pred = pipe.predict(X_test)
print(f'mae:', mean_absolute_error(y_test, y_pred))
print(f'mse:', mean_squared_error(y_test, y_pred))
print(f'r2:', r2_score(y_test, y_pred))

    
"""
모델별 성능 정리

*기준모델 성능
mae : 54808.3249, mse : 6562291134.3478, r2  : 0.0

*머신러닝 모델(Target encdoing + random forest regressor) 성능
평균 mae: -24455.0327, 평균 mse: -1679679818.9626, 평균 r2: 0.761073

**테스트 데이터셋 결과
mae: 16644.3166,  mse: 913213197.9426, 
r2 score: 0.894668
"""

#pickle 저장
with open('model.pkl', 'wb') as pickle_file:
  pickle.dump(pipe, pickle_file)

with open('model.pkl','rb') as pickle_file:
    model = pickle.load(pickle_file)
    print(model)


#pickle 테스트
model.predict(X_test)
row = X_test.iloc[[2]]
model.predict(row)

row_dict = row.to_dict
row_dict_made = {"location1":"종로구", "size":"20평미만", "old":"20년이상", "brand":0, "deal":"직거래"}
df_dict_made = pd.DataFrame(data=row_dict_made, columns=['location1', 'size', 'old', 'brand', 'deal'], index = [1])
model.predict(df_dict_made)

#데이터 sqlite로 저장
import os
import sqlite3

DB_FILENAME = 'APT_API.db'
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
#sqlite3 연결
conn = sqlite3.connect(DB_FILENAME)
cur = conn.cursor()

#이미 있는 테이블 삭제
#cur.execute("DROP TABLE IF EXISTS apt_tuned;")

#df를 sqlite 파일로 export
df.to_sql('apt', conn, schema=None, index=True, index_label=None, chunksize=None, dtype=None)

#SQL데이터를 pandas df로 저장
sql_to_df = pd.read_sql_query("SELECT * FROM apt", conn)
sql_to_df = fe(sql_to_df)

#df를 sqlite 파일로 export(fe된 테이블)
#cur.execute("DROP TABLE IF EXISTS apt_tuned;")
sql_to_df.to_sql('apt_tuned', conn, schema=None, index=True, index_label=None, chunksize=None, dtype=None)


#postgresql에 저장
from sqlite3.dbapi2 import Connection
import psycopg2

sql_to_df = pd.read_sql_query("SELECT * FROM apt", conn)

sql_to_df.to_csv('C:/Users/senas/Desktop/CoderNANG/project/project3/apt_tuned.csv', sep=',') 

connection = psycopg2.connect(
    host="castor.db.elephantsql.com",
    database="zyshrsdm",
    user="zyshrsdm",
    password="vFqWmaUpghLDhdwVGFLSd3DsjMvNQWKb")
print(connection)

cur = connection.cursor()
cur.execute("""CREATE TABLE apt_tuned2 (id INT, location1 VARCHAR(50), old VARCHAR(50), size INT, brand INT, deal VARCHAR(50), PRIMARY KEY (id));""") 

with open('apt_tuned.csv'):
    print('')

connection.commit()

conn.commit()