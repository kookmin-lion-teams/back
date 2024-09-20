# 관리자 학생 리스트 조회
from flask import Blueprint, jsonify
from dbutil import create_db_connection
import logging

# 블루프린트 정의
admin_student_bp = Blueprint('admin_student', __name__)

# 학생 전체 목록 조회 엔드포인트 (AWAY 테이블과 JOIN하여 점호 미참석 횟수 포함)
@admin_student_bp.route('/admin/students', methods=['GET'])
def get_all_students():
    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        logging.error('Database connection failed.')
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # 학생 전체 목록 조회 쿼리 (AWAY 테이블과 JOIN하여 점호 미참석 횟수 계산)
        query = """
            SELECT STUDENT.*, COUNT(AWAY.AWAYID) AS away_count
            FROM STUDENT
            LEFT JOIN AWAY ON STUDENT.STNUM = AWAY.ASTNUM
            GROUP BY STUDENT.SID
        """
        cursor.execute(query)
        students = cursor.fetchall()

        # 학생 목록 반환
        return jsonify({'students': students}), 200

    except Exception as e:
        logging.error(f"Error retrieving students: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()