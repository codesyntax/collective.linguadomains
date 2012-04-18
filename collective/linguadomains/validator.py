from zope import component
from plone.registry.interfaces import IRegistry
from collective.linguadomains import interfaces
from plone.app.layout.viewlets import common
import os
from urlparse import urlparse

import logging
logger = logging.getLogger('test')

def domainValidator(site, event):
    """Event handler on before traverse to check domain constraints
    
    purl, lang and settings are for testing purpose
    """

    request = event.request

    if hasattr(event, 'tests'):
        purl = event.tests.get('purl')
        lang = event.tests.get('lang')
        settings = event.tests.get('settings')

    else:
        pstate = component.queryMultiAdapter((site, request),
                                       name="plone_portal_state")
        if pstate is None:
            logger.info('no pstate')
            return

        purl = pstate.portal_url()
        lang = pstate.language()

        registry = component.queryUtility(IRegistry)
        if registry is None:
            logger.info('no registry')
            return
    
        settings = registry.forInterface(interfaces.ISettingsSchema,
                                         check=False)

    purl_parsed = urlparse(purl)
    url_parsed = urlparse(request.get('ACTUAL_URL'))

    if not settings:
        logger.info('no settings')
        return

    if not settings.activated:
        logger.info('not activated')
        return

    mapping_raw = settings.mapping
    mapping = {}
    for value in mapping_raw:
        url , lang = value.split('|')
        mapping[lang] = url

    if not mapping:
        logger.info('no mapping')
        return

    if not purl in mapping.values():
        logger.info('portal url not in values')
        return

    waited_url = mapping[lang]
    waited_url_parsed = urlparse(waited_url)

    if purl  == waited_url:
        return

    #improve performance by trying to reduce html rendering
    request['ajax_load'] = True

    base_path = purl_parsed.path
    waited_path = url_parsed.path
    redirect_url = waited_url + waited_path[len(base_path):]

    request.RESPONSE.redirect(redirect_url)
    logger.info('REDIRECT !')
