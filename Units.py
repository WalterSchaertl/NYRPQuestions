from typing import Optional

import DocumentControl
from Exam import Exam

CHEM_UNITS = [
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


def get_units(exam: Optional[Exam]) -> list:
	if exam is None:
		return [("-1", "Select an Exam to get units")]
	if exam.subj not in DocumentControl.SUPPORTED_SUBJECTS:
		return [("-1", "Unrecognized unit")]
	if exam.subj == "Chem":
		return CHEM_UNITS
	return [("-1", "Unit not supported yet")]