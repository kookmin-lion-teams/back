import requests

def test_update_warn():
    # API 엔드포인트 URL
    url = 'http://127.0.0.1:5000/admin/update_warn'  # 엔드포인트 URL

    # 올바른 방 번호와 자리 번호로 경고 값 증가 요청
    correct_payload = {'room_number': 100, 'seat_number': 1}
    response = requests.post(url, json=correct_payload)

    # 응답 출력
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 성공적인 응답 코드(200) 확인
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert 'Warn value updated successfully' in response.json().get('message', ''), "Warn update failed with correct room and seat number"
    print("Test with correct room and seat number passed!")


if __name__ == '__main__':
    test_update_warn()