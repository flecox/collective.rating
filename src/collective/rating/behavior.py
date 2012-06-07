from rwproperty import getproperty, setproperty

from zope import schema
from zope.interface import implements, alsoProvides
from zope.component import adapts

from z3c.form.interfaces import IDisplayForm

from plone.directives import form
from plone.app.dexterity.behaviors.metadata import MetadataBase
from plone.app.dexterity.behaviors.metadata import DCFieldProperty

from Products.CMFCore.interfaces import IDublinCore

from collective.rating import MessageFactory as _
from collective.rating.widgets.rating_widget import RatingFieldWidget

class IRating(form.Schema):
    """Add tags to content
    """
    form.omitted('ratings')
    form.no_omit(IDisplayForm, 'ratings')
    form.widget(ratings=RatingFieldWidget)
    ratings = schema.Dict(
        key_type = schema.TextLine(title=u'user'),
        value_type = schema.Int(title=u'rating'),
        required=False)

alsoProvides(IRating, form.IFormFieldProvider)

class Rating(MetadataBase):
    ratings = DCFieldProperty(IRating['ratings'])
    
    def get_rating(self):
        result = 0
        values = self.ratings.values()
        for value in values:
            result += value
        if values:
            result = result/len(values)
        return result