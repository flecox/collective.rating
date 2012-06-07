# Zope imports
import json

from zope.interface import Interface
from five import grok
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

# Local imports
from interfaces import IAddonSpecific, IThemeSpecific

from collective.rating.behavior import IRating

grok.templatedir("templates")
grok.layer(IAddonSpecific)

class RatingsView(grok.View):
    grok.context(Interface)
    grok.name("rating_view")
    grok.require("zope2.View")

    def update(self):
        try:
            rating = IRating(self.context)
        except TypeError:
            #the content is not adapted by IRating
            pass
        if rating and 'rate' in self.request.keys():
            user = self.get_user_id()
            rating.ratings[user] = int(self.request['rate'])
            self.context.ratings[user] = int(self.request['rate'])
        self.rating = rating.get_rating()
    
    def render(self):
        if 'rate_from' in self.request.keys() and \
            self.request['rate_from'] == "ajax":
            return json.dumps({"number":self.rating})
        else:
            return "";
    
    def get_user_id(self):
        membership_tool = getToolByName(self.context, 'portal_membership')
        user = membership_tool.getAuthenticatedMember()
        return user.getMemberId()
