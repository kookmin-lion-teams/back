import requests

def test_get_all_students():
    # API 엔드포인트 URL
    url = 'http://127.0.0.1:5000/admin/students'  # 엔드포인트 URL

    # GET 요청을 보내 학생 전체 목록을 조회
    response = requests.get(url)

    # 응답 출력
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 성공적인 응답 코드(200) 확인
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert 'students' in response.json(), "Failed to retrieve students list"
    print("Test to get all students passed!")

if __name__ == '__main__':
    test_get_all_students()