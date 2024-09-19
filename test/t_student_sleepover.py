import requests
import unittest
from datetime import datetime

class TestStudentSleepover(unittest.TestCase):

    def test_create_sleepover_request(self):
        # 외박 신청서 작성 API 엔드포인트 URL
        url = 'http://127.0.0.1:5000/student/sleepover'

        # 올바른 요청 데이터
        correct_payload = {
            'sstnum': '25',  # 예시 학번
            'reason': 'test',
            'startdate': '2024-09-23',
            'enddate': '2024-09-25'
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
        self.assertEqual(response.status_code, 201, f"Expected status code 201, but got {response.status_code}")
        self.assertIn('Sleepover request created', response.json().get('message', ''), "Sleepover request not created correctly.")
        print("Test for creating sleepover request passed!")

if __name__ == '__main__':
    unittest.main()