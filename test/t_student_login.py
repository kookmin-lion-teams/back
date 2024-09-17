import requests

def test_student_login():
    # API 엔드포인트 URL
    url = 'http://127.0.0.1:5000/student/login'

    # 올바른 학생 이름과 학번으로 로그인 시도
    correct_payload = {'name': '김준서', 'stnum': '20212621'}
    response = requests.post(url, json=correct_payload)

    # 응답 출력
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert 'student_info' in response.json(), "Failed to retrieve student information with correct credentials"
    print("Test with correct student credentials passed!")

    # 잘못된 학생 이름 또는 학번으로 로그인 시도
    wrong_payload = {'name': '박정빈', 'stnum': '12345678'}
    response = requests.post(url, json=wrong_payload)

    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    assert 'Invalid name or student number' in response.json().get('error', ''), "Failed to handle wrong student credentials correctly"
    print("Test with wrong student credentials passed!")

if __name__ == '__main__':
    test_student_login()