import unittest
import requests

url = "http://localhost:8000"


class TestStringMethods(unittest.TestCase):
    # test function
    def test_params_and_add(self):
        resp = requests.get(url + '/params')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json())
        requests.post(url + '/add_val_1')
        resp = requests.get(url + '/params')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json())
        requests.post(url + '/add_par_A')
        resp = requests.get(url + '/params')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(['A'], resp.json())

    def test_evaluate(self):
        vals = [1, 2, 3]
        pars = {'A': 1, 'B': 2, 'C': 3}
        for x in vals:
            requests.post(url + '/add_val_' + str(x))
        for (n, _) in pars:
            requests.post(url + 'add_par_' + n)
        resp = requests.post(url + '/eval', data=pars)
        self.assertEqual(12, resp.json())


if __name__ == '__main__':
    unittest.main()