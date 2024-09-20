# 관리자 외박 신청 거부
from flask import Blueprint, jsonify, request
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging

# 블루프린트 정의
admin_sleepover_reject_bp = Blueprint('admin_sleepover_reject', __name__)

# 외박 신청서 거부 엔드포인트
@admin_sleepover_reject_bp.route('/admin/sleepover_reject', methods=['POST'])
def reject_sleepover_request():
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

        # 거부 처리: SID에 해당하는 외박 신청서 삭제
        cursor.execute(
            "DELETE FROM SLEEPOVER WHERE SID = %s",
            (request_id,)
        )

        connection.commit()
        message = 'Sleepover request rejected and deleted from the database.'

        return jsonify({'message': message}), 200

    except Exception as e:
        logging.error(f"Error while processing sleepover rejection: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()