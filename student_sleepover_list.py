# 학생 본인의 외박 신청 내역 조회 

from flask import Blueprint, jsonify, request
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging
from datetime import datetime  # 현재 날짜와 시간을 가져오기 위해 사용

# 블루프린트 정의
student_sleepover_list_bp = Blueprint('student_sleepover_list', __name__)

# 학생 본인의 외박 신청 내역 조회 엔드포인트
@student_sleepover_list_bp.route('/student/sleepover_list', methods=['POST'])
def get_student_sleepover_list():
    # 요청 데이터에서 학번 가져오기
    student_number = request.json.get('sstnum')  # 학생 학번

    # 입력 값 유효성 검사
    if not student_number:
        return jsonify({'error': 'Student number (sstnum) is required'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # 학생의 외박 신청 내역 조회 쿼리
        query = """
        SELECT 
            SID, SSTNUM, REASON, ADATE, STARTDATE, ENDDATE, `CHECK`
        FROM SLEEPOVER
        WHERE SSTNUM = %s
        ORDER BY ADATE DESC
        """
        cursor.execute(query, (student_number,))
        sleepover_list = cursor.fetchall()

        # 반환할 결과 리스트
        result = []

        # 날짜와 요일을 분리하여 변환
        korean_weekdays = ['월', '화', '수', '목', '금', '토', '일']

        for entry in sleepover_list:
            # original_date가 datetime.date 형식이므로 str로 변환
            original_date = entry['ADATE']
            
            # 변환된 날짜와 요일
            formatted_date = original_date.strftime("%Y-%m-%d")  # 예: 2024-09-10
            formatted_day = korean_weekdays[original_date.weekday()]  # 예: 화

            # 변환된 데이터를 result에 추가
            result.append({
                'SID': entry['SID'],
                'SSTNUM': entry['SSTNUM'],
                'REASON': entry['REASON'],
                'ADATE': f"{formatted_date}({formatted_day})",
                'STARTDATE': entry['STARTDATE'].strftime("%Y-%m-%d") if entry['STARTDATE'] else None,
                'ENDDATE': entry['ENDDATE'].strftime("%Y-%m-%d") if entry['ENDDATE'] else None,
                'CHECK': entry['CHECK']
            })

        return jsonify({'sleepover_list': result}), 200

    except Exception as e:
        logging.error(f"Error retrieving sleepover list: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()