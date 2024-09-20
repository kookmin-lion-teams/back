# student_check.py
from flask import Blueprint, jsonify, request
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging  # logging 모듈 임포트
from datetime import datetime  # 현재 날짜와 시간을 가져오기 위해 사용

# 블루프린트 정의
student_check_bp = Blueprint('student_check', __name__)

# 학생 출석 체크 엔드포인트
@student_check_bp.route('/student/check_in', methods=['POST'])
def check_in():
    # 요청에서 학번 가져오기
    student_number = request.json.get('stnum')

    # 입력 값 유효성 검사
    if not student_number:
        return jsonify({'error': 'Student number is required'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # 현재 날짜 가져오기
        today_date = datetime.now().date()

        # 학생의 출석을 IN 테이블에 기록
        cursor.execute("INSERT INTO `IN` (ISTNUM, DATE, SEP) VALUES (%s, %s, %s)", 
                       (student_number, today_date, 1))
        
        # STUDENT 테이블에서 해당 학생의 IN 값을 1 증가
        cursor.execute("UPDATE STUDENT SET `IN` = `IN` + 1 WHERE STNUM = %s", (student_number,))
        
        connection.commit()

        return jsonify({'message': f"Attendance checked for student {student_number}. Recorded in IN table and updated STUDENT table."}), 200

    except Exception as e:
        logging.error(f"Error during attendance check-in: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()