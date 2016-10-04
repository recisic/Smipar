from __future__ import print_function, unicode_literals
# pypeg 2.x is written for python 3 - unicode strings only

from pypeg2 import *
import re

class OrganicSymbol(List):
	grammar = re.compile(r'Br?|Cl?|N|O|P|S|F|I')

class AromaticSymbol(List):
	grammar = re.compile(r'as|b|c|n|o|p|se?')

class WILDCARD(List):
	grammar = '*'

class ElementSymbol(List):
	grammar = re.compile(r'[A-Z][a-z]?')

class RingClosure(List):
	grammar = [(ignore('%'), re.compile(r'\d\d')), re.compile(r'\d')]

class ChiralClass(List):
	grammar = re.compile(r'@(@|TH[12]|AL[12]|SP[1-3]|TB([1-9]|1\d|20)|OH([1-9]|[12]\d|30))?')

class Charge(List):
	grammar = re.compile(r'[+-]([+-]|[1-9]\d?)?')
	# warning: '--' and '++' are deprecated

class HCount(List):
	grammar = ignore('H'), re.compile(r'\d?')

class Class(List):
	grammar = ignore(':'), re.compile(r'\d+')

class Isotope(List):
	grammar = re.compile(r'\d+')

class AtomSpec(List):
	grammar = '[', optional(Isotope), [AromaticSymbol, ElementSymbol, WILDCARD], \
			optional(ChiralClass), optional(HCount), optional(Charge), optional(Class), ']'

class Atom(List):
	grammar = [OrganicSymbol, AromaticSymbol, AtomSpec, WILDCARD]

class Bond(List):
	grammar = re.compile(r'[-=#$:/\\.]')

class SMILES(List):
	pass

SMILES.grammar = Atom, maybe_some([some(optional(Bond), [Atom, RingClosure]), \
					('(', optional(Bond), some(SMILES), ')')])

test_string = 'CBrN1C%77CC%77[13C@TB9H2-3:45]1*=c2cccnc2'
parsed_smiles = parse(test_string, SMILES)

for atom in parsed_smiles:
	print(atom)