
# 관리자 청소기록 및 청소 학생 목록 조회
from flask import Blueprint, jsonify, request
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging

# 블루프린트 정의
admin_clean_bp = Blueprint('admin_clean', __name__)

# 전체 청소 목록 조회하는 엔드포인트
@admin_clean_bp.route('/admin/clean_list', methods=['GET'])
def get_clean_list():
    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        logging.error('Database connection failed.')
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        # CLEAN 테이블과 STUDENT 테이블을 JOIN하여 데이터 조회
        query = """
        SELECT 
            CLEAN.CID, CLEAN.CSEATUM, CLEAN.CROOM, CLEAN.WARN,
            STUDENT.SID, STUDENT.NAME, STUDENT.STNUM, STUDENT.DEPARTMENT, 
            STUDENT.SEX, STUDENT.ROOM, STUDENT.SEATNUM, STUDENT.PHONE, 
            STUDENT.SLEEPOVER, STUDENT.IN, STUDENT.MINUS
        FROM CLEAN
        JOIN STUDENT ON CLEAN.CROOM = STUDENT.ROOM AND CLEAN.CSEATUM = STUDENT.SEATNUM
        """
        cursor.execute(query)
        clean_student_list = cursor.fetchall()

        # 조회된 데이터를 JSON 형식으로 반환
        return jsonify(clean_student_list), 200

    except Exception as e:
        logging.error(f"Error fetching clean list: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()