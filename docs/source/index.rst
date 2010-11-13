.. Contentlet documentation master file, created by
   sphinx-quickstart on Sun May 23 13:14:37 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Contentlet — UI framework for web
=================================

Contentlet is a framework for creating composable and reusable UI for web. It
is designed by looking at `zope.contentprovider
<http://pypi.python.org/pypi/zope.contentprovider>`_ and `zope.viewlet
<http://pypi.python.org/pypi/zope.viewlet>`_ and for using with `Pyramid
<http://docs.pylonshq.com/>`_ web framework (formerly known as 
`repoze.bfg` <http://bfg.repoze.org>).

.. toctree::
   :maxdepth: 2

Introduction
============

Contentlet operates with content providers. Content provider is a piece of code
that provides some logically complete part of UI, for example twitter stream or
toolbar.

So, the template writer provides template with point, where content providers
will be invoked. This looks like a macros system, but it isn't.  Content
provider invokation and configuration are decoupled, so one can write where he
want to see any specific content provider and other — what content provider
will be seen there.

Content providers
=================

So, what is the content provider? It is function of two arguments::

    def my_contentprovider(context, request):
        return "A piece of UI."

or any callable object, for example::

    class MyContentProvider(object):

        def __call__(self, context, request):
            return "A piece of UI."

Content providers look like a simple views (in MTV frameworks, like Pyramid)
and they are even can be registered as views and vice-versa. So content
provider can be rendered as separate page and can be embedded in another page.

Configuring content providers
=============================

Content providers can be registered by name and for specific request's context. There are two ways for registering content providers for application:

* Imperative, via ``contentlet.Configurator``.

* Declarative, with ZCML directive ``contentprovider``.

Imperative configuration
------------------------

If you use Pyramid amd don't want to hook the global component registry with
hook_zca(), you need to register ``contentlet.expression.ProviderExpression`` 
as a utility in the global component registry::

  from chameleon.zpt.interfaces import IExpressionTranslator
  from contentlet.expression import ProviderExpression
  from zope.component import provideUtility

  provideUtility(ProviderExpression(), IExpressionTranslator,
                 name='contentprovider')


For configuring you application imperatively, you should use ``contentlet.Configurator`` object::

    ...
    import contentlet

    config = contentlet.Configurator(registry=you_application_registry)
    config.add_content_provider(my_contentprovider, "name")
    ...

or if you want to register content provider for specific context::

    ...
    import contentlet

    config = contentlet.Configurator(registry=you_application_registry)
    config.add_content_provider(my_contentprovider, "name", context=MyContext)
    ...

But where ``you_application_registry`` comes from? Often it is registry, that
was created by ``pyramid.configuration.Configurator`` object, so the more
full piece of configuration code looks like this::


    ...
    import pyramid
    import contentlet

    pyramid_config = pyramid.configuration.Configurator()
    pyramid_config.add_view(my_view)
    config = contentlet.Configurator(registry=pyramid_config.registry)
    config.add_content_provider(my_contentprovider, "name", context=MyContext)
    ...

We need to create two objects for configuring our application (Pyramid and
contentlet configurators), sometimes it is better to cook own configurator.
There is ``ContentletConfiguratorMixin`` comes to mind::

    ...
    from pyramid.configuration import Configurator as PyramidConfigurator
    from contentlet import ContentletConfiguratorMixin

    class Configurator(PyramidConfigurator, ContentletConfiguratorMixin):
        pass

    config = Configurator()
    config.add_view(my_view)
    config.add_content_provider(my_contentprovider, "name", context=MyContext)
    ...

So our custom ``Configurator`` object now suitable to configure both Pyramid and
contentlet aspects of application configuration.

Declarative configuration
-------------------------

If you use Contentlet in a Pyramid application and want to use 
declarative configuration you have to call 
``pyramid.configuartion.Contfigurator().hook_zca()``
when you initialize your application.

Declarative configuration can be made with ``contentprovider`` ZCML directive::

    <configure>
        <include package="contentlet" />

        <contentprovider
            provider="mypackage.myprovider"
            name="name"
            />
    </configure>

or for registering content provider for specific context::

    <configure>
        <include package="contentlet" />

        <contentprovider
            provider="mypackage.myprovider"
            name="name"
            context="mypackage.models.MyContext"
            />
    </configure>

Note, that you should include ZCML configuration from ``contentlet`` package in
order to use ``contentprovider`` ZCML directive.

Using content providers
=======================

After registering some content providers, it is always good to query and use
them later in view or template code.

Using content providers inside views
------------------------------------

For using content providers inside views, you should use
``contentlet.get_provider`` or ``contentlet.query_provider`` function. The
difference between them is the only handling of failure of content provider
lookup. The ``contentlet.get_provider`` will raise ``LookupError`` while
``contentlet.query_provider`` will just return ``None`` value.

For query content provider by name and then render it in variable::

    ...
    from contentlet import query_provider
    provider = query_provider("provider_name")
    rendered = provider(request, context)
    ...

You can also query provider that is specific to context::

    ...
    from contentlet import query_provider
    provider = query_provider("provider_name", context=context)
    rendered = provider(request, context)
    ...

By default, ``contentlet.query_provider`` and ``contentlet.get_provider`` will
use global ZCA registry for lookups. This is not desired behaviour while using
Pyramid web-framework, cause it uses per-application registry. View code can
get it via request's ``registry`` attribiute, so querying content providers in
Pyramid's view usually done in following way::

    ...
    from contentlet import query_provider
    provider = query_provider("provider_name", registry=request.registry)
    rendered = provider(request, context)
    ...

So, ``registry`` keyword argument specify what component registry to use for
content provider lookup.

Using content providers inside Chameleon templates
--------------------------------------------------

Usually it is better to use content providers from inside templates than from
views. Pyramid comes with `Chameleon <http://chameleon.repoze.org/>`_
templating engine and Contentlet provides custom TALES expression translator
for rendering content providers::

    <div tal:replace="contentprovider:name"></div>

This ``div`` element will be replace with piece of markup, returned by content
provider with name ``name``.

.. warning::
    Temlate should have access for Pyramid request object via `request`
    variable. It can be done via passing current request from views or using
    renderers, which automatically do that.
