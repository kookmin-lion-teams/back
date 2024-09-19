import requests
import json

def test_get_all_students():
    # API 엔드포인트 URL
    url = 'http://127.0.0.1:5000/admin/students'  # 엔드포인트 URL

    # GET 요청을 보내 학생 전체 목록을 조회
    response = requests.get(url)

    # 응답 출력
    print("Response status code:", response.status_code)

    # JSON 형식 응답 파싱 시도
    try:
        response_json = response.json()
        # 학생 목록이 있는지 확인
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        assert 'students' in response_json, "Failed to retrieve students list"

        # 학생 목록 출력
        students = response_json['students']
        print("\nStudents List:\n")
        for student in students:
            # 학생 한 명의 정보를 JSON 문자열로 변환하여 보기 좋게 출력
            formatted_student = json.dumps(student, indent=4, ensure_ascii=False)
            print(formatted_student)
            print("-" * 80)  # 구분선

        print("Test to get all students passed!")
    except ValueError:
        print("Failed to decode JSON. Response content:", response.text)

if __name__ == '__main__':
    test_get_all_students()