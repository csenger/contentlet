""" Configuration for content providers."""

from zope.interface import Interface
from zope.interface import implementedBy
from zope.interface.interfaces import IInterface
from zope.component import getSiteManager

from contentlet.interfaces import IContentProvider

__all__ = ["Configurator",
           "ContentletConfiguratorMixin"]


class ContentletConfiguratorMixin(object):
    """ Mixin for using with pyramid.configuration.Configurator."""

    def add_content_provider(self, provider, name, context=None):
        """ Add content provider."""
        if context is None:
            context = Interface
        if not IInterface.providedBy(context):
            context = implementedBy(context)
        self.registry.registerAdapter(
            provider, (context,), IContentProvider, name=name)


class Configurator(ContentletConfiguratorMixin):
    """ Configurator for contentlet."""

    def __init__(self, registry=None):
        if registry is None:
            registry = getSiteManager()
        self.registry = registry
