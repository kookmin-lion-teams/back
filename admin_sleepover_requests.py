# 관리자 외박 신청 내역 목록 조회
from flask import Blueprint, jsonify
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging

# 블루프린트 정의
admin_sleepover_requests_bp = Blueprint('admin_sleepover_requests', __name__)

# 외박 신청서 목록 조회 엔드포인트
@admin_sleepover_requests_bp.route('/admin/sleepover_requests', methods=['GET'])
def get_sleepover_requests():
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        # SLEEPOVER 테이블과 STUDENT 테이블을 JOIN하여 모든 외박 신청서 목록 조회 쿼리
        query = """
        SELECT 
            SLEEPOVER.*, 
            STUDENT.NAME, STUDENT.STNUM, STUDENT.DEPARTMENT, STUDENT.SEX,
            STUDENT.ROOM, STUDENT.SEATNUM, STUDENT.PHONE, STUDENT.SLEEPOVER AS STUDENT_SLEEPOVER,
            STUDENT.IN, STUDENT.MINUS
        FROM SLEEPOVER
        JOIN STUDENT ON SLEEPOVER.SSTNUM = STUDENT.STNUM
        """
        cursor.execute(query)
        requests = cursor.fetchall()

        return jsonify({'requests': requests}), 200

    except Exception as e:
        logging.error(f"Error while fetching sleepover requests: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
