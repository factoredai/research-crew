import os

from dynaconf import Dynaconf


base_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.abspath(os.path.join(base_dir, '../../config'))

settings = Dynaconf(
    settings_files=[
        os.path.join(config_dir, 'settings.toml'),
        os.path.join(config_dir, '.secrets.toml')
    ],
)
