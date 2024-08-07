from typing import Optional

import DocumentControl

CHEM_UNITS = [
	("0", "0: None"),
	("1", "1: The Atom"),
	("2", "2: Formulas and Equations"),
	("3", "3: The Mathematics of Formulas and Equations"),
	("4", "4: Physical Behavior of Matter"),
	("5", "5: The Periodic Table"),
	("6", "6: Bonding"),
	("7", "7: Properties of Solutions"),
	("8", "8: Kinetics and Equilibrium"),
	("9", "9: Oxidation-Reduction"),
	("10", "10: Acids, Bases, and Salts"),
	("11", "11: Organic Chemistry"),
	("12", "12: Nuclear Chemistry"),
]
USHG_UNITS = [
	("0", "0: None"),
	("1", "1: 1491–1607"),  # Native Americans and early explorers (Columbus to Jamestown start)
	("2", "2: 1607–1754"),  # New world colonies of European countries (Jamestown to French and Indian War)
	("3", "3: 1754–1800"),  # American Revolution and early republic (french and india war to Jefferson's 1st term)
	("4", "4: 1800–1848"),  # Early American developments, 2nd great awakening (Jefferson to civil war)
	("5", "5: 1844–1877"),  # Civil war, prelude, war, reconstruction
	("6", "6: 1865–1898"),  # Gilded age (civil war to spanish american war)
	("7", "7: 1890–1945"),  # Grown as a super power (post Spanish-American war to end of WW2)
	("8", "8: 1945–1980"),  # Post war era, cold war, civil rights (end of WW2 to Regan)
	("9", "9: 1980–Present"),  # Modern america
]
ALG1_UNITS = [
	("0", "0: None"),  # ex) add 3*x*rad(7) + 2*x*rad(7), rationalize a number
	# 1) Use properties of rational and irrational numbers.
	("1", "1: The Real Number System"),
	# 2) Reason quantitatively and use units to solve problems
	("2", "2: Quantities"),
	# 3) Write expressions in equivalent forms to reveal their characteristics.
	("3", "3: Structure in Expressions"),
	# 4) Arithmetic operations and zeros/factors of Polynomials
	("4", "4: Arithmetic with Polynomials and Rational Expressions"),
	# 5) Create equations that describe numbers or relationships
	("5", "5: Creating Equations"),
	# 6) Represent and solve equations/inequalities in one variable, system of equations, equations on a graph
	("6", "6: Reasoning with Questions and Inequalities"),  # ex) Create an equation passing through 2 points, solve for x in a polynomial
	# 7) Function notation, functions in context/applications, analyze F() with different representations
	("7", "7: Interpreting Functions"),
	# 8) Build a function that models a relationship between two quantities, build new functions from existing functions.
	("8", "8: Building Functions"),
	# 9) Construct, compare, and interpret to solve problems
	("9", "9: Linear, Quadratic, and Exponential Models"),
	# 10) Single count or measured variables, two categorical and quantitative variables, linear models
	("10", "10: Interpreting Categorical and Quantitative Data")
]

# TODO it would be awesome to do some k means clustering with all previous exam questions to determine a
# new question distance to the known groups, and return the most likely group and a measure of confidence.
# For now we'll use the key vocabulary words and the highest count gets it
CHEM_UNIT_KEYWORDS = {
	CHEM_UNITS[0][0]: [],
	CHEM_UNITS[1][0]: [" atom ", " atomic mass ", " atomic mass unit ", " atomic number ", " compound ", " electron ",
						" element ", " excited state ", " neutron ", " ground state ", " nucleus ", " heterogeneous ",
						" orbital ", " homogeneous ", " proton ", " isotope ", " pure substance ", " mass number ",
						" valence ", " wave-mechanical model ", " spectra ", " substance ", " isotopes "],  # MIXTURES AND COMPOUNDS
	CHEM_UNITS[2][0]: [" analysis ", " chemical change ", " coefficient ", " decomposition ", " diatomic molecule ",
						" double replacement ", " empirical formula ", " endothermic ", " exothermic ", " qualitative ",
						" formula ", " quantitative ", " molecular formula ", " reactant ", " molecule ", " single replacement ",
						" physical change ", " subscript ", " polyatomic ion ", " symbol ", " product ", " synthesis "],
	CHEM_UNITS[3][0]: [" formula mass ", " mole ", " gram formula mass ", " percentage composition ", " moles "],
	CHEM_UNITS[4][0]: [" condensation ", " deposition ", " freezing ", " fusion ", " gaseous phase ", " heat ",
						" solid phase ", " heat of fusion ", " sublimation ", " heat of vaporization ", " temperature ",
						" kinetic molecular theory ", " vaporization ", " liquid phase "],
	CHEM_UNITS[5][0]: [" atomic radius ", " electronegativity ", " family ", " group ", " periodic table ",
						" ionic radius ", " noble gas ", " ionization energy ", " nonmetal ", " metal ",
						" periodic law ", " metalloid ", " period ", " ionic radius "],
	CHEM_UNITS[6][0]: [" asymmetrical molecule ", " covalent bond ", " dipole-dipole forces ", " double covalent bond ",
						" hydrogen bond ", " ion ", " ionic bond ", " nonpolar covalent bond ", " lewis dot diagram ",
						" octet ", " london dispersion forces ", " octet rule ", " malleability ",
						" polar covalent bond ", " metallic bond ", " symmetrical molecule ",
						" multiple covalent bond ", " triple covalent bond ", " charge distribution "],
	CHEM_UNITS[7][0]: [" boiling point ", " ion-dipole forces ", " molarity ", " parts per million ", " ppm ",
						" percent by volume ", " percent mass ", " supersaturated ", " saturated ", " unsaturated ",
						" solute ", " vapor ", " solution ", " vapor pressure ", " solvent ", " dissolve ",
						" mixture ", " solubility "],
	CHEM_UNITS[8][0]: [" activated complex ", " activation energy ", " catalyst ", " kinetics ", " entropy ",
						" potential ", " energy ", " equilibrium ", " stress ", " chatelier "],
	CHEM_UNITS[9][0]: [" anode ", " electrolytic cell ", " redox ", " cathode ", " half-reaction ",
						" reduction ", " electrochemical cell ", " oxidation ", " salt bridge ", " electrode ",
						" oxidation number ", " voltaic cell ", " electrolysis "],
	CHEM_UNITS[10][0]: [" acid ", " base ", " acidity ", " alkalinity ", " arrhenius acid ", " arrhenius base ",
						" electrolyte ", " neutralization ", " hydrogen ion ", " ph scale ", " hydronium ion ",
						" salt ", " indicator ", " titration "],
	CHEM_UNITS[11][0]: [" addition reaction ", " alcohol ", " aldehyde ", " alkane ", " alkene ", " alkyne ",
						" amide ", " amine ", " amino acid ", " organic ", " esterification ", " organic acid ",
						" ester ", " organic halide ", " ether ", " polymer ", " fermentation ", " polymerization ",
						" functional group ", " saponification ", " hydrocarbon ", " saturated ", " isomer ",
						" substitution reaction ", " ketone ", " unsaturated "],
	CHEM_UNITS[12][0]: [" alpha particle ", " fusion ", " radioisotope ", " artificial transmutation ",
						" gamma ray ", " tracer ", " beta particle ", " half-life ", " half life ", " transmutation ",
						" fission ", " natural transmutation "]
}

ALG1_UNIT_KEYWORDS = {
	ALG1_UNITS[0][0]: [],
	ALG1_UNITS[1][0]: ["N-RN"],
	ALG1_UNITS[2][0]: ["N-Q"],
	ALG1_UNITS[3][0]: ["A-SSE"],
	ALG1_UNITS[4][0]: ["A-APR"],
	ALG1_UNITS[5][0]: ["A-CED"],
	ALG1_UNITS[6][0]: ["A-REI"],
	ALG1_UNITS[7][0]: ["F-IF"],
	ALG1_UNITS[8][0]: ["F-BF"],
	ALG1_UNITS[9][0]: ["F-LE"],
	ALG1_UNITS[10][0]: ["S-ID"],
}


def get_units(subject: str) -> list:
	if subject is None:
		return [("0", "Select an Exam to get units")]
	elif subject not in DocumentControl.SUPPORTED_SUBJECTS:
		return [("0", "Unrecognized unit")]
	elif subject == "CHEM":
		return CHEM_UNITS
	elif subject == "USHG":
		return USHG_UNITS
	elif subject == "ALG1":
		return ALG1_UNITS
	return [("0", "Unit not supported yet")]


def guess_unit(quest_num: int, subject: str, question_and_answers: str) -> str:
	# Returns the best unit text (second value in the unit tuples) corresponding to the best guessed unit
	# based on the keywords in the UNIT_KEYWORDS dicts
	if subject == "CHEM":
		best_score = 0
		best_unit = 0
		# print(quest_num)
		for unit in range(len(CHEM_UNITS)):
			# print("\tUnit" + str(unit))
			unit_score = 0
			for keyword in CHEM_UNIT_KEYWORDS[str(unit)]:
				count = question_and_answers.count(keyword)
				unit_score += count
				# if count > 0:
					# print("\t\t" + keyword + ": " + str(count))
			if unit_score > best_score:
				best_score = unit_score
				best_unit = unit
		# print("\tBest unit was " + str(best_unit) + " with a score of " + str(best_score))
		return CHEM_UNITS[best_unit][1]
	elif subject == "ALG1":
		for unit in range(1, len(ALG1_UNITS) + 1):
			if question_and_answers.strip().startswith(ALG1_UNIT_KEYWORDS[str(unit)][0]):
				return ALG1_UNITS[unit][1]
		return ALG1_UNITS[0][1]
	else:
		# TODO this really needs to be a constant
		return "0: None"
