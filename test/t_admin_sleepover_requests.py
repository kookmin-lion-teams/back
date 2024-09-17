import requests

def test_get_sleepover_requests():
    # API 엔드포인트 URL
    url = 'http://127.0.0.1:5000/admin/sleepover_requests'  # Flask 서버의 엔드포인트 URL

    # GET 요청을 보내 외박 신청서 목록 조회
    response = requests.get(url)

    # 응답 상태 코드 출력
    print("Response status code:", response.status_code)

    # 응답이 JSON 형식으로 올바르게 반환되는지 확인
    try:
        response_json = response.json()  # JSON 응답 파싱 시도
        print("Response JSON:", response_json)

        # 성공적인 응답 코드(200) 확인
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        assert 'requests' in response_json, "Expected key 'requests' in the response"
        assert isinstance(response_json['requests'], list), "Expected 'requests' to be a list"
        print("Test to get sleepover requests passed!")

    except requests.exceptions.JSONDecodeError:
        print("Response is not in JSON format.")
        assert response.status_code == 500, f"Expected status code 500, but got {response.status_code}"
        print("Test for JSON decode error passed!")

if __name__ == '__main__':
    test_get_sleepover_requests()