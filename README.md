# SketchDay-Backend
메인 웹 서버

## 프로젝트 개요
명지대학교 캡스톤디자인 프로젝트 - SketchDay (기록을 더 풍성하게, 그림 일기 서비스)
<img width="1080" alt="title" src="https://user-images.githubusercontent.com/69189272/233691909-1cab5b7e-ea80-42f3-84a8-e794a34a1350.png">

## 주요기능
- 일기 내용을 기반으로 적절한 그림 생성
- 메신저 스크린샷만으로 그림 일기 생성
  - 메신저 스크린샷에서 대화 내용을 파악

## 프로젝트 인원
총 4명 (Front-End 1명, Back-End 3명, ML 1명)

# Environment

|분류|이름|버전|
|:---|:---|:---|
|운영체제|ubuntu|22.04|
|운영체제|MacOS|13.2|
|Language|Python|3.9.2|
|DB|MySQL|5.7|
|Web|django|4.2|
||mysqlclient|2.1.1|
||djangorestframework|3.14.0|
||django-storages|1.13.2|
||boto3|1.26.114|
|ML|Pytorch|2.0.0|

# Directories
|디렉토리명|설명|
|:---|:---|
|account|계정 앱 관련 디렉토리|
|backend|메인 서버 앱 관련 디렉토리|
|diary|메인 일기 포스트 앱 관련 디렉토리|
|diaryImg|그림 일기 앱 관련 디렉토리|
|mypage|마이페이지 앱 관련 디렉토리|

# Service Architecture
<img width="1079" alt="workflow" src="https://user-images.githubusercontent.com/69189272/233691906-0b273fba-142c-4c27-aa65-67be3a693b1d.png">

