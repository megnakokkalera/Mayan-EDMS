from __future__ import unicode_literals

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin

from ..settings import setting_storage_backend_arguments


class DocumentSignaturesSettingMigrationTestCase(
    SmartSettingTestMixin, BaseTestCase
):
    def test_signatures_storage_backend_arguments_0001_migration(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_storage_backend_arguments
        self.test_config_value = '{}'.format(test_value)
        self._create_test_config_file()

        self.assertEqual(
            setting_storage_backend_arguments.value,
            test_value
        )

    def test_signatures_storage_backend_arguments_0001_migration_with_dict(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_storage_backend_arguments
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_storage_backend_arguments.value,
            test_value
        )
