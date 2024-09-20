# t_student_sleepover_list.py
import requests
import unittest
from datetime import datetime

class TestStudentSleepoverList(unittest.TestCase):

    def test_get_sleepover_list(self):
        # 학생 외박 신청 내역 조회 API 엔드포인트 URL
        url = 'http://127.0.0.1:5000/student/sleepover_list'

        # 테스트할 학생의 학번
        student_number = 3

        # POST 요청 데이터 (로그인한 학생의 학번)
        payload = {'sstnum': student_number}

        # POST 요청 보내기
        response = requests.post(url, json=payload)

        # 응답 상태 코드 출력
        print("Response status code:", response.status_code)

        # 응답 데이터 출력
        try:
            response_json = response.json()
            print("Response JSON:")
            print(response_json)
        except ValueError:
            print("Failed to decode JSON. Response content:", response.text)
            self.fail("Failed to decode JSON response")

        # 응답에 'error' 키가 있는지 확인
        if 'error' in response_json:
            self.fail(f"API error occurred: {response_json['error']}")

        # 응답 검증
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
        self.assertIn('sleepover_list', response_json, "Sleepover list data is not present in the response")
        self.assertIsInstance(response_json['sleepover_list'], list, "Sleepover list data should be a list")

        # 체크리스트 항목이 올바른 형식인지 검증
        for entry in response_json['sleepover_list']:
            self.assertIn('SID', entry, "Each entry should have 'SID'")
            self.assertIn('SSTNUM', entry, "Each entry should have 'SSTNUM'")
            self.assertIn('REASON', entry, "Each entry should have 'REASON'")
            self.assertIn('ADATE', entry, "Each entry should have 'ADATE'")
            self.assertIn('STARTDATE', entry, "Each entry should have 'STARTDATE'")
            self.assertIn('ENDDATE', entry, "Each entry should have 'ENDDATE'")
            self.assertIn('CHECK', entry, "Each entry should have 'CHECK'")

            # 날짜 형식 검증
            date_format = "%Y-%m-%d"
            try:
                date_part, day_part = entry['ADATE'].split("(")
                datetime.strptime(date_part, date_format)
                self.assertIn(day_part.rstrip(")"), ['월', '화', '수', '목', '금', '토', '일'], f"Invalid day format: {day_part}")
            except ValueError:
                self.fail(f"Date format incorrect: {entry['ADATE']}")

        print("Test for student sleepover list API passed!")

if __name__ == '__main__':
    unittest.main()