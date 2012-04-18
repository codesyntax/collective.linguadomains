from zope import component
from plone.registry.interfaces import IRegistry
from collective.linguadomains import interfaces
from plone.app.layout.viewlets import common
import os
from urlparse import urlparse

import logging
logger = logging.getLogger('collective.linguadomains')
from plone.app.layout.viewlets.common import ViewletBase

class URLValidator(ViewletBase):
    """Viewlet that check language of the content page against translated url
    if the language do not correspond to the content you will be redirected
    to the same page with the corresponding URL
    """
    def __init__(self, context, request, view, manager=None):
        super(URLValidator, self).__init__(context, request, view,
                                           manager=manager)
        self.tests = None
        self._settings = None
        self._portal_url = None

    def index(self):
        """This viewlet check stuff, it doesn't display anythings"""
        return u""

    def _plone_portal_state(self):
        return component.queryMultiAdapter((self.context, self.request),
                                           name="plone_portal_state")

    def portal_url(self):
        if self._portal_url is None:
            pstate = self._plone_portal_state()
            self._portal_url = pstate.portal_url()
        return self._portal_url

    def language(self):
        return self.context.Language()

    def settings(self):
        if self._settings is None:
            registry = component.queryUtility(IRegistry)
            if registry is None:
                logger.info('no registry')
                return
        
            self._settings = registry.forInterface(interfaces.ISettingsSchema,
                                                    check=False)
        return self._settings

    def update(self):
        request = self.request
        if self.request.get('donotcheck'):
            return

        purl = self.portal_url()
        lang = self.language()
        settings = self.settings()

        purl_parsed = urlparse(purl)
        url_parsed = urlparse(request.get('ACTUAL_URL'))

        if not settings:
            return

        if not settings.activated:
            return

        mapping_raw = settings.mapping
        mapping = {}
        for value in mapping_raw:
            url , langcode = value.split('|')
            mapping[langcode] = url

        if not mapping:
            return

        if not purl in mapping.values():
            logger.info('URL not configured')
            return

        waited_url = mapping.get(lang,None)
        if waited_url is None:
            logger.info('Language not configured')
            return
        waited_url_parsed = urlparse(waited_url)

        if purl  == waited_url:
            return

        base_path = purl_parsed.path
        waited_path = url_parsed.path
        redirect_url = waited_url + waited_path[len(base_path):]
    
        request.RESPONSE.redirect(redirect_url)
        logger.info('REDIRECT')
