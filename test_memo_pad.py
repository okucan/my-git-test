import unittest
import os
import io
import sys
import memo_pad # To modify memo_pad.MEMO_FILE
from memo_pad import add_memo, view_memos, delete_memo
from unittest.mock import patch

class TestMemoPad(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.test_memo_file = "test_memos.txt"
        # This is the crucial part: we are telling memo_pad to use a different file for its operations.
        memo_pad.MEMO_FILE = self.test_memo_file
        # Ensure a clean slate before each test
        if os.path.exists(self.test_memo_file):
            os.remove(self.test_memo_file)

    def tearDown(self):
        """Tear down after test methods."""
        # Clean up the test file after each test
        if os.path.exists(self.test_memo_file):
            os.remove(self.test_memo_file)
        # It's good practice to restore the original MEMO_FILE value if other tests might run in the same session,
        # though for isolated unittest runs, it might not be strictly necessary.
        memo_pad.MEMO_FILE = "memos.txt"


    # --- Tests for add_memo ---
    def test_add_single_memo(self):
        add_memo("Test memo 1")
        self.assertTrue(os.path.exists(self.test_memo_file))
        with open(self.test_memo_file, "r") as f:
            content = f.readlines()
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].strip(), "Test memo 1")

    def test_add_multiple_memos(self):
        add_memo("Memo Alpha")
        add_memo("Memo Beta")
        add_memo("Memo Gamma")
        self.assertTrue(os.path.exists(self.test_memo_file))
        with open(self.test_memo_file, "r") as f:
            content = f.readlines()
        self.assertEqual(len(content), 3)
        self.assertEqual(content[0].strip(), "Memo Alpha")
        self.assertEqual(content[1].strip(), "Memo Beta")
        self.assertEqual(content[2].strip(), "Memo Gamma")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_empty_memo_string(self, mock_stdout):
        add_memo("") # Empty string
        self.assertFalse(os.path.exists(self.test_memo_file), "File should not be created for an empty memo.")
        self.assertEqual(mock_stdout.getvalue().strip(), "Error: Memo text cannot be empty.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_whitespace_memo_string(self, mock_stdout):
        add_memo("   ") # Whitespace string
        self.assertFalse(os.path.exists(self.test_memo_file), "File should not be created for a whitespace-only memo.")
        self.assertEqual(mock_stdout.getvalue().strip(), "Error: Memo text cannot be empty.")

    def test_add_memo_strips_whitespace(self):
        add_memo("  Leading and trailing spaces  ")
        self.assertTrue(os.path.exists(self.test_memo_file))
        with open(self.test_memo_file, "r") as f:
            content = f.readlines()
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].strip(), "Leading and trailing spaces")


    # --- Tests for view_memos ---
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_view_memos_no_file(self, mock_stdout):
        # Ensure file does not exist (setUp should handle this, but double-check)
        if os.path.exists(self.test_memo_file):
            os.remove(self.test_memo_file)
        view_memos()
        self.assertEqual(mock_stdout.getvalue().strip(), "No memos found.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_view_memos_empty_file(self, mock_stdout):
        # Create an empty test_memos.txt
        open(self.test_memo_file, 'w').close()
        self.assertTrue(os.path.exists(self.test_memo_file)) # Ensure it's there
        statinfo = os.stat(self.test_memo_file)
        self.assertEqual(statinfo.st_size, 0) # Ensure it's empty

        view_memos()
        self.assertEqual(mock_stdout.getvalue().strip(), "No memos found.")
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_view_memos_with_memos(self, mock_stdout):
        add_memo("First memo for viewing")
        add_memo("Second memo for viewing")
        
        view_memos()
        
        expected_output_lines = [
            "1. First memo for viewing",
            "2. Second memo for viewing"
        ]
        # Get all printed lines, stripping each one, and filter out empty lines that might result from splitting.
        actual_output_lines = [line.strip() for line in mock_stdout.getvalue().strip().split('\n') if line.strip()]
        
        self.assertEqual(len(actual_output_lines), len(expected_output_lines))
        for i, expected_line in enumerate(expected_output_lines):
            self.assertEqual(actual_output_lines[i], expected_line)


    # --- Tests for delete_memo ---
    def test_delete_single_memo_successfully(self):
        add_memo("To be deleted")
        add_memo("To remain")
        delete_memo("1") # Delete "To be deleted"
        
        with open(self.test_memo_file, "r") as f:
            content = f.readlines()
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].strip(), "To remain")

    def test_delete_one_of_multiple_memos(self):
        memos_to_add = ["Memo A", "Memo B", "Memo C", "Memo D"]
        for m in memos_to_add:
            add_memo(m)
        
        # Delete "Memo B" (which is number 2)
        delete_memo("2")
        
        with open(self.test_memo_file, "r") as f:
            content = [line.strip() for line in f.readlines()]
        
        expected_remaining_memos = ["Memo A", "Memo C", "Memo D"]
        self.assertEqual(len(content), len(expected_remaining_memos))
        for i, expected_memo in enumerate(expected_remaining_memos):
            self.assertEqual(content[i], expected_memo)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_memo_no_file(self, mock_stdout):
        # Ensure file does not exist
        if os.path.exists(self.test_memo_file):
            os.remove(self.test_memo_file)
        delete_memo("1")
        self.assertEqual(mock_stdout.getvalue().strip(), "No memos to delete.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_memo_empty_file(self, mock_stdout):
        open(self.test_memo_file, 'w').close() # Create empty file
        delete_memo("1")
        self.assertEqual(mock_stdout.getvalue().strip(), "No memos to delete.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_memo_invalid_number_out_of_bounds_too_high(self, mock_stdout):
        add_memo("Only memo")
        delete_memo("2") # Try to delete memo 2 when only 1 exists
        self.assertEqual(mock_stdout.getvalue().strip(), "Error: Invalid memo number. Please enter a number between 1 and 1.")
        # Check that the memo was not deleted
        with open(self.test_memo_file, "r") as f:
            content = f.readlines()
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].strip(), "Only memo")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_memo_invalid_number_out_of_bounds_zero(self, mock_stdout):
        add_memo("First and only memo")
        delete_memo("0") # Try to delete memo 0
        self.assertEqual(mock_stdout.getvalue().strip(), "Error: Invalid memo number. Please enter a number between 1 and 1.")
        with open(self.test_memo_file, "r") as f:
            content = f.readlines()
        self.assertEqual(len(content), 1)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_memo_invalid_number_non_integer(self, mock_stdout):
        add_memo("A memo")
        delete_memo("abc")
        self.assertEqual(mock_stdout.getvalue().strip(), "Error: Invalid input. Memo number must be an integer.")
        with open(self.test_memo_file, "r") as f:
            content = f.readlines()
        self.assertEqual(len(content), 1)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_memo_prints_confirmation(self, mock_stdout):
        add_memo("Test Memo for Deletion Confirmation")
        delete_memo("1")
        # The actual output from delete_memo includes the content of the deleted memo
        self.assertIn("Memo 1 ('Test Memo for Deletion Confirmation') deleted.", mock_stdout.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
