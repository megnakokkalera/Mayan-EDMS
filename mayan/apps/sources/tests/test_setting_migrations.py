from __future__ import unicode_literals

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin

from ..settings import setting_staging_file_image_cache_storage_arguments


class SourceSettingMigrationTestCase(
    SmartSettingTestMixin, BaseTestCase
):
    def test_setting_staging_file_image_cache_storage_arguments_0001_migration(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_staging_file_image_cache_storage_arguments
        self.test_config_value = '{}'.format(test_value)
        self._create_test_config_file()

        self.assertEqual(
            setting_staging_file_image_cache_storage_arguments.value,
            test_value
        )

    def test_setting_staging_file_image_cache_storage_arguments_0001_migration_with_dict(self):
        test_value = {'location': 'test value'}

        self.test_setting = setting_staging_file_image_cache_storage_arguments
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_staging_file_image_cache_storage_arguments.value,
            test_value
        )
