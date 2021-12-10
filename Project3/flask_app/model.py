
"Project_APT"

#데이터 불러오기(API CALL)
# Commented out IPython magic to ensure Python compatibility.
import os
import json
# %pip install xmltodict
import xmltodict
import xml.etree.ElementTree as ET
from flask import Flask, jsonify
import requests
from requests.models import parse_header_links
import csv
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

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
      df = pd.DataFrame(df_str)
      df_list.append(df)

    except:
      pass

#for loop으로 수집된 데이터프레임 리스트 확인
print(df_list)

#데이터 수집 완료
df = pd.concat(df_list)
print(df)

"""데이터 분석"""

# Commented out IPython magic to ensure Python compatibility.
# # 라이브러리 설치
# %%capture
# import sys
# 
# if 'google.colab' in sys.modules:
#     #Install packages in Colab
#     !pip install category_encoders==2.*
#     !pip install eli5
#     !pip install pandas-profiling==2.*
#     !pip install pdpbox
#     !pip install shap

#라이브러리 import
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import math
import urllib
import sklearn
import xgboost
import shap

from numpy import linalg as LA
from numpy import array
from numpy.linalg import norm

from scipy import stats
from scipy.spatial import distance

from sklearn.linear_model import LinearRegression
from sklearn.metrics import  mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import f_regression, SelectKBest
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_regression, SelectKBest
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

#!pip install category_encoders
from category_encoders import OneHotEncoder
from category_encoders import OrdinalEncoder
from category_encoders import TargetEncoder

from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None 

"""##EDA"""

df = df_keep

#df 살펴보기
import pandas_profiling
from pandas_profiling import ProfileReport
df.profile_report()

#법정동코드 숫자-> 지역이름으로 변경
df_code = df_code.rename(columns={"법정동코드": "도로명시군구코드"})
df = pd.merge(df, df_code, how="left", on=["도로명시군구코드"])

#거래금액 object->int로 변경하기 위한 함수 설정
def toint(string):
  return int(string.replace(',',''))


#eda, feature engineering 함수
def fe(df):
  #건축년도 nan값 채우기
  df['건축년도'] = df['건축년도'].fillna(df['건축년도'].median()).astype(int)
  #거래유형 nan값 채우기
  df['거래유형'] = df['거래유형'].fillna('모르겠음')
  #브랜드아파트 피쳐 생성(10대 브랜드)
  df['브랜드'] = (df['아파트'].str.contains('힐스테이트|자이|푸르지오|더샵|래미안|롯데캐슬|아이파크|sk뷰|e편한세상|e-편한세상|위브|타워팰리스|하이페리온|더샵스타시티', case=False) == True) & (df['아파트'].str.contains("위브센티움") == False)
  #아파트 거래금액 int로 변경
  df['거래금액'] = df['거래금액'].apply(toint)
  #column 삭제
  df.drop(df.columns.difference(['월', '일', '도로명시군구코드', '법정동', '건축년도', '전용면적',  '아파트', '거래유형', '거래금액', '브랜드']), 1, inplace=True)
  
  return df


#train, test 세트 구분
train = df[(df['월'] <= 10)]
test = df[(df['월'] == 11)]

#feature engineering 진행
fe(train)
fe(test)

#features, target 지정
features = ['월', '일','도로명시군구코드', '법정동', '건축년도', '전용면적',  '브랜드', '거래유형']
target = '거래금액'

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
     TargetEncoder(smoothing=10), 
     SimpleImputer(), 
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

#테스트 데이터셋 테스트 결과
print('r2 score:', pipe.score(X_test, y_test))
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



#데이터 저장
import os
import sqlite3

DB_FILENAME = 'APT.db'
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)

conn = sqlite3.connect(DB_FILENAME)
cur = conn.cursor()

cur.execute("""CREATE TABLE apt(
	No INT NOT NULL, 
	거래유형 NVARCHAR(10), 
	건축년도 NVARCHAR(10),
  도로명시군구코드 NVARCHAR(10),
  법정동 NVARCHAR(10),
  아파트 NVARCHAR(30),
  월 INT NOT NULL,
  일 INT NOT NULL,
  전용면적 FOLAT NOT NULL,
  브랜드 INT NOT NULL,
 	CONSTRAINT apt_PK PRIMARY KEY (index));""")



