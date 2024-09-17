from flask import Blueprint, jsonify
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging
from datetime import datetime

# 블루프린트 정의
student_away_bp = Blueprint('student_away', __name__)

# 매주 화요일 오전 00:00에 실행되는 점호 초기화 함수
def reset_attendance():
    try:
        connection = create_db_connection()
        if connection is None:
            logging.error('Database connection failed during attendance reset.')
            return {'error': 'Database connection failed.'}, 500

        cursor = connection.cursor()
        cursor.execute("UPDATE STUDENT SET `IN` = 0")
        connection.commit()
        logging.info('Attendance reset successfully.')
        return {'message': 'Attendance reset successfully.'}, 200
    except Exception as e:
        logging.error(f"Error during attendance reset: {e}")
        return {'error': str(e)}, 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 매일 9시 10분에 실행되는 점호 불참 학생을 AWAY 테이블에 추가하는 함수
def mark_absent_students():
    connection = create_db_connection()
    if connection is None:
        logging.error('Database connection failed during absent mark.')
        return {'error': 'Database connection failed.'}, 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        # IN 값이 0인 학생 찾기
        cursor.execute("SELECT STNUM FROM STUDENT WHERE `IN` = 0")
        absent_students = cursor.fetchall()

        # 현재 날짜를 가져옴
        today = datetime.now().date()

        # IN 값이 0인 학생들을 AWAY 테이블에 추가
        for student in absent_students:
            stnum = student['STNUM']
            cursor.execute("INSERT INTO AWAY (ASTNUM, DATE) VALUES (%s, %s)", (stnum, today))

        connection.commit()
        logging.info('Absent students marked successfully.')
        return {'message': 'Absent students marked successfully.'}, 200

    except Exception as e:
        logging.error(f"Error while marking absent students: {e}")
        return {'error': str(e)}, 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 점호 불참자 목록 조회하는 엔드포인트
@student_away_bp.route('/get_absent_students', methods=['GET'])
def get_absent_students():
    try:
        connection = create_db_connection()
        if connection is None:
            logging.error('Database connection failed.')
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = connection.cursor(dictionary=True)
        
        # AWAY 테이블과 STUDENT 테이블을 JOIN하여 불참석 학생 목록 조회
        query = """
        SELECT 
            AWAY.AWAYID, AWAY.ASTNUM, AWAY.DATE,
            STUDENT.NAME, STUDENT.STNUM, STUDENT.DEPARTMENT, STUDENT.SEX,
            STUDENT.ROOM, STUDENT.SEATNUM, STUDENT.PHONE, STUDENT.SLEEPOVER,
            STUDENT.IN, STUDENT.MINUS
        FROM AWAY
        JOIN STUDENT ON AWAY.ASTNUM = STUDENT.STNUM
        """
        cursor.execute(query)
        absent_students_info = cursor.fetchall()

        return jsonify({'absent_students': absent_students_info}), 200

    except Exception as e:
        logging.error(f"Error fetching absent students: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()