import unittest2 as unittest
from collective.linguadomains.tests import base

class IntegrationTestSetup(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def test_controlpanel(self):
        self.portal.portal_controlpanel

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)