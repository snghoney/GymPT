# GymPT

GymPT는 Flask로 제작된 웹 애플리케이션으로, 사용자의 운동 자세를 실시간으로 분석하고 불균형을 측정하여 저장하는 프로그램입니다. 사용자는 로그인하여 운동 데이터를 기록하고, 분석된 결과를 확인할 수 있습니다.

## 프로젝트 개요

GymPT는 다음과 같은 주요 기능을 제공합니다:
- 사용자가 로그인 및 로그아웃할 수 있습니다.
- 다양한 운동을 선택할 수 있습니다.
- Mediapipe를 사용하여 실시간으로 운동 자세를 분석합니다.
- 분석된 데이터를 데이터베이스에 저장하고, 결과를 시각화하여 제공합니다.

## 설치 방법

프로젝트를 로컬에서 실행하기 위해 다음 단계를 따르세요:

1. **프로젝트 클론**
    ```bash
    git clone <repository-url>
    cd gympt
    ```

2. **가상 환경 생성 및 활성화**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows에서는 venv\Scripts\activate
    ```

3. **필요한 패키지 설치**
    ```bash
    pip install -r requirements.txt
    ```

4. **환경 변수 설정**
    - `.env` 파일을 프로젝트 루트에 생성하고, 다음과 같은 환경 변수를 설정합니다:
      ```plaintext
      SECRET_KEY=your_secret_key
      SQLALCHEMY_DATABASE_URI=sqlite:///data.sqlite
      OPENAI_API_KEY=your_openai_api_key
      ```

5. **데이터베이스 초기화 및 마이그레이션**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6. **애플리케이션 실행**
    ```bash
    flask run
    ```

## 사용 방법

1. 웹 브라우저에서 `http://localhost:5000`에 접속합니다.
2. 회원 정보를 입력하여 로그인합니다.
3. 운동을 선택하고, 실시간 자세 분석을 시작합니다.
4. 운동 종료 후 결과를 확인하고 데이터베이스에 저장합니다.

## 기술 스택

- **Backend:** Flask, SQLAlchemy, Flask-Migrate
- **Frontend:** HTML, CSS, JavaScript
- **Realtime Pose Estimation:** Mediapipe
- **Database:** SQLite

## 파일 구조

```plaintext
gympt/
├── app.py                  # Flask 애플리케이션 설정 및 라우트 정의
├── config.py               # 설정 파일
├── requirements.txt        # 필요한 패키지 목록
├── migrations/             # 데이터베이스 마이그레이션 파일
├── templates/              # HTML 템플릿 파일
│   ├── index.html
│   ├── select.html
│   ├── exercise1.html
│   ├── exercise2.html
│   └── exercise3.html
├── static/                 # 정적 파일 (CSS, JS, 이미지)
│   ├── css/
│   ├── js/
│   └── images/
└── README.md               # 프로젝트 설명 파일
