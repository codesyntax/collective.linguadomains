import unittest2 as unittest
from collective.linguadomains.tests import base, utils
from collective.linguadomains import validator

class UnitTestSetup(base.UnitTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def test_not_configure_url(self):
        event = utils.FakeEvent()
        event.tests['purl'] = 'http://nohost/plone'
        validator.domainValidator(None, event)
        self.assertTrue(event.request.RESPONSE.next_url is None)
        #no redirection happens

    def test_already_good_url(self):
        event = utils.FakeEvent()
        event.tests['purl'] = 'http://nohost-en/plone'
        event.tests['lang'] = 'fr'
        validator.domainValidator(None, event)
        self.assertTrue(event.request.RESPONSE.next_url is None)

        event.tests['purl'] = 'http://nohost-fr/plone'
        event.tests['lang'] = 'en'
        validator.domainValidator(None, event)
        self.assertTrue(event.request.RESPONSE.next_url is None)

        event.tests['purl'] = 'http://nohost-nl/plone'
        event.tests['lang'] = 'nl'
        validator.domainValidator(None, event)
        self.assertTrue(event.request.RESPONSE.next_url is None)

    def test_should_redirect(self):
        event = utils.FakeEvent()
        event.tests['purl'] = 'http://nohost-en/plone/news'
        event.tests['lang'] = 'fr'
        validator.domainValidator(None, event)
        self.assertTrue(event.request.RESPONSE.next_url,
                        'http://nohost-fr/plone/news')

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)