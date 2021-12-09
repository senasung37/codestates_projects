
#데이터 불러오기(API CALL)

import os
import json
#%pip install xmltodict
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
df_code

#수도권(서울+경기) 법정동 코드 리스트로 변환
df_code_seoul = df_code[df_code['법정동주소'].str.contains("서울특별시")]
df_code_seoul = df_code_seoul.iloc[1: , :]
code_list = list(df_code_seoul['법정동코드'])
code_list

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
df_list

#데이터 수집 완료
df = pd.concat(df_list)
df



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

from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None  # default='warn'
import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning, module='xgboost')

##EDA

df_keep = df

#features, target 구분
features = ['월', '일', '법정동', '건축년도', '전용면적',  '아파트', '거래유형', '중개사소재지']
target = ['거래금액']


