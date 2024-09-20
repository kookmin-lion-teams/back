import requests
import unittest

class TestGetAllStudents(unittest.TestCase):

    def test_get_all_students(self):
        # API 엔드포인트 URL
        url = 'http://127.0.0.1:5000/admin/students'

        # GET 요청을 보내 학생 전체 목록 조회
        response = requests.get(url)

        # 응답 상태 코드 확인
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")

        # JSON 응답 데이터 확인
        response_json = response.json()
        print("Response JSON:", response_json)

        # 'students' 키가 있는지 확인
        self.assertIn('students', response_json, "Response JSON does not contain 'students' key")

        # 학생 목록 데이터가 올바른지 확인
        students = response_json['students']
        self.assertIsInstance(students, list, "Expected 'students' to be a list")
        
        # 각 학생의 정보를 확인 (필수 필드 및 'away_count' 필드 확인)
        for student in students:
            self.assertIn('STNUM', student, "Each student record should contain 'STNUM'")
            self.assertIn('NAME', student, "Each student record should contain 'NAME'")
            self.assertIn('away_count', student, "Each student record should contain 'away_count'")
            print(f"Student {student['STNUM']} - {student['NAME']} has {student['away_count']} missed check-ins")

        print("Test to get all students with away_count passed!")

if __name__ == '__main__':
    unittest.main()