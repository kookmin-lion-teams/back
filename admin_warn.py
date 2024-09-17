# 관리자 청소 상태 경고 api 
# 경고 2쌓이면 0으로 초기화 학생 테이블의 해당 학생 minus 컬럼 + 1(누적 경고 확인용)
from flask import Blueprint, jsonify, request
from dbutil import create_db_connection
import logging

# 블루프린트 정의
admin_warn_bp = Blueprint('admin_warn', __name__)

# 청소 상태 업데이트 엔드포인트 (경고 값 증가 및 처리)
@admin_warn_bp.route('/admin/update_warn', methods=['POST'])
def update_warn():
    # 요청에서 자리 번호와 방 번호를 가져옴
    seat_number = request.json.get('seat_number')
    room_number = request.json.get('room_number')

    # 디버깅 로그 추가
    logging.info(f"Warn update request received for room {room_number}, seat {seat_number}")

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        logging.error('Database connection failed.')
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # 경고 값 증가
        cursor.execute(
            """
            UPDATE CLEAN 
            SET WARN = WARN + 1 
            WHERE CROOM = %s AND CSEATUM = %s
            """, (room_number, seat_number)
        )
        connection.commit()

        # 현재 경고 값을 확인
        cursor.execute(
            """
            SELECT WARN 
            FROM CLEAN 
            WHERE CROOM = %s AND CSEATUM = %s
            """, (room_number, seat_number)
        )
        warn_status = cursor.fetchone()

        # 경고 값이 2 이상일 때 처리
        warn_value = warn_status['WARN']
        logging.info(f"Current warn value for room {room_number}, seat {seat_number}: {warn_value}")

        if warn_value >= 2:
            # CLEAN 테이블의 WARN을 0으로 초기화하고 STUDENT 테이블의 MINUS 값을 1 증가
            cursor.execute(
                """
                UPDATE CLEAN 
                SET WARN = 0 
                WHERE CROOM = %s AND CSEATUM = %s
                """, (room_number, seat_number)
            )
            cursor.execute(
                """
                UPDATE STUDENT 
                SET MINUS = MINUS + 1 
                WHERE ROOM = %s AND SEATNUM = %s
                """, (room_number, seat_number)
            )
            connection.commit()

        return jsonify({'message': 'Warn value updated successfully'}), 200

    except Exception as e:
        logging.error(f"Error updating warn value: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()