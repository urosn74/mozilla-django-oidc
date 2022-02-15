import threading

from mozilla_django_oidc.utils import import_from_settings, resolve_from_name


provider_instance = None


class OidcConfigurationProvider:

    def get_settings(self, attr, *args):
        raise NotImplemented()

    @staticmethod
    def get_provider():
        global provider_instance
        if provider_instance is None:
            provider_name = import_from_settings(
                'OIDC_CONFIGURATION_PROVIDER',
                'mozilla_django_oidc.configuration.DefaultConfigurationProvider'
            )
            provider_class = resolve_from_name(provider_name)
            provider_instance = provider_class()
        return provider_instance


class DefaultConfigurationProvider(OidcConfigurationProvider):
    """ Provides configuration parameters extracted from Django settings
        file.
    """
    def get_settings(self, attr, *args):
        return import_from_settings(attr, *args)


class NamedConfigurationProvider(OidcConfigurationProvider):
    context = threading.local()

    @classmethod
    def set_configuration_name(cls, name):
        cls.context.name = name

    @classmethod
    def get_configuration_name(cls):
        return getattr(cls.context, 'name', None)

    def get_settings(self, attr, *args):
        named_cfg = import_from_settings('OIDC_NAMED_CFG', None)
        name = NamedConfigurationProvider.get_configuration_name()
        if named_cfg and name in named_cfg:
            val = named_cfg[name].get(attr, None)
            if val is not None:
                return val
        return import_from_settings(attr, *args)
