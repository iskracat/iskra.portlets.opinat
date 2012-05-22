from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

# TODO: If you define any fields for the portlet configuration schema below
# do not forget to uncomment the following import
from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from plone.memoize.view import memoize

# TODO: If you require i18n translation for any of your schema fields below,
# uncomment the following to import your package MessageFactory
from iskra.porltets.opinat import LogosOpinatMessageFactory as _


class INPSOpinat(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    url = schema.TextLine(title=_(u"URL to get"),
                             description=_(u"SOAP SERVICE"),
                             required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(INPSOpinat)

    # TODO: Set default values for the configurable parameters here

    url = 'http://bo.opinat.com/yii/index.php?r=wSNpsInfo/npsinfo'

    # TODO: Add keyword parameters for configurable parameters here
    def __init__(self, url='http://bo.opinat.com/yii/index.php?r=wSNpsInfo/npsinfo'):
        self.url = url

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "NPS Opinat"


import random
from suds.client import Client


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('npsopinat.pt')

    @memoize
    def demanarNumeros(self):
        client = Client(self.data.url)
        numeros = client.service.getNPSInfo('npsinf', 'fnispn9826', '', '', '', '')
        dades = numeros.split(';')
        servidas = dades[1]
        recividas = dades[2]
        servidas = servidas[:-3]+'.'+servidas[-3:]
        recividas = recividas[:-3]+'.'+recividas[-3:]
        return {'enviades': servidas, 'respostes': recividas}

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(INPSOpinat)

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(INPSOpinat)
