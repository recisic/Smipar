from __future__ import print_function, unicode_literals
import Smipar, json

test_string = 'CBrN1C%77C(C%77[13c@TB9H2--:45]1*=c2)cccnc2'
# parsed_smiles = Smipar.parser(test_string)
# Smipar.print_parsed(parsed_smiles)
print((Smipar.parser_json(test_string)))