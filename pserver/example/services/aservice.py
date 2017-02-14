from plone.server import configure
from plone.server.api.service import Service
from plone.server.interfaces import ISite
from plone.server.browser import Response

# SEE the official services documentation for more info:
# http://ploneserver.readthedocs.io/en/latest/services.html

# plone.server.configure.service is a decorator that helps remove
# the need for separated configuration via ZCML or some such. When
# the application this service belongs to is started, a scan will
# run from the modules __init__.py (IE pserver/example/__init__.py#includeme)
# which will load all modules configured there.
# SEE: http://ploneserver.readthedocs.io/en/latest/applicationconfiguration.html#service
@configure.service(
    # this is going to generally be ISite by default -- but you'll start
    # wanting to change this as you add different content types that are
    # defined by various _interfaces_
    # SEE: http://ploneserver.readthedocs.io/en/latest/contenttypes.html
    # ALSO: customtypeservice.py in this folder
    context=ISite,
    # this is the name of the endpoint as seen in the URL -- EX:
    # http://127.0.0.1/zodb/plone/@jsonresponseclass
    name='@jsonresponseclass',
    # the HTTP method this endpoint accepts
    method='GET',
    # the permission that applies to this end point, for more documentation,
    # see: http://ploneserver.readthedocs.io/en/latest/roles.html
    permission='plone.AccessPreflight')
# the actual service (AKA "view") code can be either a _class_ or
# a _function_ (see below).
class JSONResponse(Service):
    # if a class, then the __call__ method will be the entry point into
    # the service
    async def __call__(self):
        context = self.context
        request = self.request

        # return values of particular types are automatically turned into
        # appropriate HTTP responses:
        # - dictionary: this will get output as a JSON document
        # - list: this will also get output as a JSON document
        # - string: this will get output as an HTML document
        # - None: this will get output as an empty JSON document
        # - plone.server.browser.Response: this will get output nearly as-is
        #   because it's assumed that you know how you want your response
        #   structured -- basically this is the 100% custom option without
        #   having to create a renderer and go through a bunch more
        #   custom configuration of plone.server (which you _absolutely_
        #   can still do, if it fits your need)
        return dict(foo='bar')


# This is an example of using a function to define the service instead of
# a class. It's basically the same without the object, and getting the
# context and request as parameters.
@configure.service(
    context=ISite,
    name='@jsonresponsefunc',
    method='GET',
    permission='plone.AccessPreflight')
async def JSONResponseFunc(context, request):
    return {'foo':['bar','baz']}
