# 부트캠프(코드스테이츠) 프로젝트 모음
아래는 제가 부트캠프 과정(7개월)동안 진행한 ML/DL 개인 프로젝트 5개의 모음입니다. <br> 
각 프로젝트 제목에서 [ ] 안의 문자가 폴더명입니다. <br> <br>
이미지 위주로 보시려면 아래 링크의 포트폴리오를 봐주시면 감사하겠습니다. <br> 
https://www.notion.so/SENA-3659604b8ae44077b3ee313a0d120495 <br><br>

## [DL_CNN,DCGAN] CNN, DCGAN 인테리어 이미지 분류 및 생성 프로젝트
- **프로젝트 주제**
    - 컴퓨터 비전 딥러닝 기술인 CNN, DCGAN을 통해인테리어 이미지를 효율적으로 분류
    - 가상 인테리어 이미지 생성을 통해 고객의 취향에 맞는 새로운 인테리어 제안
    
- **프로젝트 개요**
    - 웹스크레이핑으로 컨셉별 인테리어 이미지 수집
    - CNN 모델로 수집된 인테리어 이미지 컨셉별 분류
    - DCGAN 모델을 활용하여 특정 컨셉의 가상 인테리어 이미지 생성

- **프로젝트 결과**
    - CNN 이미지 분류결과: Accuracy 0.9398
- **데이터**
  - 웹스크레이핑을 통해 검색싸이트(www.bing.com) 이미지 수집
- **코드 참고**
  - 이미지 수집 
    - 채널명: 동빈나
    - 링크: https://www.youtube.com/embed/Lu93Ah2h9XA 
  - 이미지 분류 
    - 웹사이트명: 텐서플로우 공식문서
    -  링크: https://www.tensorflow.org/tutorials/images/classification
  - 이미지 생성 
    - 웹사이트명: 케라스 공식문서
    - 링크: https://keras.io/examples/generative/dcgan_overriding_train_step/
<br><br><br><br>

## [DL_CycleGAN] CycleGAN 인테리어 이미지 변형 프로젝트
- **프로젝트 주제**
    - 기존의 인테리어 이미지를 다른 컨셉으로 변형
    - 고객의 기존 인테리어를 원하는 새로운 컨셉으로 변화시킬 수 있도록 제안

- **프로젝트 개요**
    - 웹스크레이핑으로 컨셉별 인테리어 이미지 수집
    - CycleGAN 모델을 사용하여 인테리어 이미지 컨셉 변형
        - 북유럽 스타일 인테리어 이미지를 한옥 스타일로 변형
        
- **데이터**
  - 웹스크레이핑을 통해 검색싸이트(www.bing.com) 이미지 수집
- **코드 참고**
  - 이미지 수집 
    - 채널명: 동빈나 
    - 링크: https://www.youtube.com/embed/Lu93Ah2h9XA 
  - 이미지 분류 
    - 웹사이트명: 텐서플로우 공식문서 
    - 링크: https://www.tensorflow.org/tutorials/generative/cyclegan?hl=ko
<br><br><br><br>

## [ML_apt_web_app] 아파트 매매가 예측 웹어플리케이션 개발 프로젝트
- **프로젝트 주제**
    - 서울에서 아파트를 매매하고자 하는 고객에게 지역, 면적 등 아파트의 특성에 따라 예측 매매가를 제공하는 서비스 개발
    
- **프로젝트 개요**
    - 서울시 아파트 매매가 예측 웹 어플리케이션 개발
    - 머신러닝 기술을 사용한 서울시 매매가 예측 알고리즘
    - FLASK를 활용한 웹 어플리케이션 제작
    - METABASE를 활용한 대시보드 제작
    - SQL로 input 데이터 연동
    
- **데이터**
  - 공공데이터포털 서울특별시_동별 아파트 매매거래 현황 (https://www.data.go.kr/data/15081037/fileData.do)

- **코드참고**
  - 채널명: Tech With Tim 
  - 링크: https://youtu.be/dam0GPOAvVI
<br><br><br><br>

## [ML_sephora_website_sales] 화장품 웹싸이트 평점 분석 프로젝트
- **프로젝트 주제**
    - 화장품 회사(세포라) 웹싸이트에서 판매된 화장품들의 특징에 따라 평점 예측, 어떤 요인에 의해 평점이 도출되는지 분석

- **프로젝트 개요**
    - 세포라 웹싸이트 화장품 평점 분석
    - 제품 특징에 따른 높은 평점(추천제품) 예측
    - 평점에 영향을 끼치는 요인 분석 (PDP)
- **프로젝트 결과**
  - Accuracy: 0.511 → 0.646
    
- **데이터** 
  - 캐글 Sephora Website (https://www.kaggle.com/raghadalharbi/all-products-available-on-sephora-website)
<br><br><br><br>



## ML_video_game_sales
- 주제: 통계분석을 통한 지역별 비디오게임 판매량 비교분석
- 데이터: 코드스테이츠 제공 
<br><br>


