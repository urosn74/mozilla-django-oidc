from django.test import TestCase, override_settings

from mozilla_django_oidc.configuration import NamedConfigurationProvider


class NamedConfigurationProviderTestCase(TestCase):

    def test_set_configuration_name(self):
        self.assertIsNone(NamedConfigurationProvider.get_configuration_name())
        NamedConfigurationProvider.set_configuration_name('config1')
        self.assertEqual(NamedConfigurationProvider.get_configuration_name(), 'config1')
        NamedConfigurationProvider.set_configuration_name('config2')
        self.assertEqual(NamedConfigurationProvider.get_configuration_name(), 'config2')

    @override_settings(OIDC_NAMED_CFG={'config1': {'itemx': 'success'}})
    def test_value_is_extracted_from_named_configuration(self):
        provider = NamedConfigurationProvider()
        NamedConfigurationProvider.set_configuration_name('config1')
        self.assertEqual(provider.get_settings('itemx'), 'success')

    @override_settings(OIDC_TEST_VALUE2='default')
    @override_settings(OIDC_NAMED_CFG={'config1': {'OIDC_TEST_VALUE1': 'error'}})
    def test_value_is_extracted_from_default_settings(self):
        provider = NamedConfigurationProvider()
        NamedConfigurationProvider.set_configuration_name('config1')
        self.assertEqual(provider.get_settings('OIDC_TEST_VALUE2'), 'default')
