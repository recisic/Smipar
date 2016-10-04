from __future__ import print_function, unicode_literals
from pypeg2 import *
import re, json


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

class Bond(str):
	grammar = re.compile(r'[-=#$:/\\.]')

class OpenBranch(str):
	grammar = re.compile(r'[()]')

class CloseBranch(str):
	grammar = re.compile(r'[)]')

class Branch(List):
	pass

class SMILES(List):
	pass


# passed grammars (recursive)

Branch.grammar = grammar = OpenBranch, optional(Bond), some(SMILES), CloseBranch
SMILES.grammar = Atom, maybe_some([some(optional(Bond), [Atom, RingClosure]), Branch])


# print function

def print_parsed(parsed_smiles):
	for k in parsed_smiles:
		if isinstance(k, (OrganicSymbol, AromaticSymbol, WILDCARD, \
			OpenBranch, CloseBranch, RingClosure, Bond)):
			print(k.__class__.__name__, ':', k)
		elif isinstance(k, AtomSpec):
			print(k.__class__.__name__, end = ' : [')
			for s in k:
				print(s.__class__.__name__, ':', s, end = ", ")
			print(']')
		elif isinstance(k, List):
			print_parsed(k)


# parser function

def parser(input_smiles):
	return parse(input_smiles, SMILES)


# json writer

def parse_class_json(k):
		if isinstance(k, (OrganicSymbol, WILDCARD)):
			return {
				"type": "atom",
				"symbol": k,
				"isotope": "null",
				"aromatic": "false",
				"chiralClass": "null",
				"hydrogens": "null",
				"charge": "null",
				"klass": 0
			}

		elif isinstance(k, AromaticSymbol):
			return {
				"type": "atom",
				"symbol": k,
				"isotope": "null",
				"aromatic": "true",
				"chiralClass": "null",
				"hydrogens": "null",
				"charge": "null",
				"klass": 0
			}

		elif isinstance(k, RingClosure):
			return {
				"type": "ring-closure",
				"index": k
			}

		elif isinstance(k, OpenBranch):
			return {"type": "open-branch"}

		elif isinstance(k, CloseBranch):
			return {"type": "close-branch"}

		elif isinstance(k, AtomSpec):
			symbol = isotope = chiralClass = charge = "null"
			hydrogens = klass = 0
			aromatic = "false"
			for s in k:
				if isinstance(s, (OrganicSymbol, AromaticSymbol, WILDCARD)):
					symbol = s
				elif isinstance(s, AromaticSymbol):
					aromatic = "true"
				elif isinstance(s, Isotope):
					isotope = int(s)
				elif isinstance(s, ChiralClass):
					chiralClass = s
				elif isinstance(s, HCount):
					hydrogens = int(s)
				elif isinstance(s, Charge):
					charge = s
				elif isinstance(s, Klass):
					klass = int(s)

			return {
				"type": "atom",
				"symbol": symbol,
				"isotope": isotope,
				"aromatic": aromatic,
				"chiralClass": chiralClass,
				"hydrogens": hydrogens,
				"charge": charge,
				"klass": klass
			}


def parser_json(input_object, isParsed = False, isFinal = True):
	parsed_json = []

	if not isParsed:
		input_object = parser(input_object)
	
	for k in input_object:
		if isinstance(k, (OrganicSymbol, AromaticSymbol, WILDCARD, \
			OpenBranch, CloseBranch, RingClosure, AtomSpec)):
			parsed_json = parsed_json + [parse_class_json(k)]

		elif isinstance(k, List):
			parsed_json = parsed_json + parser_json(k, True, False)

	# TODO: needs refactoring
	if not isFinal:
		return parsed_json
	else:
		return json.dumps(parsed_json, sort_keys=True, indent=4, separators=(',', ': '))
