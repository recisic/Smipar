from __future__ import print_function, unicode_literals
# pypeg 2.x is written for python 3 - unicode strings only

from pypeg2 import *
import re

class OrganicSymbol(str):
	grammar = re.compile(r'Br?|Cl?|N|O|P|S|F|I')

class AromaticSymbol(str):
	grammar = re.compile(r'as|b|c|n|o|p|se?')

class WILDCARD(str):
	grammar = re.compile(r'[*]')

class ElementSymbol(str):
	grammar = re.compile(r'[A-Z][a-z]?')

class RingClosure(str):
	grammar = [(ignore('%'), re.compile(r'\d\d')), re.compile(r'\d')]

class ChiralClass(str):
	grammar = re.compile(r'@(@|TH[12]|AL[12]|SP[1-3]|TB([1-9]|1\d|20)|OH([1-9]|[12]\d|30))?')

class Charge(str):
	grammar = re.compile(r'[+-]([+-]|[1-9]\d?)?')
	# warning: '--' and '++' are deprecated

class HCount(str):
	grammar = ignore('H'), re.compile(r'\d?')

class Klass(str):
	grammar = ignore(':'), re.compile(r'\d+')

class Isotope(str):
	grammar = re.compile(r'\d+')

class AtomSpec(List):
	grammar = '[', optional(Isotope), [AromaticSymbol, ElementSymbol, WILDCARD], \
		optional(ChiralClass), optional(HCount), optional(Charge), optional(Klass), ']'

class Atom(List):
	grammar = [OrganicSymbol, AromaticSymbol, AtomSpec, WILDCARD]

class Bond(List):
	grammar = re.compile(r'[-=#$:/\\.]')

class OpenBranch(str):
	grammar = re.compile(r'[(]')

class CloseBranch(str):
	grammar = re.compile(r'[)]')

class Branch(List):
	pass

class SMILES(List):
	pass

# passed grammars (recursive)

Branch.grammar = grammar = OpenBranch, optional(Bond), some(SMILES), CloseBranch
SMILES.grammar = Atom, maybe_some([some(optional(Bond), [Atom, RingClosure]), Branch])

def print_parsed(smiles):
	for k in smiles:
		if isinstance(k, (OrganicSymbol, AromaticSymbol, WILDCARD, \
			OpenBranch, CloseBranch, RingClosure)):
			print(k.__class__.__name__, ':', k)
		elif isinstance(k, AtomSpec):
			print(k.__class__.__name__, end = ' : [')
			for s in k:
				print(s.__class__.__name__, ':', s, end = ", ")
			print(']')
		elif isinstance(k, List):
			print_parsed(k)


# test
test_string = 'CBrN1C%77C(C%77[13C@TB9H2-3:45]1*=c2)cccnc2'
parsed_smiles = parse(test_string, SMILES)
print_parsed(parsed_smiles)