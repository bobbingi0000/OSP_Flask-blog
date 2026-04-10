# -- Sphinx Documentation Configuration (conf.py) --------------------
# Located in the docs/ directory.
# Usage: cd docs && make html

import os
import sys

# ── Add project root to sys.path (so autodoc can find the app package) ──
sys.path.insert(0, os.path.abspath('..'))

# ── Project Information ──────────────────────────────────────────
project = 'Cyber Y2K Blog'
copyright = '2026, Y2K Blog Developer'
author = 'Y2K Blog Developer'
release = '1.0.0'

# ── Extensions ───────────────────────────────────────────────────
extensions = [
    'sphinx.ext.autodoc',          # Auto-extract docstrings
    'sphinx.ext.napoleon',         # Google/NumPy docstring support
    'sphinx.ext.viewcode',         # Add source code links
    'sphinx.ext.intersphinx',      # Cross-reference external docs
    'sphinx_autodoc_typehints',    # Auto-document type hints
]

# ── Napoleon Settings (Google Docstring Style) ───────────────────
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# ── Intersphinx Mapping ─────────────────────────────────────────
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'flask': ('https://flask.palletsprojects.com/en/3.0.x/', None),
}

# ── HTML Output Theme ────────────────────────────────────────────
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
    'style_nav_header_background': '#1a1a2e',   # Y2K dark navy
}
html_static_path = ['_static']
html_logo = None   # Set logo image path if available

# ── autodoc Settings ─────────────────────────────────────────────
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
}

# ── Miscellaneous ────────────────────────────────────────────────
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
language = 'en'
