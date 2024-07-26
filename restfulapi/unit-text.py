import unittest
from unittest.mock import patch, MagicMock
import service
import json

class TestService(unittest.TestCase):
    @patch('service.sqlite3')
    @patch('service.verify_token')  # 模拟 verify_token 函数
    def test_get_alarm(self, mock_verify_token, mock_sqlite):
        # 模拟 verify_token 总是返回 True
        mock_verify_token.return_value = True

        # 模拟数据库操作
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        # 模拟返回值
        mock_cursor.fetchone.return_value = (1, 'Test Alarm', 'Description')
        
        token = "dummy_token"  # 假设的 token
        result = service.get_alarm(token, 1)
        
        # 验证返回的 JSON
        expected_result = json.dumps({'id': 1, 'name': 'Test Alarm', 'description': 'Description'})
        self.assertEqual(result, expected_result)

    @patch('service.sqlite3')
    @patch('service.verify_token')  # 模拟 verify_token 函数
    def test_add_alarm(self, mock_verify_token, mock_sqlite):
        # 模拟 verify_token 总是返回 True
        mock_verify_token.return_value = True

        # 模拟数据库操作
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        alarm_data = {'name': 'New Alarm', 'description': 'New alarm description'}
        token = "dummy_token"  # 假设的 token
        service.add_alarm(token, alarm_data)
        
        # 验证是否执行了正确的 SQL 语句
        mock_cursor.execute.assert_called_with("INSERT INTO alarms (name, description) VALUES (?, ?)", (alarm_data['name'], alarm_data['description']))

if __name__ == '__main__':
    unittest.main()