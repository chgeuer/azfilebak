"""Unit tests for backupconfiguration."""
import os
import json
import unittest
from mock import patch
from azfilebak.backupconfiguration import BackupConfiguration
from azfilebak.azurevminstancemetadata import AzureVMInstanceMetadata
from tests.loggedtestcase import LoggedTestCase

class TestBackupConfiguration(LoggedTestCase):
    """Unit tests for class BackupConfiguration."""

    def setUp(self):
        self.json_meta = open('sample_instance_metadata.json').read()

        self.meta = AzureVMInstanceMetadata(
            lambda: (json.JSONDecoder()).decode(self.json_meta)
        )

        self.patcher1 = patch('azfilebak.azurevminstancemetadata.AzureVMInstanceMetadata.create_instance',
                              return_value=self.meta)
        self.patcher1.start()

        self.cfg = BackupConfiguration(config_filename="sample_backup.conf")

    def test_cfg_file_value(self):
        """test cfg_file_value"""
        self.assertEqual(self.cfg.cfg_file_value('local_temp_directory'), '/tmp')

    def test_get_vm_name(self):
        """test get_vm_name"""
        self.assertEqual(self.cfg.get_vm_name(), 'hec99v106014')

    def test_get_subscription_id(self):
        """test get_subscription_id"""
        self.assertEqual(self.cfg.get_subscription_id(), '2e394ee6-2714-4080-88c3-ecfc33d85147')

    def test_get_azure_storage_account_name(self):
        """test get_azure_storage_account_name"""
        self.assertEqual(self.cfg.get_azure_storage_account_name(), 'sahec99az1backup0001')

    def test_get_backup_command(self):
        """test get_commandline"""
        self.assertEqual(self.cfg.get_backup_command('tmp_dir'), 'tar cvzf - /tmp --ignore-failed-read')
        self.assertEqual(self.cfg.get_backup_command('osdisk'),
                         'tar cvzf - / --exclude /dev --exclude /proc --exclude /run --exclude /sys')

    def test_get_restore_command(self):
        """test get_commandline"""
        self.assertEqual(self.cfg.get_restore_command('tmp_dir'), 'tar xvzf -')
        self.assertEqual(self.cfg.get_restore_command('osdisk'), 'tar xvzf -')

    def test_get_filesets(self):
        """test get_filesets"""
        filesets = self.cfg.get_filesets()
        self.assertIn('tmp_dir', filesets)
        self.assertIn('osdisk', filesets)
        self.assertIn('testecho', filesets)

    def test_get_fileset_sources(self):
        """test get_fileset_sources"""
        self.assertEqual(self.cfg.get_fileset_sources('ci'), '/tmp')
        self.assertEqual(self.cfg.get_fileset_sources('hana'), '/tmp')
        self.assertEqual(self.cfg.get_fileset_sources('ase'), '/tmp')

    def test_get_fileset_exclude(self):
        """test get_fileset_sources"""
        self.assertEqual(self.cfg.get_fileset_exclude('ci'), '/install')
        self.assertEqual(self.cfg.get_fileset_exclude('hana'), '/install,/hana/log/AZ3,/hana/data/AZ3,/hana_backup/AZ3/log,/hana_backup/AZ3/data')
        self.assertEqual(self.cfg.get_fileset_exclude('ase'), '/install,/sybase/AZ3/saparch_1,/sybase/AZ3/sapdata_1,/sybase/AZ3/saplog_1,/sybase/AZ3/saptemp_1')

    def test_storage_client(self):
        """test storage_client"""
        if not os.environ.has_key('STORAGE_KEY'):
            return True
        client = self.cfg.storage_client
        self.assertEqual(client.protocol, 'https')

    def tearDown(self):
        self.patcher1.stop()

if __name__ == '__main__':
    unittest.main()
