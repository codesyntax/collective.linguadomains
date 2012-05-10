from zope import interface
from zope import schema
from zope import i18nmessageid

from plone.z3cform import layout
from plone.app.registry.browser import controlpanel as base
from plone.registry import field
_ = i18nmessageid.MessageFactory('collective.domainvalidator')

class ISettingsSchema(interface.Interface):
    """Settings for this addon"""

    activated = schema.Bool(title=_(u"Is activated"),
                            description=_(u"Uncheck to unactivate this addon"),
                            default=True)

    mapping = schema.List(title=_(u"URL - Language mapping"),
                          default=[],
                          value_type=field.URI(title=_(u"URL|LANG"),
                                               description=_(u"http://mysite.com|en")))


class ControlPanelForm(base.RegistryEditForm):
    schema = ISettingsSchema
    label = _(u"Domain validator control panel")
    #TODO: validate all urls !!!!
    
    def extractData(self):
        data, errors = super(ControlPanelForm, self).extractData()
        import pdb;pdb.set_trace()

    def validate_mapping(self, mapping):
        pass

class ControlPanelView(base.ControlPanelFormWrapper):
    form = ControlPanelForm
