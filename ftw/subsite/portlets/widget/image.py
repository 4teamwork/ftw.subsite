"""
Copied from elyself.portlets.image
the image portlet is not working proper under plone 3.0.6
"""
from Acquisition import aq_inner
from zope.publisher.browser import BrowserView


class ImageView(BrowserView):
    '''
    View the image field of the image portlet. We steal header details
    from zope.app.file.browser.file and adapt it to use the dublin
    core implementation that the Image object here has.
    '''

    def __call__(self):
        context = aq_inner(self.context)
        image = context.image
        self.request.response.setHeader('Content-Type', image.contentType)
        self.request.response.write(image.data)
