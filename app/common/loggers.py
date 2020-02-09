import logging
from logging import config


__logger_config = {}


def setup_loggers(conf_class=None):
    '''
    When you want to configure logging for your project, you should do it as soon as possible when the program starts. 
    If app.logger is accessed before logging is configured, it will add a default handler. 
    If possible, configure logging before creating the application object.
    '''
    pass
