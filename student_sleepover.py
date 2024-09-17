# 학생 외박신청
from flask import Blueprint, jsonify, request
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging
from datetime import datetime

# 블루프린트 정의
student_sleepover_bp = Blueprint('student_sleepover', __name__)

# 외박 신청서 작성 엔드포인트
@student_sleepover_bp.route('/student/sleepover', methods=['POST'])
def create_sleepover_request():
    # 요청에서 데이터 가져오기
    student_number = request.json.get('sstnum')
    reason = request.json.get('reason')
    start_date = request.json.get('startdate')
    end_date = request.json.get('enddate')

    # 입력 값 유효성 검사
    if not student_number or not reason or not start_date or not end_date:
        return jsonify({'error': 'All fields are required: student number, reason, start date, end date'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # 신청서를 작성하는 현재 날짜
        application_date = datetime.now().date()

        # 외박 신청서 추가 쿼리 실행
        cursor.execute("""
            INSERT INTO SLEEPOVER (SSTNUM, REASON, ADATE, STARTDATE, ENDDATE, `CHECK`)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (student_number, reason, application_date, start_date, end_date, 0))
        
        connection.commit()

        return jsonify({'message': f"Sleepover request created for student {student_number}."}), 201

    except Exception as e:
        logging.error(f"Error while creating sleepover request: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()