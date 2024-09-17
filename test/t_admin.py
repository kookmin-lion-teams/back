import requests

def test_admin_login():
    # API 엔드포인트 URL
    url = 'http://127.0.0.1:5000/admin/login'

    # 올바른 관리자 아이디와 패스워드로 로그인 시도
    correct_payload = {'admin_id': 'admin', 'admin_password': '1234'}
    response = requests.post(url, json=correct_payload)

    # 응답 출력
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert 'Welcome, admin!' in response.json().get('message', ''), "Failed to login with correct admin credentials"
    print("Test with correct admin credentials passed!")

    # 잘못된 관리자 아이디 또는 패스워드로 로그인 시도
    wrong_payload = {'admin_id': 'wrongadmin', 'admin_password': 'wrongpass'}
    response = requests.post(url, json=wrong_payload)

    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    assert 'Invalid admin ID or password' in response.json().get('error', ''), "Failed to handle wrong admin credentials correctly"
    print("Test with wrong admin credentials passed!")

if __name__ == '__main__':
    test_admin_login()