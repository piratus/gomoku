# coding: utf-8
import logging

from tornado.ioloop import IOLoop
from tornado.options import options

from gomoku.app import Application
from gomoku.settings import settings


logger = logging.getLogger(__name__)


app = Application(**settings)

runlevel = 'DEBUG' if options.debug else 'PRODUCTION'
logger.info('Starting %s server on port %d...', runlevel, options.port)

app.listen(options.port, xheaders=not options.debug)

IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
IOLoop.current().start()
