# 관리자 로그인 

from flask import Blueprint, jsonify, request
from dbutil import create_db_connection  # DB 연결 유틸리티 임포트
import logging  # logging 모듈 임포트

# 블루프린트 정의
admin_login = Blueprint('admin_login', __name__)

# 관리자 로그인 엔드포인트
@admin_login.route('/admin/login', methods=['POST'])
def login():
    # 요청에서 아이디와 패스워드 가져오기
    admin_id = request.json.get('admin_id')
    admin_password = request.json.get('admin_password')

    # 입력 값 유효성 검사
    if not admin_id or not admin_password:
        return jsonify({'error': 'Admin ID and password are required'}), 400

    # 데이터베이스 연결 생성
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        # SQL 쿼리에서 테이블의 실제 컬럼 이름(ID와 PW) 사용
        cursor.execute("SELECT * FROM ADMIN WHERE ID = %s AND PW = %s", (admin_id, admin_password))
        admin = cursor.fetchone()  # 일치하는 첫 번째 관리자 데이터 가져오기

        # 쿼리 결과 확인용 로그
        logging.debug(f"Query result: {admin}")

        # 관리자 정보가 일치하는지 확인
        if admin:
            # 'ID' 키를 사용하여 결과 출력
            return jsonify({'message': f"Welcome, {admin.get('ID', 'Unknown')}!"}), 200
        else:
            return jsonify({'error': 'Invalid admin ID or password'}), 404
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()