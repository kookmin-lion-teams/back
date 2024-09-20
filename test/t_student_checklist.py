# t_student_checklist.py
import requests
import unittest

class TestStudentChecklist(unittest.TestCase):

    def test_get_checklist(self):
        # 학생 점호 내역 조회 API 엔드포인트 URL
        url = 'http://127.0.0.1:5000/student/checklist'

        # 테스트할 학생의 학번
        student_number = 3

        # POST 요청 데이터 (로그인한 학생의 학번)
        payload = {'stnum': student_number}

        # POST 요청 보내기
        response = requests.post(url, json=payload)

        # 응답 상태 코드 출력
        print("Response status code:", response.status_code)

        # 응답 데이터 출력
        try:
            response_json = response.json()
            print("Response JSON:", response_json)
        except ValueError:
            print("Failed to decode JSON. Response content:", response.text)
            self.fail("Failed to decode JSON response")

        # 응답 검증
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
        self.assertIn('checklist', response_json, "Checklist data is not present in the response")
        self.assertIsInstance(response_json['checklist'], list, "Checklist data should be a list")

        # 체크리스트 항목이 올바른 형식인지 검증
        for entry in response_json['checklist']:
            self.assertIn('DATE', entry, "Each entry should have 'DATE'")
            self.assertIn('STATUS', entry, "Each entry should have 'STATUS'")
            self.assertIn('SEP', entry, "Each entry should have 'SEP'")

        print("Test for student checklist API passed!")

if __name__ == '__main__':
    unittest.main()