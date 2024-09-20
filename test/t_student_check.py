# t_student_check.py
import requests
import unittest

class TestStudentCheck(unittest.TestCase):

    def test_check_in(self):
        # 학생 점호 체크 API 엔드포인트 URL
        url = 'http://127.0.0.1:5000/student/check_in'

        # 테스트할 학생의 학번
        student_number = 1

        # POST 요청 데이터
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
        self.assertIn('message', response_json, "Message data is not present in the response")
        
        # STUDENT 테이블에서 IN 값 확인
        student_url = f'http://127.0.0.1:5000/admin/students'
        student_response = requests.get(student_url)
        
        try:
            student_data = student_response.json()
            # 해당 학생의 정보를 필터링하여 가져오기
            student_info = next(item for item in student_data['students'] if item["STNUM"] == student_number)
            print("Check Response JSON:", student_info)
        except ValueError:
            print("Failed to decode JSON from STUDENT table. Response content:", student_response.text)
            self.fail("Failed to decode JSON response from STUDENT table")
        
        # 출석 체크 후 IN 값이 증가했는지 확인
        expected_in_value = 2  # 이전 IN 값이 1일 경우 다음 값은 2
        self.assertEqual(student_info['IN'], expected_in_value, f"Expected IN value to be {expected_in_value}, but got {student_info['IN']}")

        print("Test for student check-in API passed!")

if __name__ == '__main__':
    unittest.main()