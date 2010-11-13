0.2
---

* contentprovider zcml directive: Put the directive into it's the own 
  namespace "http://braintrace.ru/contentlet" and move the registration
  from configure.zcml to meta.zcml.

* Change component registrations and lookups to make declerative 
  configuration work with Pyramid without the need to use hook_zca()
  or share the global registry.

* port from repoze.bfg to Pyramid

* Added ``contentlet.provider.render_`` as shortcut for rendering providers.

* Do not depend on repoze.bfg at all.

* For all component registrations and lookups use hookable getSiteManager API.

0.1.1
-----

* Fixed missed import of ``ContentletConfiguratorMixin``.

0.1
---

* Implementation of content provider pattern (zope.contentprovider).

* Imperative API for configuration.
