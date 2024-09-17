# 관리자 외박 신청 승인/거부 

from flask import Blueprint, jsonify, request
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging

# 블루프린트 정의
admin_sleepover_approve_bp = Blueprint('admin_sleepover_approve', __name__)

# 외박 신청서 승인/미승인 처리 엔드포인트
@admin_sleepover_approve_bp.route('/admin/sleepover_approve/<int:request_id>', methods=['POST'])
def approve_sleepover_request(request_id):
    action = request.json.get('action')  # 'approve' 또는 'reject'

    # 입력 값 유효성 검사
    if not action:
        return jsonify({'error': 'Action is required'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()

        if action == 'approve':
            # 승인 처리: CHECK 값을 1로 업데이트
            cursor.execute("UPDATE SLEEPOVER SET `CHECK` = 1 WHERE SID = %s", (request_id,))
            message = 'Sleepover request approved.'
        elif action == 'reject':
            # 미승인 처리: 신청서 삭제
            cursor.execute("DELETE FROM SLEEPOVER WHERE SID = %s", (request_id,))
            message = 'Sleepover request rejected and deleted.'
        else:
            return jsonify({'error': 'Invalid action specified'}), 400

        connection.commit()
        return jsonify({'message': message}), 200

    except Exception as e:
        logging.error(f"Error while processing sleepover approval: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()