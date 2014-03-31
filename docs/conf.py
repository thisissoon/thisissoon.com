# -*- coding: utf-8 -*-

"""
.. module:: docs
   :synopsis: Sphinx documentation configuration
"""

import sys
import os

from better import better_theme_path

# Add SOON_ to the Path
root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
    )
)

sys.path.append(os.path.join(root, 'soon'))

import soon  # noqa


# Project details
project = u'SOON_'
copyright = u'2014, SOON_'
version = '0.0.1'
release = '0.0.1'

# Sphinx Config
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

exclude_patterns = []

# Theme
html_theme_path = [better_theme_path]
html_theme = 'better'
html_static_path = ['_static']
pygments_style = 'sphinx'
htmlhelp_basename = 'SOON_'

man_pages = [(
    'index', 'pravis', u'SOON_ Documentation',
    [u'SOON_'], 1
)]

texinfo_documents = [(
    'index', 'SOON_', u'Pravis Documentation',
    u'SOON_', 'SOON_', 'One line description of project.',
    'Miscellaneous'),
]
