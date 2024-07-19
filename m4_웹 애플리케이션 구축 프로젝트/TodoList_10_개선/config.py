import os

# 현재 파일의 절대 경로를 기반으로 basedir 변수를 설정. 이 변수는 프로젝트의 기본 디렉터리를 나타낸다.
# os.path.abspath(path): 주어진 경로 path의 절대 경로를 반환
# __file__ 의 디렉토리 부분만을 추출. C:\kita240424\workspace\m4_웹 애플리케이션 구축 프로젝트\TodoList_10
basedir = os.path.abspath(os.path.dirname(__file__))
# Flask configuration
# 세션 데이터 암호화, CSRF 보호 등을 위해 사용

class Config:
    SECRET_KEY = '09d26bba5aff12ec002bdbd3234a24d03ce1436c56987b3a'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://hyunjin:Monster98!@localhost:3306/hyunjin_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_FILES_DEST = os.path.join(basedir, 'uploads')
