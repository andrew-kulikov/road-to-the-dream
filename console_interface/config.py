"""
This module contains a class for loading, editing and saving application settings

Public class:

'Config': Is intended for reading and applying program settings
"""

import os
from pathlib import Path
import configparser


class Config:
    """
    Is intended for reading and applying program settings with file configuration.txt

    Public Constant:

    'LIBRARY_PATH': contains the path to the installed program folder

    Private Attributes:

    '__config_path': contains the path to the configuration program
    '__LOG_PATH': contains the path to the history login users in program
    '__DATABASE_FOLDER_PATH': contains the path folder with information about tasks and messages

    Public Methods:

    'load_dirs': read information on configuration.txt file
    'check_file_path': check file on exist
    'get_config_path': return path on configuration file
    'set_config_path': set new path for configuration file
    'get_task_file': return path on file with tasks
    'get_messages_file': return path on file with user messages
    'get_logger_output_path': return path on file with logger output
    'get_status_logger': return status logger
    'get_status_logger': return status logger
    'set_status_logger': set new status logger

    Default work file: configuration.txt

    Lines in file:
    0: path to logger records
    1: path to tasks file
    2: path to task lists file
    3: logger status in format ON/OFF (logger = ON/OFF)

    P.S. If records in configurations file was just name file, then work path was 'default directory' + 'name file'.
    ('default directory' for logger records=/logger_output, for task and messages=/database), else if records was
    directory, then work path was 'directory with file'.
    """

    LIBRARY_PATH = os.path.dirname(__file__)
    __config_path = os.path.join(LIBRARY_PATH, 'config.ini')
    __LOG_PATH = os.path.join(LIBRARY_PATH, 'logs')
    __DATABASE_FOLDER_PATH = os.path.join(LIBRARY_PATH, 'data')

    @classmethod
    def load_config(cls):
        """ Load information of program and all settings with configuration.txt
        If file not found, create it.
        If some path is not specified, applies it for it default values
        Return list with paths to files

        :return
        'settings': list with different path tos files
        """
        settings = {'log_path': os.path.join(cls.__LOG_PATH, 'log.log'),
                    'log_on': True,
                    'tasks_file': os.path.join(cls.__DATABASE_FOLDER_PATH, 'tasks.json'),
                    'task_lists_file': os.path.join(cls.__DATABASE_FOLDER_PATH, 'task_lists.json'),
                    }
        # settings = [None] * 4  # config include 4 settings: path for tasks, messages, output logger and status logger

        if Path(cls.__config_path).is_file():
            config = configparser.RawConfigParser()
            config.read(cls.__config_path)
            default = config['DEFAULT']
            if 'log_path' in default:
                settings['log_path'] = default['log_path']
            if 'log_on' in default:
                settings['log_on'] = default['log_on']
            if 'tasks_file' in default:
                settings['tasks_file'] = default['tasks_file']
            if 'task_lists_file' in default:
                settings['task_lists_file'] = default['task_lists_file']

        return settings

    @classmethod
    def check_file_path(cls, path):
        """ Check file on exist, if file not found create it

        :param
        'path': path checked file

        :return: path file
        """
        if not os.path.exists(cls.__DATABASE_FOLDER_PATH):
            os.makedirs(cls.__DATABASE_FOLDER_PATH)

        if not os.path.exists(cls.__LOG_PATH):
            os.makedirs(cls.__LOG_PATH)

        if not Path(path).is_file():
            with open(path, 'w'):
                pass

        return path

    @classmethod
    def get_logger_output_path(cls):
        """Return path to log file"""
        settings = cls.load_config()
        if settings['log_path'].find('/') == -1:
            return cls.check_file_path(cls.__LOG_PATH + str(settings['log_path']))
        else:
            return cls.check_file_path(settings['log_path'])

    @classmethod
    def get_tasks_file(cls):
        """ Return path file with tasks"""
        settings = cls.load_config()
        if settings['tasks_file'].find('/') == -1:
            return cls.check_file_path(cls.__DATABASE_FOLDER_PATH + str(settings['tasks_file']))
        else:
            return cls.check_file_path(settings['tasks_file'])

    @classmethod
    def get_task_lists_file(cls):
        """ Return path file with tasks"""
        settings = cls.load_config()
        if settings['task_lists_file'].find('/') == -1:
            return cls.check_file_path(cls.__DATABASE_FOLDER_PATH + str(settings['task_lists_file']))
        else:
            return cls.check_file_path(settings['task_lists_file'])

    @classmethod
    def get_config_path(cls):
        """ Return path configuration file"""
        cls.load_config()
        return cls.__config_path

    @classmethod
    def set_new_config_path(cls, new_path):
        """Set new path for configuration file. Default value is config.ini"""
        cls.__config_path = new_path

    @classmethod
    def get_logger_status(cls):
        """Return status logger (ON/OFF). Default status = ON

        :raises
        'Exception': if status not equal ON/OFF
        """
        settings = cls.load_config()
        return bool(settings['log_on'])

    @classmethod
    def set_logger_status(cls, log_on=True):
        """Enable/disable logging.

        :param log_on: new logging status.
        :return:
        :raises
        'TypeError': if status is not boolean.
        """
        new_settings = cls.load_config()
        if not isinstance(log_on, bool):
            raise TypeError('Status must be boolean')
        new_settings['log_on'] = log_on
        cls.save_changes(new_settings)

    @classmethod
    def save_changes(cls, new_config):
        """Save new settings into config file.

        :param new_config: new dict of settings, will be saved in DEFAULT section.
        :return:
        """
        config = configparser.RawConfigParser()
        config['DEFAULT'] = new_config
        with open(cls.__config_path, 'w') as config_file:
            config.write(config_file)
