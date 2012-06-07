import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form.browser.text import TextWidget
from z3c.form.widget import FieldWidget
from z3c.form.converter import BaseDataConverter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.rating import _
from collective.rating.widgets.interfaces import IRatingWidget

STARS_NUMBER = 5

class RatingWidget(TextWidget):
    """Input type upload widget implementation."""
    zope.interface.implementsOnly(IRatingWidget)
    
    template = ViewPageTemplateFile('rating_template.pt')
    
    klass = u'rating-widget'
    
    def render(self):
        return self.template(self)
    
    def rate_url(self, number=None):
        url = self.context.absolute_url() + "/rating_view"
        if number:
            url += "?rate=%s" % number
        return url
    
    def stars(self):
        return [i for i in range(1,STARS_NUMBER+1)]
    
    def is_rated(self, number):
        return number <= self.value

@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def RatingFieldWidget(field, request):
    """IFieldWidget factory for RatingWidget."""
    return FieldWidget(field, RatingWidget(request))


class RatingDataConverter(BaseDataConverter):
    """A general data converter for numbers."""
    
    zope.component.adapts(
        zope.schema.interfaces.IDict, IRatingWidget)
    type = dict
    errorMessage = _('The entered value is not a valid integer literal.')

    def __init__(self, field, widget):
        super(RatingDataConverter, self).__init__(field, widget)

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value:
            return self.get_rating(value.values())
        return 0

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        return ''

    def get_rating(self, values):
        result = 0
        for value in values:
            result += value
        if values:
            result = result/len(values)
        return result