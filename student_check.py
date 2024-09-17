### 학생 점호 버튼 클릭 api 

from flask import Blueprint, jsonify, request
from dbutil import create_db_connection
import logging

# 블루프린트 정의
student_check = Blueprint('student_check', __name__)

# 점호 체크 엔드포인트
@student_check.route('/student/check', methods=['POST'])
def check_attendance():
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

        # 학생의 현재 IN 값을 가져오기
        cursor.execute("SELECT `IN` FROM STUDENT WHERE STNUM = %s", (student_number,))
        result = cursor.fetchone()

        if result:
            # 현재 IN 값 가져오기
            current_in = result['IN']

            # IN 값을 1 증가
            new_in = current_in + 1

            # 업데이트 쿼리 실행
            cursor.execute("UPDATE STUDENT SET `IN` = %s WHERE STNUM = %s", (new_in, student_number))
            connection.commit()

            return jsonify({'message': f"Attendance checked for student {student_number}. IN updated to {new_in}."}), 200
        else:
            return jsonify({'error': 'Student not found'}), 404

    except Exception as e:
        logging.error(f"Error during attendance check: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()