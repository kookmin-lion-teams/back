# t_student_checklist.py
import requests
import unittest
from datetime import datetime

class TestStudentChecklist(unittest.TestCase):

    def test_get_checklist(self):
        url = 'http://127.0.0.1:5000/student/checklist'
        student_number = 1
        payload = {'stnum': student_number}

        response = requests.post(url, json=payload)
        print("Response status code:", response.status_code)

        try:
            response_json = response.json()
            print("Response JSON:", response_json)
            for entry in response_json.get('checklist', []):
                print(f"Date: {entry['date']} ({entry['day']}), Status: {entry['status']}, SEP: {entry['sep']}")
        except ValueError:
            print("Failed to decode JSON. Response content:", response.text)
            self.fail("Failed to decode JSON response")

        # 응답 검증
        if 'checklist' not in response_json:
            print(f"Error: 'checklist' key not found in response: {response_json}")
            self.fail("Checklist data not found in the response")
            
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
        self.assertIn('checklist', response_json, "Checklist data is not present in the response")
        self.assertIsInstance(response_json['checklist'], list, "Checklist data should be a list")

        # 체크리스트 항목 검증
        for entry in response_json['checklist']:
            self.assertIn('date', entry, "Each entry should have 'date'")
            self.assertIn('day', entry, "Each entry should have 'day'")
            self.assertIn('status', entry, "Each entry should have 'status'")
            self.assertIn('sep', entry, "Each entry should have 'sep'")

            date_format = "%Y-%m-%d"
            try:
                datetime.strptime(entry['date'], date_format)
            except ValueError:
                self.fail(f"Date format incorrect: {entry['date']}")

            self.assertIn(entry['day'], ['월', '화', '수', '목', '금', '토', '일'], f"Invalid day format: {entry['day']}")
            self.assertIn(entry['status'], ['AWAY', 'IN'], f"Invalid STATUS value: {entry['status']}")
            self.assertIsInstance(entry['sep'], int, f"SEP should be an integer: {entry['sep']}")

        print("Test for student checklist API passed!")

if __name__ == '__main__':
    unittest.main()