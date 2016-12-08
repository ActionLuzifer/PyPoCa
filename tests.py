#!/usr/bin/python3
# coding=utf-8
'''
Created on 2013-01-31

@author: actionluzifer
'''

import unittest

import source.Tests.RSS20Test as RSS20Test
import source.Tests.PyPoCaTest as PyPoCaTest
import sys


def getTestSuiteFromModule(Module):
    loader = unittest.TestLoader()
    testsuite = loader.loadTestsFromModule(Module)
    #testsuite = loader.loadTestsFromTestCase(Module)
    return testsuite


testsuite = getTestSuiteFromModule(RSS20Test)
runner = unittest.TextTestRunner(sys.stdout, verbosity=2)
result = runner.run(testsuite)

testSuite = unittest.TestLoader().loadTestsFromTestCase(PyPoCaTest.PyPoCaTestCase)
unittest.TextTestRunner(verbosity=2).run(testSuite)