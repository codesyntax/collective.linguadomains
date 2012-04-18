import unittest2 as unittest
from collective.linguadomains import validator

class IntegrationTestValidator(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def setUp(self):
        super(IntegrationTestValidator, self).setup()

    def test_not_configure_url(self):
        pass

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)