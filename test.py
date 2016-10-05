from __future__ import print_function, unicode_literals
import Smipar, json

test_string = '[c:7]1([CH3:6])[c:12]([C:3]([c:2]2[cH:11][cH:12][cH:7][cH:8][c:9]2[CH3:10])=[O:5])[cH:11][cH:10][cH:9][cH:8]1'
# parsed_smiles = Smipar.parser(test_string)
# Smipar.print_parsed(parsed_smiles)
print((Smipar.parser_json(test_string)))