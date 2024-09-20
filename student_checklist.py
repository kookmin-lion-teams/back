# student_checklist.py
from flask import Blueprint, jsonify, request
from dbutil import create_db_connection
import logging
from datetime import datetime

# 블루프린트 정의
student_checklist_bp = Blueprint('student_checklist', __name__)

# 점호 내역 조회 엔드포인트
@student_checklist_bp.route('/student/checklist', methods=['POST'])
def get_checklist():
    # 요청에서 학번 가져오기 (로그인한 학생의 학번을 받아옴)
    student_number = request.json.get('stnum')

    # 입력 값 유효성 검사
    if not student_number:
        logging.error("Student number is required but not provided.")
        return jsonify({'error': 'Student number is required'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        logging.error("Database connection failed.")
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # 학생의 AWAY 및 IN 테이블에서 정보 가져오기
        query = """
        SELECT DATE, 'AWAY' AS STATUS, SEP
        FROM AWAY
        WHERE ASTNUM = %s
        UNION ALL
        SELECT DATE, 'IN' AS STATUS, SEP
        FROM `IN`
        WHERE ISTNUM = %s
        ORDER BY DATE
        """

        cursor.execute(query, (student_number, student_number))
        checklist = cursor.fetchall()

        # 반환할 결과 리스트
        result = []

        # 날짜와 요일을 분리하여 변환
        korean_weekdays = ['월', '화', '수', '목', '금', '토', '일']

        for entry in checklist:
            # 원본 날짜가 datetime.date 객체인 경우 처리
            if isinstance(entry['DATE'], datetime):
                date_obj = entry['DATE']
            else:
                # 원본 날짜가 문자열인 경우 datetime 객체로 변환
                date_obj = datetime.strptime(str(entry['DATE']), '%Y-%m-%d')

            # 변환된 날짜와 요일
            formatted_date = date_obj.strftime("%Y-%m-%d")  # 예: 2024-09-10
            formatted_day = korean_weekdays[date_obj.weekday()]  # 예: 화

            # 변환된 데이터를 result에 추가
            result.append({
                'date': formatted_date,
                'day': formatted_day,
                'status': entry['STATUS'],
                'sep': entry['SEP']
            })

        if not result:
            logging.error(f"No data found for student number: {student_number}")
            return jsonify({'error': 'No checklist data found for the student'}), 404

        return jsonify({'checklist': result}), 200

    except Exception as e:
        logging.error(f"Error retrieving checklist: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()