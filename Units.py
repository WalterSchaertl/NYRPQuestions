from typing import Optional

from DocumentControl import *

UNIT_ZERO = ("0", "0: None")
UNITS = {
    ExamCode.CHEM: [
        UNIT_ZERO,
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
    ],
    ExamCode.USHG: [
        UNIT_ZERO,
        ("1", "1: 1491–1607"),  # Native Americans and early explorers (Columbus to Jamestown start)
        ("2", "2: 1607–1754"),  # New world colonies of European countries (Jamestown to French and Indian War)
        ("3", "3: 1754–1800"),  # American Revolution and early republic (french and india war to Jefferson's 1st term)
        ("4", "4: 1800–1848"),  # Early American developments, 2nd great awakening (Jefferson to civil war)
        ("5", "5: 1844–1877"),  # Civil war, prelude, war, reconstruction
        ("6", "6: 1865–1898"),  # Gilded age (civil war to spanish american war)
        ("7", "7: 1890–1945"),  # Grown as a super power (post Spanish-American war to end of WW2)
        ("8", "8: 1945–1980"),  # Post war era, cold war, civil rights (end of WW2 to Regan)
        ("9", "9: 1980–Present"),  # Modern america
    ],
    ExamCode.ALG1: [
        UNIT_ZERO,
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
        ("6", "6: Reasoning with Questions and Inequalities"),
        # ex) Create an equation passing through 2 points, solve for x in a polynomial
        # 7) Function notation, functions in context/applications, analyze F() with different representations
        ("7", "7: Interpreting Functions"),
        # 8) Build a function that models a relationship between two quantities, build new functions from existing functions.
        ("8", "8: Building Functions"),
        # 9) Construct, compare, and interpret to solve problems
        ("9", "9: Linear, Quadratic, and Exponential Models"),
        # 10) Single count or measured variables, two categorical and quantitative variables, linear models
        ("10", "10: Interpreting Categorical and Quantitative Data")
    ],
    ExamCode.GHG2: [
        UNIT_ZERO,
        ("1", "1: The World in 1750"),  # 10.1
        ("2", "2: Enlightenment, Revolution, and Nationalism (1750-1914)"),  # 10.2 (1750-1914)
        ("3", "3: Causes and Effects of the Industrial Revolution (1750-1914)"),  # 10.3 (1750-1914)
        ("4", "4: Imperialism (1750-1914)"),  # 10.4 (1750-1914)
        ("5", "5: Unresolved Global Conflict (1914-1945)"),  # 10.5 (1914-1945)
        ("6", "6: Unresolved Global Conflict (1945-1991)"),  # 10.5 (1945-1991)
        ("7", "7: Decolonization and Nationalism (1900-2000)"),  # 10.7 (1900-2000)
        ("8", "8: Tensions Between Traditional Cultures and Modernization (1945-present)"),  # 10.8 (1945-present)
        ("9", "9: Globalization and a Changing Global Environment (1990-present)"),  # 10.9 (1990-present)
        ("10", "10: Human Rights Violations (1933-present)")  # 10.10 (1948-present)
    ],
    ExamCode.ALG2: [
        UNIT_ZERO,
        ("1", "1: The Real Number System"),
        ("2", "2: Quantities"),
        ("3", "3: The Complex Number System"),
        ("4", "4: Seeing Structure in Expressions"),
        ("5", "5: Arithmetic with Polynomials and Rational Expressions"),
        ("6", "6: Creating Equations"),
        ("7", "7: Reasoning with Equations and Inequalities"),
        ("8", "8: Expressing Geometric Properties with Equations"),
        ("9", "9: Interpreting Functions"),
        ("10", "10: Building Functions"),
        ("11", "11: Linear, Quadratic, and Exponential Models "),
        ("12", "12: Trigonometric Functions "),
        ("13", "13: Interpreting categorical and quantitative data "),
        ("14", "14: Making Inferences and Justifying Conclusions"),
        ("15", "15: Conditional Probability and the Rules of Probability ")
    ],
    ExamCode.ESCI: [
        UNIT_ZERO,
        ("1", "1: Introduction to Earth's Changing Environment"),
        ("2", "2: Measuring Earth"),
        ("3", "3: Earth in the Universe"),
        ("4", "4: Motion of Earth, Moon, and Sun"),
        ("5", "5: Energy in Earth Processes"),
        ("6", "6: Insolation and the Seasons"),
        ("7", "7: Weather"),
        ("8", "8: Water and Climate"),
        ("9", "9: Weathering and Erosion"),
        ("10", "10: Deposition"),
        ("11", "11: Earth Materials-Minerals, Rocks, and Mineral Resources"),
        ("12", "12: Earth's Dynamic Crust and Interior"),
        ("13", "13: Interpreting Geologic History"),
        ("14", "14: Landscape Development and Environmental Change"),
    ]
}

# Some of these are based off key words, some can look up the unit from the guide directly
# TODO fix the 0 unit, add key works or units to USHG
UNIT_KEYWORDS = {
    ExamCode.CHEM: {
        "0": [],
        "1": [" atom ", " atomic mass ", " atomic mass unit ", " atomic number ", " compound ", " electron ",
              " element ", " excited state ", " neutron ", " ground state ", " nucleus ", " heterogeneous ",
              " orbital ", " homogeneous ", " proton ", " isotope ", " pure substance ", " mass number ",
              " valence ", " wave-mechanical model ", " spectra ", " substance ", " isotopes "],
        # MIXTURES AND COMPOUNDS
        "2": [" analysis ", " chemical change ", " coefficient ", " decomposition ", " diatomic molecule ",
              " double replacement ", " empirical formula ", " endothermic ", " exothermic ", " qualitative ",
              " formula ", " quantitative ", " molecular formula ", " reactant ", " molecule ", " single replacement ",
              " physical change ", " subscript ", " polyatomic ion ", " symbol ", " product ", " synthesis "],
        "3": [" formula mass ", " mole ", " gram formula mass ", " percentage composition ", " moles "],
        "4": [" condensation ", " deposition ", " freezing ", " fusion ", " gaseous phase ", " heat ",
              " solid phase ", " heat of fusion ", " sublimation ", " heat of vaporization ", " temperature ",
              " kinetic molecular theory ", " vaporization ", " liquid phase "],
        "5": [" atomic radius ", " electronegativity ", " family ", " group ", " periodic table ",
              " ionic radius ", " noble gas ", " ionization energy ", " nonmetal ", " metal ",
              " periodic law ", " metalloid ", " period ", " ionic radius "],
        "6": [" asymmetrical molecule ", " covalent bond ", " dipole-dipole forces ", " double covalent bond ",
              " hydrogen bond ", " ion ", " ionic bond ", " nonpolar covalent bond ", " lewis dot diagram ",
              " octet ", " london dispersion forces ", " octet rule ", " malleability ",
              " polar covalent bond ", " metallic bond ", " symmetrical molecule ",
              " multiple covalent bond ", " triple covalent bond ", " charge distribution "],
        "7": [" boiling point ", " ion-dipole forces ", " molarity ", " parts per million ", " ppm ",
              " percent by volume ", " percent mass ", " supersaturated ", " saturated ", " unsaturated ",
              " solute ", " vapor ", " solution ", " vapor pressure ", " solvent ", " dissolve ",
              " mixture ", " solubility "],
        "8": [" activated complex ", " activation energy ", " catalyst ", " kinetics ", " entropy ",
              " potential ", " energy ", " equilibrium ", " stress ", " chatelier "],
        "9": [" anode ", " electrolytic cell ", " redox ", " cathode ", " half-reaction ",
              " reduction ", " electrochemical cell ", " oxidation ", " salt bridge ", " electrode ",
              " oxidation number ", " voltaic cell ", " electrolysis "],
        "10": [" acid ", " base ", " acidity ", " alkalinity ", " arrhenius acid ", " arrhenius base ",
               " electrolyte ", " neutralization ", " hydrogen ion ", " ph scale ", " hydronium ion ",
               " salt ", " indicator ", " titration "],
        "11": [" addition reaction ", " alcohol ", " aldehyde ", " alkane ", " alkene ", " alkyne ",
               " amide ", " amine ", " amino acid ", " organic ", " esterification ", " organic acid ",
               " ester ", " organic halide ", " ether ", " polymer ", " fermentation ", " polymerization ",
               " functional group ", " saponification ", " hydrocarbon ", " saturated ", " isomer ",
               " substitution reaction ", " ketone ", " unsaturated "],
        "12": [" alpha particle ", " fusion ", " radioisotope ", " artificial transmutation ",
               " gamma ray ", " tracer ", " beta particle ", " half-life ", " half life ", " transmutation ",
               " fission ", " natural transmutation "]
    },
    ExamCode.USHG: None,
    ExamCode.ALG1: {
        "0": ["not_a_thing"],
        "1": ["N-RN"],
        "2": ["N-Q"],
        "3": ["A-SSE"],
        "4": ["A-APR"],
        "5": ["A-CED"],
        "6": ["A-REI"],
        "7": ["F-IF"],
        "8": ["F-BF"],
        "9": ["F-LE"],
        "10": ["S-ID"],
    },
    ExamCode.GHG2: {
        "0": ["10.0"],
        "1": ["10.1"],
        "2": ["10.2"],
        "3": ["10.3"],
        "4": ["10.4"],
        "5": ["10.5"],
        "6": ["10.6"],
        "7": ["10.7"],
        "8": ["10.8"],
        "9": ["10.9"],
        "10": ["10.10"],
    },
    ExamCode.ALG2: {
        "0": ["not_a_thing"],
        "1": ["N-RN"],
        "2": ["N-Q"],
        "3": ["N-CN"],
        "4": ["A-SSE"],
        "5": ["A-APR"],
        "6": ["A-CED"],
        "7": ["A-REI"],
        "8": ["G-GPE"],
        "9": ["F-IF"],
        "10": ["F-BF"],
        "11": ["F-LE"],
        "12": ["F-TF"],
        "13": ["S-ID"],
        "14": ["S-IC"],
        "15": ["S-CP"]
    },
    ExamCode.ESCI: {
        "0":  [],
        "1":  [" classification ", " cyclic change ", " density ", " dynamic equilibrium ", " inference ",
               " instrument ", " interface ", " mass ", " measurement ", " natural hazard ", " natural resources ",
               " observation ", " percent deviation ", " pollution ", " prediction ", " rate of change ",
               " universe ", " volume "],
        "2":  [" atmosphere ", " contour line ", " coordinate system ", " crust ", " Earth's interior ",
               " elevation ", " equator ", " field ", " gradient ", " hydrosphere ", " inline ", " latitude ",
               " lithosphere ", " longitude ", " meridian of longitude ", " model ", " pauses ",
               " primer meridian ", " profile ", " topographic map "],
        "3":  [" asteroid ", " Big Bang theory ", " celestial object ", " comet ", " Doppler effect ",
               " eccentricity ", " ellipse ", " focus ", " foci ", " galaxy ", " gravitation ", " impact crater ",
               " impact event ", " inertia ", " Jovian planet ", " luminosity ", " meteor ", " Milky Way Galaxy ",
               " moon ", " nuclear fusion ", " red shift ", " revolution ", " rotation ", " solar system ", " star ",
               " terrestrial planet ", " universe "],
        "4":  [" axis ", " constellation ", " Coriolis effect ", " eclipse ", " Foucault pendulum ",
               " geocentric model ", " heliocentric model ", " local time ", " phases ", " tides ", " time zone "],
        "5":  [" condensation ", " conduction ", " convection ", " crystallization ", " electromagnetic energy ",
               " electromagnetic spectrum ", " energy ", " heat emergy ", " joules ", " mechanical energy ",
               " nuclear decay ", " radiation ", " solidification ", " specific heat ", " temperature ",
               " texture ", " vaporization ", " wavelength "],
        "6":  [" angle of incidence ", " deforestation ", " el nino ", " global warming ", " greenhouse gases ",
               " heat budget ", " ice ages ", " insolation ", " ozone ", " sunspot ", " transpiration "],
        "7":  [" air mass ", " air pressure gradient ", " anemometer ", " atmospheric pressure ",
               " barometric pressure ", " air pressure ", " atmospheric transparency ", " barometer ",
               " cloud cover ", " cold front ", " cyclone ", " cyclonic storm ", " dew point ", " front ",
               " humidity ", " isobar ", " jet stream ", " monsoon ", " occluded front ", " planetary wind belt ",
               " polar front ", " precipitation ", " probability ", " psychrometer ", " radar ",
               " relative humidity ", " stationary front ", " station model ", " troposphere ", " visibility ",
               " warm front ", " water vapor ", " weather variables "],
        "8":  [" capillarity ", " climate ", " ground water ", " hydrologic cycle ", " infiltrate ",
               " permeability ", " porosity ", " prevailing winds ", " runoff ", " seep ", " sorted ",
               " stream discharge ", " unsorted ", " urbanization ", " water cycle ", " water retention ",
               " water table "],
        "9":  [" abrasion ", " breaking wave ", " chemical weathering ", " delta ", " erosion ", " finger lake ",
               " flood plain ", " glacial groove ", " glacial parallel scratches ", " glacier ", " mass movement ",
               " meander ", " physical weathering ", " sandbar ", " sandblasting ", " sediment ", " stream ",
               " stream abrasion ", " stream channel shape ", " tributary ", " U-shaped valley ", " V-shaped valley ",
               " watershed ", " weathering "],
        "10": [" barrier island ", " deposition ", " drumlin ", " kettle lake ", " moraine ", " outwash plane ",
               " sand dune ", " sorted sediments ", " unsorted sediments ", ],
        "11": [" sedimentary ", " cleavage ", " metamorphism ", " crystal ", " igneous ", " foliation ", " fossil ",
               " fracture ", " hardness ", " inorganic ", " luster ", " rock ", " magma ", " metamorphic ", " mineral ",
               " organic ", " precipitation ", " rock cycle ", " sedimentary ", " streak ", " texture "],
        "12": [" asthenosphere ", " continental crust ", " convergent plate boundary ", " crust ",
               " divergent plate boundary ", " earthquake ", " epicenter ", " faulted ", " folded ", " hot spot ",
               " inner core ", " island arc ", " lithosphere ", " lithospheric plate ", " mantle ",
               " mid-ocean ridge ", " Moho ", " oceanic crust ", " ocean trench ", " original horizontally ",
               " outer core ", " plate ", " plate tectonic theory ", " P-waves ", " seismic wave ", " subduction ",
               " S-waves ", " tectonic plate ", " transform plat boundary ", " tsunami ", " uplifted ",
               " volcanic eruption ", " volcano ", " young mountains "],
        "13": [" absolute age ", " bedrock ", " carbon-14 dating ", " correlation ", " cross-cutting relationships ",
               " extrusion ", " fossil ", " geologic time scale ", " half-life ", " inclusion ", " index fossil ",
               " intrusion ", " isotope ", " organic evolution ", " outgassing ", " principle of superposition ",
               " radioactive dating ", " radioactive decay ", " species ", " unconformity ", " uranium-238 ",
               " volcanic ash "],
        "14": [" escarpment ", " landscape ", " landscape region ", " mountain ", " plain ",
               " plateau ", " ridges ", " stream drainage ", " uplifting "],
    }
}

UNIT_KEYWORDS_TYPE = {
    ExamCode.CHEM: "CONTAINS",
    ExamCode.USHG: None,
    ExamCode.ALG1: "STARTS_WITH",
    ExamCode.GHG2: "EXACT_MATCH",
    ExamCode.ALG2: "STARTS_WITH",
    ExamCode.ESCI: "CONTAINS"
}


def get_units(subject: ExamCode) -> list:
    return UNITS.get(subject, [UNIT_ZERO])


def guess_unit(subject: ExamCode, question_and_answers: str) -> str:
    # A subject not supported yet
    if UNIT_KEYWORDS_TYPE.get(subject) is None:
        return UNIT_ZERO[1]
    subject_units = UNITS[subject]
    subject_keywords = UNIT_KEYWORDS[subject]
    subject_keyword_type = UNIT_KEYWORDS_TYPE[subject]
    # Returns the best unit text (second value in the unit tuples) corresponding to the best guessed unit
    # based on the keywords in the UNIT_KEYWORDS dicts
    if subject_keyword_type == "CONTAINS":
        best_score = 0
        best_unit = 0
        for unit in range(len(subject_units)):
            unit_score = 0
            for keyword in subject_keywords[str(unit)]:
                count = question_and_answers.count(keyword)
                unit_score += count
            if unit_score > best_score:
                best_score = unit_score
                best_unit = unit
        return subject_units[best_unit][1]
    # The question_and_answers must start with the given unit key text
    elif subject_keyword_type == "STARTS_WITH":
        for unit in range(0, len(subject_units)):
            if question_and_answers.strip().startswith(subject_keywords[str(unit)][0]):
                return subject_units[unit][1]
    # The question_and_answers must exactly match the unit key text
    elif subject_keyword_type == "EXACT_MATCH":
        for unit in range(0, len(subject_units)):
            if question_and_answers.strip() == subject_keywords[str(unit)][0]:
                return subject_keywords[unit][1]
    return UNIT_ZERO[1]
