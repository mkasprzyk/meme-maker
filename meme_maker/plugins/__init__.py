#!/usr/bin/env python
import os
import importlib

try:
    import yaml
except:
    #Ignore missing pyyaml for testing purposes
    yaml = None



class Plugin(object):
    def __init__(self):
        self.meta = None
        self.module = None

    @property
    def handler(self):
        handler_name = self.meta.get('handler')
        try:
            return getattr(self.module, handler_name)
        except Exception as exc:
            print(exc)
            return

    @property
    def name(self):
        return self.meta.get('name')

    @property
    def version(self):
        return self.meta.get('version')

    @property
    def scm(self):
        return self.meta.get('scm')

    @property
    def script(self):
        script, ext = self.meta.get('script').split('.')
        return script

    @property
    def author(self):
        return self.meta.get('author')

    @property
    def email(self):
        return self.meta.get('email')

    def __str__(self):
        return '<Plugin: {}>'.format(self.name)


class PluginMeta(object):
    default_meta_file = 'plugin.yaml'

    plugins_path = os.path.dirname(
        os.path.abspath(__file__)
    )

    plugin_meta_required = [
        'name', 'version', 'scm', 'script', 'handler'
    ]

    plugin_meta_optional = [
        'author', 'email'
    ]

    def __init__(self, plugin):
        self.plugin_name = plugin
        self.plugin_path = self.get_plugin_path()
        self.meta_path = self.get_meta_path()
        self.meta_content = self.get_meta_content()

    def get_plugin_path(self):
        return os.path.join(self.plugins_path, self.plugin_name)

    def get_meta_path(self):
        return os.path.join(self.plugin_path, self.default_meta_file)

    def get_meta_content(self):
        with open(self.meta_path, 'r') as meta_file:
            try:
                return yaml.load(meta_file)
            except yaml.YAMLError as exc:
                raise

    def get_script_file(self, script_file):
        return os.path.join(self.plugin_path, script_file)


#TODO: More validation
class PluginValidator(PluginMeta):
    def __init__(self, plugin_name):
        super(PluginValidator, self).__init__(plugin_name)
        self.plugin = Plugin()
        self.invalid = []

    def check_meta_file(self):
        plugin_package = os.listdir(self.plugin_path)
        if not self.default_meta_file in plugin_package:
            self.invalid.append('Missing meta file {}'.format(self.default_meta_file))
            return False
        return True

    def validate_required_fields(self):
        common_fields = set(self.plugin_meta_required) & set(self.meta_content.keys())
        missing_fields = set(self.plugin_meta_required) - set(self.meta_content.keys())
        if len(common_fields) < len(self.plugin_meta_required):
            self.invalid.append('Missing required fields: {}'.format(missing_fields))
            return False
        return True

    def validate_unsupported_fields(self):
        unsupported_fields = set(self.meta_content.keys()) - set(self.plugin_meta_required + self.plugin_meta_optional)
        if len(unsupported_fields):
            self.invalid.append('Unsupported field: {}'.format(unsupported_fields))
            return False
        return True

    def validate_script_file(self):
        script_name = self.meta_content.get('script')
        if not script_name:
            self.invalid.append('Missing value of required parameter script')
            return False
        script_file = self.get_script_file(script_name)
        if not os.path.exists(script_file):
            self.invalid.append('Missing script file: {}'.format(script_file))
            return False
        return True

    def validate_handler(self):
        handler_name = self.meta_content.get('handler')
        if not handler_name:
            self.invalid.append('Missing value of required parameter handler')
            return False
        return True

    def is_valid(self):
        validators = [
            self.validate_required_fields,
            self.validate_unsupported_fields,
            self.check_meta_file,
            self.validate_script_file,
            self.validate_handler
        ]
        for validator in validators:
            if not validator():
                return False
        self.plugin.meta = self.meta_content
        return True


class PluginsLoader(PluginMeta):
    def __init__(self, logger=None):
        self.logger = logger
        self.plugins = {}

    def handle(self, plugin_name, context):
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            return {'error': 'Plugin {} not found'.format(plugin_name)}
        try:
            return {'response': plugin.handler(context)}
        except Exception as exc:
            return {'exception': exc}

    def discover(self):
        if not os.path.exists(self.plugins_path):
            self.logger.error('Unable to resolve plugins path: {}'.format(plugins_path))
            return
        self.load()

    def __prepare(self, plugins):
        for plugin in plugins:
            self.logger.info('Checking plugin: {}'.format(plugin))
            maybe_plugin = PluginValidator(plugin)

            if maybe_plugin.is_valid():
                yield maybe_plugin.plugin
            else:
                self.logger.warning('Plugin {} is invalid'.format(plugin))
                for cause in maybe_plugin.invalid:
                    self.logger.warning(cause)

    def load(self):
        plugins = [
            plugin for plugin in os.listdir(self.plugins_path) if
            os.path.isdir(os.path.join(self.plugins_path, plugin))
        ]
        try:
            for plugin in self.__prepare(plugins):
                plugin.module = importlib.import_module('.'.join([__name__, plugin.name, plugin.script]))
                self.plugins[plugin.name] = plugin
        except ImportError as exc:
            self.logger.error('Unable to load plugins: {}'.format(exc))