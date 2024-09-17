import unittest
import requests

class TestStudentClean(unittest.TestCase):

    def test_upload_clean_photos_success(self):
        url = 'http://127.0.0.1:5000/student/upload_clean_photos'

        # 성공적인 사진 업로드 케이스
        files = {
            'photos': [
                ('photo1', open('test_images/photo1.jpg', 'rb')),
                ('photo2', open('test_images/photo2.jpg', 'rb'))
            ]
        }
        data = {
            'student_number': '20212621',
            'room_number': '101',
            'seat_number': '1'
        }

        response = requests.post(url, files=files, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Photos uploaded successfully', response.json().get('message', ''))

    def test_upload_clean_photos_failure_no_files(self):
        url = 'http://127.0.0.1:5000/student/upload_clean_photos'

        # 파일 없이 요청하는 케이스
        data = {
            'student_number': '20212621',
            'room_number': '101',
            'seat_number': '1'
        }

        response = requests.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('You must upload at least 1 and at most 4 photos', response.json().get('error', ''))

    def test_upload_clean_photos_failure_exceeds_max_files(self):
        url = 'http://127.0.0.1:5000/student/upload_clean_photos'

        # 최대 개수(4장)를 초과하는 사진 업로드
        files = {
            'photos': [
                ('photo1', open('test_images/photo1.jpg', 'rb')),
                ('photo2', open('test_images/photo2.jpg', 'rb')),
                ('photo3', open('test_images/photo3.jpg', 'rb')),
                ('photo4', open('test_images/photo4.jpg', 'rb')),
                ('photo5', open('test_images/photo5.jpg', 'rb'))
            ]
        }
        data = {
            'student_number': '20212621',
            'room_number': '101',
            'seat_number': '1'
        }

        response = requests.post(url, files=files, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('You must upload at least 1 and at most 4 photos', response.json().get('error', ''))

if __name__ == '__main__':
    unittest.main()