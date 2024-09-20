import requests
import unittest

class TestApproveSleepoverRequest(unittest.TestCase):

    def test_approve_sleepover_request(self):
        # 외박 신청서 승인 API 엔드포인트 URL
        url = 'http://127.0.0.1:5000/admin/sleepover_approve'

        # 승인할 외박 신청 SID (테스트할 값으로 변경)
        correct_payload = {
            'sid': 10  # 테스트할 외박 신청 SID (예: 2)
        }

        # API 호출
        response = requests.post(url, json=correct_payload)

        # 응답 상태 코드 출력
        print("Response status code:", response.status_code)

        # 응답 데이터 출력
        try:
            response_json = response.json()
            print("Response JSON:", response_json)
        except ValueError:
            print("Failed to decode JSON. Response content:", response.text)

        # API 호출 결과를 검증
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
        self.assertIn('Sleepover request approved', response_json.get('message', ''), "Sleepover request not approved correctly.")
        print("Test for approving sleepover request passed!")

if __name__ == '__main__':
    unittest.main()