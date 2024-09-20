from flask import Blueprint, request, jsonify
from dbutil import create_db_connection
import logging
from datetime import datetime

# 블루프린트 정의
student_clean_bp = Blueprint('student_clean', __name__)

# 사진 업로드 엔드포인트 (BLOB 데이터베이스 저장용)
@student_clean_bp.route('/student/upload_clean_photos', methods=['POST'])
def upload_clean_photos_blob():
    # 요청으로부터 학생 학번 및 방 번호, 자리 번호 가져오기
    student_number = request.json.get('student_number')
    room_number = request.json.get('room_number')
    seat_number = request.json.get('seat_number')

    # BLOB 데이터 가져오기
    photos = request.json.get('photos')  # photos는 프론트에서 보낸 BLOB 데이터 리스트

    if not student_number or not room_number or not seat_number:
        return jsonify({'error': 'Student number, room number, and seat number are required'}), 400

    if not photos or len(photos) < 1 or len(photos) > 4:
        return jsonify({'error': 'You must upload at least 1 and at most 4 photos in BLOB format'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # WARN의 기본값을 0으로 설정
        warn_default = 0

        # 4개 미만의 사진이 업로드되면 남은 PIC 칼럼은 NULL로 설정
        while len(photos) < 4:
            photos.append(None)

        # 기존 데이터가 있는지 확인
        cursor.execute(
            "SELECT CID FROM CLEAN WHERE CROOM = %s AND CSEATUM = %s",
            (room_number, seat_number)
        )
        existing_data = cursor.fetchone()

        # 기존 데이터가 있으면 업데이트, 없으면 새로운 레코드 생성
        if existing_data:
            # 기존 레코드 업데이트
            update_query = """
                UPDATE CLEAN 
                SET PIC1 = %s, PIC2 = %s, PIC3 = %s, PIC4 = %s, WARN = %s 
                WHERE CROOM = %s AND CSEATUM = %s
            """
            cursor.execute(update_query, (*photos, warn_default, room_number, seat_number))
            message = "Photos updated successfully for existing record."
        else:
            # 새 레코드 삽입
            insert_query = """
                INSERT INTO CLEAN (CROOM, CSEATUM, PIC1, PIC2, PIC3, PIC4, WARN)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (room_number, seat_number, *photos, warn_default))
            message = "Photos uploaded successfully for new record."

        connection.commit()
        return jsonify({'message': message}), 200

    except Exception as e:
        logging.error(f"Error during photo upload: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()