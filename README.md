# coinone-system-trading-simulator
This is system trading simulator V.0.0.0 using coinone API V2

### 프로젝트 목표
코인원에서 제공하는 API를 이용하여 system trading 시뮬레이션을 확인해보기 위한 프로젝트

### 프로그램 설명
- 코인원 ticker API를 이용해 시세 정보를 불러오고, 시세에 변화가 있을 때 마다 db에 저장
- fusioncharts 패키지를 이용하여 db에 저장된 시세 정보를 차트로 출력
- 코인원 Account_V2 - Balance API를 이용해 사용자의 계좌 정보를 불러오고, 사용자 세팅 가능
- 직접 매도/매수를 하지않고, 설정된 시나리오대로 매수/매도시 balance 변화를 log로 화면에 출력

### 컴파일 환경
- Python 2.7.14
- django 1.10.7

### 개념도
![coinone-system-trading-simulator 1](https://user-images.githubusercontent.com/12479160/37813954-eb2dd9b8-2eaa-11e8-813c-e120d0a0ce59.png)

### 활용 예제
- src 디렉토리 내의 png 파일 참조

### 주의 사항
- src 디렉토리 내의 codingTest와 codingTest_stack은 각각 프로그램의 주된 역할을 하는 프로젝트와 시세 정보를 불러오기만 하는 별개의 프로젝트로, 서버 구동시 포트 번호를 다르게 지정해줘야함 (e.g. localhost:8000, localhost:7000)
- 단, codingTest와 codingTest_stack의 db는 같은 파일을 사용하도록 각 프로젝트 폴더 내의 settings.py 파일에서 path 설정을 해줘야함
- Coinone에서 제공하는 access token과 secret key는 json 형태로 secrets.json 파일에 입력하여 codingTest 프로젝트의 manage.py 파일과 같은 위치에 저장시켜줘야함 (ACCESS_KEY, V2_SECRET_KEY)
