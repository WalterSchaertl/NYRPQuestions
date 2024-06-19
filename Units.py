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


def get_units(subject: str) -> list:
	if subject is None:
		return [("0", "Select an Exam to get units")]
	if subject not in DocumentControl.SUPPORTED_SUBJECTS:
		return [("0", "Unrecognized unit")]
	if subject == "Chem":
		return CHEM_UNITS
	return [("0", "Unit not supported yet")]