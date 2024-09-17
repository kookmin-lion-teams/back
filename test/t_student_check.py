import requests

def test_check_attendance():
    # 점호 체크 API 엔드포인트 URL
    url = 'http://127.0.0.1:5000/student/check'

    # 올바른 학번으로 점호 체크 시도
    correct_payload = {'stnum': '20212621'}  # 존재하는 학번을 사용해야 합니다
    response = requests.post(url, json=correct_payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert 'Attendance checked for student' in response.json().get('message', ''), "Failed to check attendance with correct student number"
    print("Test with correct student number passed!")

    # 잘못된 학번으로 점호 체크 시도
    wrong_payload = {'stnum': '99999999'}  # 존재하지 않는 학번
    response = requests.post(url, json=wrong_payload)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    assert 'Student not found' in response.json().get('error', ''), "Failed to handle wrong student number correctly"
    print("Test with wrong student number passed!")

if __name__ == '__main__':
    test_check_attendance()