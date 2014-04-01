# -*- coding: utf-8 -*-

"""
.. module:: soon.run
   :synopsis: Spawn application for uWSGI
"""

from soon.loader import create_app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
