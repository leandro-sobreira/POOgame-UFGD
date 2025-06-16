import os
import sys

sys.path.insert(0, os.path.abspath('../project'))
#sys.path.append(os.path.abspath('../project/src/classes'))
#sys.path.append(os.path.abspath('../project/src/'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'POO Game Cassino UFGD (Grupo LEMA)'
copyright = '2025, Leandro Peres Sobreira, Abner Lucas Pereira Cardoso Vera, Eduardo Rodrigues Rizzi, Marcos Henrique Almeida Lima'
author = 'Leandro Peres Sobreira, Abner Lucas Pereira Cardoso Vera, Eduardo Rodrigues Rizzi, Marcos Henrique Almeida Lima'
release = '16/06/2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

napoleon_custom_sections = ['Bad title']

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []

language = 'pt-br'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
