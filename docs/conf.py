# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# added manually for autodoc imports
import sys

sys.path.append("../../src")

project = "quoter"
copyright = "2023, jsm8989"
author = "jsm8989"
release = "0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# see also spike2py package for inspiration in these (via an identical issue on stack overflow)

master_doc = "index"
pygments_style = "sphinx"
source_suffix = ".rst"

extensions = ["sphinx.ext.autodoc", "sphinx_rtd_theme"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
