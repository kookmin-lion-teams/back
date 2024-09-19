# 관리자 외박 신청 승인/거부 
from flask import Blueprint, jsonify, request
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging

# 블루프린트 정의
admin_sleepover_approve_bp = Blueprint('admin_sleepover_approve', __name__)

# 외박 신청서 승인/미승인 처리 엔드포인트
@admin_sleepover_approve_bp.route('/admin/sleepover_approve', methods=['POST'])
def approve_sleepover_request():
    # 요청 데이터에서 SID 가져오기
    request_id = request.json.get('sid')  # 외박 신청 ID

    # 입력 값 유효성 검사
    if not request_id:
        return jsonify({'error': 'SID is required'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()

        # 승인 처리: SID에 해당하는 외박 신청의 CHECK 값을 1로 업데이트
        cursor.execute(
            "UPDATE SLEEPOVER SET `CHECK` = 1 WHERE SID = %s",
            (request_id,)
        )

        # 승인된 외박 신청서의 SSTNUM(학생 학번) 가져오기
        cursor.execute(
            "SELECT SSTNUM FROM SLEEPOVER WHERE SID = %s",
            (request_id,)
        )
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'Student not found for given SID'}), 404

        student_number = result[0]

        # 해당 학생의 SLEEPCOUNT 값 증가
        cursor.execute(
            "UPDATE STUDENT SET SLEEPCOUNT = SLEEPCOUNT + 1 WHERE STNUM = %s",
            (student_number,)
        )

        connection.commit()
        message = 'Sleepover request approved and student sleep count updated.'

        return jsonify({'message': message}), 200

    except Exception as e:
        logging.error(f"Error while processing sleepover approval: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()