from __future__ import print_function, unicode_literals
import Smipar, json

test_string = 'CSC1=NC(=C(C(=N1)O)[N+](=O)[O-])O'
# parsed_smiles = Smipar.parser(test_string)
# Smipar.print_parsed(parsed_smiles)
print((Smipar.parser_json(test_string)))