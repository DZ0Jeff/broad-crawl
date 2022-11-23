import unittest
from main import get_base_domain


class TestDomain(unittest.TestCase):
    def test_domain(self):
        urls = ["http://www.azuramedicalspa.com/", "http://azuramedicalspa.com/"]
        for url in urls:
            print(get_base_domain(url, partial=True))


if __name__ == "__main__":
    unittest.main()
