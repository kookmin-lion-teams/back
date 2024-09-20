import unittest
import requests

class TestStudentCheck(unittest.TestCase):
    
    def test_check_in(self):
        # 학생 출석 체크 API 엔드포인트 URL
        url = 'http://127.0.0.1:5000/student/check_in'

        # 올바른 요청 데이터 (테스트할 학생 학번 사용)
        payload = {'stnum': 5}  # 테스트할 학번 설정

        # API 호출
        response = requests.post(url, json=payload)

        # 응답 상태 코드 출력 및 검증
        print("Response status code:", response.status_code)
        try:
            response_json = response.json()
            print("Response JSON:", response_json)
        except ValueError:
            print("Failed to decode JSON response.")
            response_json = {}

        # 테스트 검증
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
        self.assertIn('Recorded in IN table', response_json.get('message', ''), 
                      "Expected 'Recorded in IN table' in the message")

if __name__ == '__main__':
    unittest.main()