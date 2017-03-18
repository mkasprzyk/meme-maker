import unittest
from unittest.mock import MagicMock, patch, mock_open

from meme_maker.plugins import (
    Plugin,
    PluginMeta,
    PluginsLoader,
    PluginValidator
)

fake_meta = {
    #Required fake fields
    'name': 'fake',
    'version': 0,
    'scm': 'http://fake.git.repo',
    'script': 'fake.py',
    #Optional fake fields
    'author': 'Fake Author',
    'email': 'fake@email.co',

}

class PluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()
        self.plugin.meta = fake_meta

    def test_name_attr_returns_meta_name(self):
        self.assertEqual(self.plugin.name, fake_meta['name'])

    def test_version_attr_returns_meta_version(self):
        self.assertEqual(self.plugin.version, fake_meta['version'])

    def test_scm_attr_returns_meta_scm(self):
        self.assertEqual(self.plugin.scm, fake_meta['scm'])

    def test_script_attr_returns_meta_script_without_extension(self):
        script, ext = fake_meta['script'].split('.')
        self.assertEqual(self.plugin.script, script)

    def test_author_attr_returns_meta_author(self):
        self.assertEqual(self.plugin.author, fake_meta['author'])

    def test_email_attr_returns_meta_email(self):
        self.assertEqual(self.plugin.email, fake_meta['email'])


class PluginMetaTestCase(unittest.TestCase):
    @patch('meme_maker.plugins.yaml')
    def setUp(self, mock_yaml):
        self.meta = PluginMeta('fake')


    def test_plugins_path(self):
        print(self.meta.plugins_path)

class PluginLoaderTestCase(unittest.TestCase):
    pass

class PluginValidatorTestCase(unittest.TestCase):
    pass