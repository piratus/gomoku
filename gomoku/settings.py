# coding: utf-8
import os
from tornado.options import define, options, parse_command_line, \
    parse_config_file


DEFAULT_SECRET = '__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__'

define('config', type=str, help='path to config file',
       callback=lambda path: parse_config_file(path, final=False))

define('port', default=8888, help='run server on given port', type=int)
define('debug', default=False, help='run server in debug mode', type=bool)
define('secret', default=DEFAULT_SECRET, help='cookie secret key', type=str)

parse_command_line()

package_dir = os.path.dirname(__file__)

settings = {
    'debug': options.debug,
    'cookie_secret': DEFAULT_SECRET,
    'template_path': os.path.join(package_dir, 'templates'),
    'static_path': os.path.join(package_dir, '..', 'dist'),
    'static_url_prefix': '/static/',
    'xsrf_cookies': True
}
