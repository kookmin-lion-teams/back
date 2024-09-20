from flask import Blueprint, request, jsonify
from dbutil import create_db_connection
import logging
from datetime import datetime

# 블루프린트 정의
student_clean_bp = Blueprint('student_clean', __name__)

# 사진 업로드 엔드포인트 (BLOB 데이터베이스 저장용)
@student_clean_bp.route('/student/upload_clean_photos', methods=['POST'])
def upload_clean_photos_blob():
    try:
        # 요청으로부터 학생 학번 및 방 번호, 자리 번호 가져오기
        student_number = request.form.get('student_number')
        room_number = request.form.get('room_number')
        seat_number = request.form.get('seat_number')

        # BLOB 데이터 가져오기
        photos = request.files.getlist('photos')  # `photos`는 프론트에서 보낸 파일 데이터 리스트

        # 디버깅 메시지 추가
        logging.debug(f"Received student_number: {student_number}")
        logging.debug(f"Received room_number: {room_number}")
        logging.debug(f"Received seat_number: {seat_number}")
        logging.debug(f"Received photos count: {len(photos)}")

        # 사진의 내용 확인 (파일명 및 첫 몇 바이트를 로깅)
        for i, file in enumerate(photos):
            file_content = file.read()
            logging.debug(f"Photo {i+1}: filename={file.filename}, size={len(file_content)} bytes, first 100 bytes: {file_content[:100]}")
            file.seek(0)  # 이후 사용할 수 있도록 파일 포인터를 처음으로 되돌리기

        # 유효성 검사
        if not student_number or not room_number or not seat_number:
            return jsonify({'error': 'Student number, room number, and seat number are required'}), 400

        if len(photos) < 1 or len(photos) > 4:
            return jsonify({'error': 'You must upload at least 1 and at most 4 photos in BLOB format'}), 400

        # 데이터베이스 연결 생성
        connection = create_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = connection.cursor(dictionary=True)

        # WARN의 기본값을 0으로 설정
        warn_default = 0

        # 4개 미만의 사진이 업로드되면 남은 PIC 칼럼은 NULL로 설정
        while len(photos) < 4:
            photos.append(None)

        # 사진 BLOB 데이터를 데이터베이스에 저장
        update_query = """
            UPDATE CLEAN 
            SET PIC1 = %s, PIC2 = %s, PIC3 = %s, PIC4 = %s, WARN = %s 
            WHERE CROOM = %s AND CSEATUM = %s
        """
        
        photo_data = [file.read() if file is not None else None for file in photos]
        cursor.execute(update_query, (*photo_data, warn_default, room_number, seat_number))

        connection.commit()
        return jsonify({'message': 'Photos uploaded successfully as BLOB data'}), 200

    except Exception as e:
        logging.error(f"Error during photo upload: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()