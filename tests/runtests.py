import glob
import os
import unittest


def build_test_suite():
    suite = unittest.TestSuite()

    for test_case in glob.glob('tests/test_*.py'):
        modname = os.path.splitext(test_case)[0]
        modname = modname.replace('/', '.')
        module = __import__(modname, {}, {}, ['1'])
        suite.addTest(unittest.TestLoader().loadTestsFromModule(module))

    return suite


if __name__ == "__main__":
    suite = build_test_suite()
    runner = unittest.TextTestRunner()

    runner.run(suite)
