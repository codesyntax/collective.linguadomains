import unittest2 as unittest
from collective.linguadomains.tests import base, utils
from collective.linguadomains import validator

class UnitTestValidator(base.UnitTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def setUp(self):
        context = utils.FakeContext()
        request = utils.FakeRequest()
        self.viewlet = validator.URLValidator(context, request, None)
        self.viewlet._settings = utils.FakeSettings()

    def test_not_configure_url(self):
        viewlet = self.viewlet
        viewlet._portal_url = 'http://nohost/plone'
        viewlet.update()

        self.assertTrue(self.viewlet.request.RESPONSE.redirect_url is None)

    def test_good_url(self):
        viewlet = self.viewlet
        viewlet._portal_url = 'http://nohost-fr/plone'
        viewlet.context.lang = 'fr'
        viewlet.update()
        redirect_url = self.viewlet.request.RESPONSE.redirect_url
        self.assertTrue(redirect_url is None)

    def test_should_redirect(self):
        viewlet = self.viewlet
        viewlet._portal_url = 'http://nohost-fr/plone'
        viewlet.context.lang = 'nl'
        viewlet.update()
        self.assertEqual(self.viewlet.request.RESPONSE.redirect_url,
                        'http://nohost-nl/plone/news')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)