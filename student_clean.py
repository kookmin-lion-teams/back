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
    student_number = request.form.get('student_number')
    room_number = request.form.get('room_number')
    seat_number = request.form.get('seat_number')

    # 파일 체크: 최소 1장, 최대 4장이어야 함
    files = request.files.getlist('photos')  # 'photos'는 프론트에서 보낸 파일 리스트

    if not student_number or not room_number or not seat_number:
        return jsonify({'error': 'Student number, room number, and seat number are required'}), 400

    if len(files) < 1 or len(files) > 4:
        return jsonify({'error': 'You must upload at least 1 and at most 4 photos'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # WARN의 기본값을 0으로 설정
        warn_default = 0

        # 4개 미만의 사진이 업로드되면 남은 PIC 칼럼은 NULL로 설정
        photo_blobs = []
        for file in files:
            # 파일을 BLOB 형식으로 읽어오기
            photo_blob = file.read()
            photo_blobs.append(photo_blob)
        
        # 4개 미만의 사진이 업로드되면 남은 PIC 칼럼은 NULL로 설정
        while len(photo_blobs) < 4:
            photo_blobs.append(None)

        # 사진 BLOB 데이터를 데이터베이스에 저장
        update_query = """
            UPDATE CLEAN 
            SET PIC1 = %s, PIC2 = %s, PIC3 = %s, PIC4 = %s, WARN = %s 
            WHERE CROOM = %s AND CSEATUM = %s
        """
        
        cursor.execute(update_query, (*photo_blobs, warn_default, room_number, seat_number))

        connection.commit()
        return jsonify({'message': 'Photos uploaded successfully as BLOB data'}), 200

    except Exception as e:
        logging.error(f"Error during photo upload: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()