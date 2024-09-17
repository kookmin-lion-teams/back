import unittest
import requests

class TestAdminSleepoverApproval(unittest.TestCase):

    def test_approve_sleepover_request(self):
        # API URL 정의
        url_approve = 'http://127.0.0.1:5000/admin/sleepover_approve'
        url_list = 'http://127.0.0.1:5000/admin/sleepover_requests'
        
        # 외박 신청서 목록 조회
        response = requests.get(url_list)
        self.assertEqual(response.status_code, 200, f"Failed to fetch sleepover requests with status code {response.status_code}")
        
        requests_list = response.json().get('requests', [])

        # 승인할 첫 번째 신청서 선택 (있을 경우)
        if requests_list:
            request_id = requests_list[0]['SID']

            # 승인 테스트
            approve_payload = {'action': 'approve'}
            response = requests.post(f"{url_approve}/{request_id}", json=approve_payload)
            self.assertEqual(response.status_code, 200, f"Failed to approve sleepover request with status code {response.status_code}")
            print("Approval test passed!")

    def test_reject_sleepover_request(self):
        # API URL 정의
        url_reject = 'http://127.0.0.1:5000/admin/sleepover_approve'
        url_list = 'http://127.0.0.1:5000/admin/sleepover_requests'
        
        # 외박 신청서 목록 조회
        response = requests.get(url_list)
        self.assertEqual(response.status_code, 200, f"Failed to fetch sleepover requests with status code {response.status_code}")
        
        requests_list = response.json().get('requests', [])

        # 미승인할 첫 번째 신청서 선택 (있을 경우)
        if requests_list:
            request_id = requests_list[0]['SID']

            # 미승인 테스트
            reject_payload = {'action': 'reject'}
            response = requests.post(f"{url_reject}/{request_id}", json=reject_payload)
            self.assertEqual(response.status_code, 200, f"Failed to reject sleepover request with status code {response.status_code}")
            print("Rejection test passed!")

if __name__ == '__main__':
    unittest.main()