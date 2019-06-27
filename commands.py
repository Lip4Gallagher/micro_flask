#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from abc import ABC

import gevent.monkey
from flask_script import Command
from gevent import pywsgi
from werkzeug.contrib import profiler


class ProfileServer(Command, ABC):
    """
        Run the server with profiling tools
    """

    def __init__(self, host='localhost', port=9000, **options):
        super().__init__()
        self.port = port
        self.host = host
        self.server_options = options

    def __call__(self, app, **kwargs):
        f = open('profiler.log', 'w')
        stream = profiler.MergeStream(sys.stdout, f)

        app.config['PROFILE'] = True
        app.wsgi_app = profiler.ProfilerMiddleware(app.wsgi_app, stream, restrictions=[30])
        app.run(debug=True)


class GEventServer(Command, ABC):
    """
        Run the server with gevent
    """

    def __init__(self, host='127.0.0.1', port=5000, **options):
        super().__init__()
        self.port = port
        self.host = host
        self.server_options = options

    def __call__(self, app, **kwargs):
        gevent.monkey.patch_all()

        ws = pywsgi.WSGIServer(listener=(self.host, self.port), application=app)
        print("* Running on http://{}:{}/ (Press CTRL+C to quit)".format(self.host, self.port))
        ws.serve_forever()
