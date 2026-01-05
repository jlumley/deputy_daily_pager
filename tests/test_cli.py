import unittest

from run import parse_notify_list, validate_positive_int


class TestCliHelpers(unittest.TestCase):
    def test_parse_notify_list_empty(self):
        self.assertEqual(parse_notify_list(None), None)
        self.assertEqual(parse_notify_list(""), [])

    def test_parse_notify_list_values(self):
        self.assertEqual(parse_notify_list("123"), [123])
        self.assertEqual(parse_notify_list("123,456"), [123, 456])
        self.assertEqual(parse_notify_list(" 123 , 456 "), [123, 456])

    def test_validate_positive_int(self):
        self.assertEqual(validate_positive_int("7"), 7)
        with self.assertRaises(ValueError):
            validate_positive_int("0")
        with self.assertRaises(ValueError):
            validate_positive_int("-2")


if __name__ == "__main__":
    unittest.main()
