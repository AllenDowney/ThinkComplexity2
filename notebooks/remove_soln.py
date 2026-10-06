import nbformat as nbf
from glob import glob
from os.path import basename
import re
import sys

notebooks = sys.argv[1:]

text = '# Solution'
replacement = ''

# the Colab link in a solution notebook points to soln/; in the student
# copy, point it to the student notebook instead
colab = r'(colab\.research\.google\.com/github/AllenDowney/ThinkComplexity2/blob/master/)soln/[\w.-]+\.ipynb'

# Search through each notebook
for ipath in notebooks:
    ntbk = nbf.read(ipath, nbf.NO_CONVERT)

    for cell in ntbk.cells:
        # remove tags
        if 'tags' in cell['metadata']:
            cell['metadata']['tags'] = []

        # remove output
        if 'outputs' in cell:
            cell['outputs'] = []

        # remove solutions
        if cell['source'].startswith(text):
            cell['source'] = replacement

        # link to this notebook on Colab
        if cell['cell_type'] == 'markdown':
            cell['source'] = re.sub(colab, r'\1notebooks/' + basename(ipath), cell['source'])

    nbf.write(ntbk, ipath)
