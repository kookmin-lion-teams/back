from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from admin_login import admin_login # 관리자 로그인 
from student_login import student_login # 학생 로그인 
from student_check import student_check # 학생 점호 버튼 클릭 
from student_away import student_away_bp, reset_attendance, mark_absent_students  # 수정된 함수 이름으로 가져오기
# 점호 불참 학생 조회 / 스케줄러  # IN 컬럼 0 초기화 # 9시 10분 이후 학생 away 테이블에 추가  
from student_sleepover import student_sleepover_bp # 학생 외박 신청 
from admin_sleepover_requests import admin_sleepover_requests_bp # 관리자 학생 외박 목록 조회
from admin_sleepover_approve import admin_sleepover_approve_bp # 외박 승인 거부 
from student_clean import student_clean_bp # 청소 사진 업로드
from admin_clean import admin_clean_bp # 청소 목록 조회
from admin_warn import admin_warn_bp # 청소 상태 경고 ( warn 2 스택 0 초기화 학생 테이블 minus + 1)
from admin_student_list import admin_student_bp # 학생 목록 조회
from dbutil import create_db_connection  # DB 연결 유틸리티 가져오기

app = Flask(__name__)

# 블루프린트 등록
app.register_blueprint(admin_login)
app.register_blueprint(student_login)
app.register_blueprint(student_check)
app.register_blueprint(student_away_bp, url_prefix='/student_away')
app.register_blueprint(student_sleepover_bp)
app.register_blueprint(admin_sleepover_requests_bp)
app.register_blueprint(admin_sleepover_approve_bp)
app.register_blueprint(student_clean_bp)
app.register_blueprint(admin_clean_bp)
app.register_blueprint(admin_warn_bp)
app.register_blueprint(admin_student_bp)

# 학생의 sleepcount 값을 0으로 초기화하는 함수
def reset_sleepcount():
    try:
        # 데이터베이스 연결 생성
        connection = create_db_connection()
        if connection is None:
            logging.error('Database connection failed during sleepcount reset.')
            return
        
        cursor = connection.cursor()

        # 학생의 sleepcount 값을 0으로 초기화하는 쿼리 실행
        cursor.execute("UPDATE STUDENT SET SLEEPCOUNT = 0")
        connection.commit()

        logging.info('All students\' sleepcount reset to 0 successfully.')
    
    except Exception as e:
        logging.error(f"Error during sleepcount reset: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 스케줄러 설정
scheduler = BackgroundScheduler()

# 매주 화요일 00:00에 reset_attendance 함수를 실행하는 작업 추가
scheduler.add_job(func=reset_attendance, trigger='cron', day_of_week='mon', hour=0, minute=0)

# 매일 9시 10분에 mark_absent_students 함수를 실행하는 작업 추가
scheduler.add_job(func=mark_absent_students, trigger='cron', hour=9, minute=10)

# 매월 1일 00:00에 reset_sleepcount 함수를 실행하는 작업 추가
scheduler.add_job(func=reset_sleepcount, trigger='cron', day=1, hour=0, minute=0)

# 스케줄러 시작
scheduler.start()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()