import logging
import logging.config
import os

import yaml

import config

__all__ = ['init_logger', 'logger']


def init_logger(path: str = os.path.join(config.config_dir, config.logging_filename)):
    with open(path, 'r', encoding='utf8') as f:
        yml_config = yaml.safe_load(f.read())
        logging.config.dictConfig(yml_config)


logger = logging.getLogger(config.project_name)
