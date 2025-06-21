import unittest
from unittest.mock import patch, MagicMock
import datetime
from aws_cost_report import get_dates, print_table, post_to_discord


class TestAWSCostReport(unittest.TestCase):

    def test_get_dates_returns_yesterday_and_month_start(self):
        today, yesterday, month_start = get_dates()
        self.assertEqual(today, datetime.date.today())
        self.assertEqual(yesterday, today - datetime.timedelta(days=1))
        self.assertEqual(month_start, today.replace(day=1))

    def test_print_table_returns_correct_total(self):
        groups = [
            {'Keys': ['Amazon EC2'], 'Metrics': {'UnblendedCost': {'Amount': '3.45'}}},
            {'Keys': ['Amazon S3'], 'Metrics': {'UnblendedCost': {'Amount': '1.55'}}}
        ]
        with patch('builtins.print'):
            total = print_table("Test Title", groups, "Service")
        self.assertAlmostEqual(total, 5.0)

    @patch('requests.post')
    def test_post_to_discord_success(self, mock_post):
        mock_post.return_value.status_code = 204
        with patch('builtins.print') as mock_print:
            post_to_discord("https://fake.url", 4.50, 99.99, datetime.date(2025, 6, 20))
            mock_print.assert_any_call("\n✅ Summary successfully posted to Discord.")

    @patch('requests.post')
    def test_post_to_discord_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = "Bad Request"
        with patch('builtins.print') as mock_print:
            post_to_discord("https://fake.url", 4.50, 99.99, datetime.date(2025, 6, 20))
            mock_print.assert_any_call("\n⚠️  Failed to post to Discord: 400 - Bad Request")


if __name__ == '__main__':
    unittest.main()
