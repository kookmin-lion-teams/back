import requests
import unittest
import json

class TestStudentSleepoverList(unittest.TestCase):

    def test_get_student_sleepover_list(self):
        # API 엔드포인트 URL
        url = 'http://127.0.0.1:5000/student/sleepover_list'

        # 학번이 3인 학생의 외박 신청 내역 조회를 위한 요청 데이터
        payload = {
            'sstnum': 3  # 학번이 3인 학생
        }

        # API 호출
        response = requests.post(url, json=payload)

        # 응답 상태 코드 출력
        print("Response status code:", response.status_code)

        # 응답 데이터 출력
        try:
            response_json = response.json()
            print("Response JSON:")
            # 모든 컬럼의 내용 출력
            for index, item in enumerate(response_json.get('sleepover_list', []), 1):
                print(f"Record {index}: {json.dumps(item, ensure_ascii=False, indent=4)}")  # JSON 형식으로 한 줄씩 출력
        except ValueError:
            print("Failed to decode JSON. Response content:", response.text)

        # API 호출 결과를 검증
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
        self.assertIn('sleepover_list', response.json(), "Failed to retrieve sleepover list")
        self.assertIsInstance(response.json().get('sleepover_list'), list, "Expected 'sleepover_list' to be a list")
        self.assertGreater(len(response.json().get('sleepover_list')), 0, "Expected at least one sleepover record for student with sstnum 3")
        print("Test to get student sleepover list passed!")

if __name__ == '__main__':
    unittest.main()