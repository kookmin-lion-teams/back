# 학생 로그인 
from flask import Blueprint, jsonify, request
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging  # logging 모듈 임포트

# 블루프린트 정의
student_login = Blueprint('student_login', __name__)

# 학생 로그인 엔드포인트
@student_login.route('/student/login', methods=['POST'])
def login():
    # 요청에서 이름과 학번 가져오기
    student_name = request.json.get('name')
    student_number = request.json.get('stnum')

    # 입력 값 유효성 검사
    if not student_name or not student_number:
        return jsonify({'error': 'Name and student number are required'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        # 학생의 이름과 학번이 일치하는 정보를 조회
        cursor.execute("SELECT * FROM STUDENT WHERE NAME = %s AND STNUM = %s", (student_name, student_number))
        student = cursor.fetchone()  # 일치하는 첫 번째 학생 데이터 가져오기

        # 쿼리 결과 확인용 로그
        logging.debug(f"Query result: {student}")

        # 학생 정보가 일치하는지 확인
        if student:
            return jsonify({'student_info': student}), 200
        else:
            return jsonify({'error': 'Invalid name or student number'}), 404
    except Exception as e:
        logging.error(f"Error during student login: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()