import mysql.connector
from mysql.connector import Error
import logging
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

# 환경 변수 로드
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# 환경 변수 출력하여 확인
print(f"DB_HOST: {db_host}, DB_NAME: {db_name}, DB_USER: {db_user}, DB_PASSWORD: {db_password}")

def create_db_connection():
    """데이터베이스 연결을 생성하는 함수"""
    try:
        logging.debug("Connecting to MySQL database...")
        # MySQL 연결 설정 (포트 명시적 설정)
        connection = mysql.connector.connect(
            host=db_host,
            port=3306,  # 포트 번호 명시적 설정
            database=db_name,
            user=db_user,
            password=db_password
        )
        logging.debug("Connection established")
        print("Connection established")
        return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL database: {e}")
        print(f"Error connecting to MySQL database: {e}")
        return None