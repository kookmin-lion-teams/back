import requests
import unittest

class TestRejectSleepoverRequest(unittest.TestCase):

    def test_reject_sleepover_request(self):
        # 외박 신청서 거부 API 엔드포인트 URL
        url = 'http://127.0.0.1:5000/admin/sleepover_reject'

        # 올바른 요청 데이터 (테스트할 SID 사용)
        correct_payload = {
            'sid': 3  # 테스트할 외박 신청 SID (예: 2)
        }

        # API 호출
        response = requests.post(url, json=correct_payload)

        # 응답 상태 코드 출력
        print("Response status code:", response.status_code)

        # 응답 데이터 출력
        try:
            print("Response JSON:", response.json())
        except ValueError:
            print("Failed to decode JSON. Response content:", response.text)

        # API 호출 결과를 검증
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
        self.assertIn('Sleepover request rejected', response.json().get('message', ''), "Sleepover request not rejected correctly.")
        print("Test for rejecting sleepover request passed!")

if __name__ == '__main__':
    unittest.main()