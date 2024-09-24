import json
import operator
import os
import re
import sys
from typing import Optional
from PIL import Image

import DocumentControl
import Units


class Question:
    compare_error = "Questions must have the same exam to compare"
    diagram_hints = ["diagram", "figure", "plot", "chart"]

    def __init__(self, exam: "Exam", number: int, question_text: Optional[str], a: Optional[str],
                 b: Optional[str], c: Optional[str], d: Optional[str], e: Optional[str], ans: int,
                 unit_text: Optional[str]):
        """
        A valid question requires all of the above parameters except e and a diagram path. Others that are marked
        optional can be None on creation, but must eventually be set to pass validation.
        """
        self.exam = exam
        self.number = number
        self.question_text = question_text
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = "" if e is None else e
        self.ans = ans
        self.unit_text = unit_text
        self.unit = None if unit_text is None else int(unit_text[0: unit_text.index(":")])
        self.diagram_path = None
        self.set_diagram(None)

    def __compare__(self, other: "Question", op: operator):
        if isinstance(other, Question):
            if self.exam == other.exam:
                return op(self.number, other.number)
            else:
                raise TypeError(self.compare_error)
        return False

    def __lt__(self, other):
        return self.__compare__(other, operator.lt)

    def __le__(self, other):
        return self.__compare__(other, operator.le)

    def __gt__(self, other):
        return self.__compare__(other, operator.gt)

    def __ge__(self, other):
        return self.__compare__(other, operator.ge)

    def __eq__(self, other):
        return self.__compare__(other, operator.eq)

    def __ne__(self, other):
        return self.__compare__(other, operator.ne)

    def __str__(self) -> str:
        return str(self.get_as_dict())

    def pretty_format(self):
        return json.dumps(self.get_as_dict(), indent=4, ensure_ascii=False)

    def get_as_dict(self) -> dict:
        return {"number": self.number, "question": self.question_text, "A": self.a, "B": self.b, "C": self.c,
                "D": self.d, "E": self.e, "ans": self.ans, "unit_text": self.unit_text, "unit": self.unit,
                "diagram": self.diagram_path, "subject": self.exam.subj, "year": self.exam.year, "month": self.exam.month}

    def get_as_html(self) -> str:
        return """
        <div class="col-md-10">
            <h3>Question {index} of {total}</h3>
            <h3 class="text-center">
                {question_text}
            </h3>
            {image}
            <div class="centered">
                <table style="margin-left:auto;margin-right:auto;">
                  <tr>
                    <td><button class="btn" id= "a" >A </button><font color="black" id="a_text">{q_a}</font></td>
                  </tr>
                  <tr>
                    <td><button class="btn" id= "b" >B </button><font color="black" id="b_text">{q_b}</font></td>
                  </tr>
                  <tr>
                    <td><button class="btn" id= "c" >C </button><font color="black" id="c_text">{q_c}</font></td>
                  </tr>
                  <tr>
                    <td><button class="btn" id= "d" >D </button><font color="black" id="d_text">{q_d}</font></td>
                  </tr>
                </table>
            </div> 
        </div>
        """.format(index=self.number, total=self.exam.num_questions, question_text=self.question_text,
                   image= "<img src=\"" + self.diagram_path + "\" alt=\"Diagram\">" if self.diagram_path is not None else "",
                   q_a=self.a, q_b=self.b, q_c=self.c, q_d=self.d)

    def get_validation_errors(self) -> list[str]:
        errors = list()
        if self.ans is None:
            errors.append("Answer is not set")
        if self.unit is None or self.unit == 0:
            errors.append("Unit is not set")
        if self.question_text is None:
            errors.append("Question text is not set")
        elif any(fig_key_word in self.question_text.lower() for fig_key_word in [" diagram ", " graph "]) and self.diagram_path is None:
            errors.append("Question text mentions a diagram but none defined.")
        if None in [self.a, self.b, self.c, self.d]:
            errors.append("A, B, C, and/or option D is not set")
        for label, text in [("Question", self.question_text), ("A", self.a), ("B", self.b), ("C", self.c), ("D", self.d)]:
            if text is not None:
                try:
                    text.encode('ascii')
                except UnicodeEncodeError as e:
                    errors.append("Invalid characters in " + label + ": '" + str(text[e.start:e.end])
                                  + "' at position " + str(e.start) + " to " + str(e.end))

        return errors

    def get_validation_warnings(self) -> list[str]:
        warnings = list()
        # Check to see if there are indications of a diagram but no diagram set
        if self.question_text is not None and any(x in self.question_text for x in self.diagram_hints):
            warnings.append("Question text indicates it may have a diagram, but no diagram is set.")

    def set_diagram(self, im: Image) -> None:
        # Set the diagram for the question. If an image is provided, save it to the path and set it. If an image
        # is not given, check to see if one exists at the expected path, set it if it does.
        possible_diagram = os.path.abspath(os.path.join(self.exam.working_dir, self.exam.working_dir + "_" + str(self.number) + ".png"))
        if im is not None:
            im.save(possible_diagram)
        if os.path.exists(possible_diagram):
            self.diagram_path = possible_diagram

    def delete_diagram(self) -> None:
        if self.diagram_path is not None and os.path.isfile(self.diagram_path):
            os.remove(self.diagram_path)
            self.diagram_path = None

    def set_unit(self, unit_text: str):
        self.unit_text = unit_text
        self.unit = None if unit_text is None else int(unit_text[0: unit_text.index(":")])


class Exam:
    def __init__(self, woring_dir: str, year: int, month: str, subj: str, answer_file: str, num_questions: int = None):
        self.working_dir = woring_dir
        self.year = year
        self.month = month
        self.subj = subj
        self.answers = dict()
        self.units = dict()
        self.num_questions = num_questions if num_questions is not None else DocumentControl.QUESTION_PER_SUBJECT[subj]
        self.questions = dict()
        self.formatted_answer_file = answer_file

        # Read in the correct answer, formatted as question_number answer_number unit_number[optional] one per line
        int_to_letter = {"1": "A", "2": "B", "3": "C", "4": "D"}
        with open(answer_file) as f:
            for line in f.readlines():
                if line.strip() != "":
                    tup = line.split()
                    self.answers[int(tup[0])] = int_to_letter.get(tup[1], tup[1])
                    if len(tup) == 3:
                        self.units[int(tup[0])] = int(tup[2])

    def __eq__(self, other):
        if isinstance(other, Exam):
            return self.year == other.year and self.month == other.month and self.subj == other.subj
        else:
            raise TypeError("Only exams can be compared to each other")

    def generate_questions_from_file(self, questions_file: str) -> set:
        # Read in and parse the exam
        with open(questions_file) as f:
            lines = f.readlines()
        return self.generate_questions_from_text(lines)

    def generate_questions_from_text(self, lines: list) -> set:
        # If there is a file that maps the NYRP units to our units, read it and store it in memoery, use later
        units = dict()
        nyrp_unit_file = os.path.join(self.working_dir, self.working_dir + "_guide.txt")
        if os.path.exists(nyrp_unit_file):
            with open(nyrp_unit_file, "r") as unit_file_in:
                for line in unit_file_in:
                    q, u = line.split()
                    units[int(q)] = u
        errors = set()
        found_questions = set()
        for i in range(len(lines)):
            # Search for the start of a question
            match = re.compile(r"^\d+ ").match(lines[i])
            if match is not None and 0 < int(match.group(0)) <= self.num_questions:
                question_number = int(match.group(0))
                # Start of a question and answers (trim its number) and don't end until the next question
                # is found or the end of the file
                question_block = lines[i][len(match.group(0)):].rstrip()
                i += 1
                while i < len(lines) and re.compile(r"^\d{1,2} ").match(lines[i]) is None:
                    question_block += " " + lines[i].rstrip()
                    i += 1
                i -= 1

                # Parse through the text of answers looking for (1), (2), (3), and (4)
                # These are not guaranteed to be in any particular order, or even present
                opts = {1: None, 2: None, 3: None, 4: None}
                question_text = None
                try:
                    indexes = sorted([question_block.index("(" + str(i) + ")") for i in range(1, 5)])
                    question_text = question_block[:indexes[0]].rstrip()
                    # TODO look for key words in the question text to highlight a question as needing a diagram
                    for j in range(4):
                        answer_num = int(question_block[int(indexes[j] + 1)])
                        start = indexes[j]
                        end = indexes[j + 1] if j + 1 < 4 else -1
                        opts[answer_num] = question_block[start:end].replace("\n", " ").strip()[4:]
                except ValueError:
                    errors.add("Failed to find all answers for question " + str(question_number))

                unit_text = None
                # First check a previous in-memory version of the test
                if self.questions.get(question_number) is not None:
                    unit_text = self.questions[question_number].unit_text
                # Second, look at the answer file when the exam was originally loaded
                elif self.units.get(question_number) is not None:
                    unit_text = Units.get_units(self.subj)[(self.units.get(question_number))][1]
                # Third, Check to see if we read in the unit file
                elif units.get(question_number) is not None:
                    unit_text = Units.guess_unit(self.subj, units.get(question_number))
                # Fourth, try to guess the unit if the unit is zero
                elif unit_text is None or "0: None" in unit_text:  # TODO change to enum rather than string
                    question_and_answers = " {} {} {} {} {} ".format(question_text, opts[1], opts[2], opts[3], opts[4])\
                        .replace(",", " ").replace(".", " ").replace("?", " ").lower()
                    unit_text = Units.guess_unit(self.subj, question_and_answers)
                # Check to see if we already found this question this round
                if question_number in found_questions:
                    errors.add("Found multiple question candidates for #" + str(question_number))
                found_questions.add(question_number)
                self.questions[question_number] = Question(self, question_number, question_text,
                                                           opts[1], opts[2], opts[3], opts[4], None,
                                                           self.answers[question_number], unit_text)
        # Create empty questions for those we couldn't find
        for i in range(self.num_questions):
            if i + 1 not in self.questions:
                self.questions[i + 1] = Question(self, i + 1, None, None, None, None, None, None, self.answers[i + 1], None)

        for error in errors:
            print(error)
        # Return the errors
        return errors

    def is_valid(self) -> bool:
        questions_valid = len(self.get_invalid_questions()) == 0 and len(self.questions) == self.num_questions
        exam_valid = None not in [self.year, self.month, self.subj]
        return questions_valid and exam_valid

    def get_invalid_questions(self) -> list:
        """
        Returns a list of invalid questions
        """
        invalid_questions = list()
        valid_questions_text = set()
        for _, question in self.questions.items():
            if len(question.get_validation_errors()) > 0 or question.question_text in valid_questions_text:
                invalid_questions.append(question)
            else:
                valid_questions_text.add(question.question_text)
        return invalid_questions

    def finalize(self, filepath: str, ignore_errors: bool = False) -> None:
        """
        When all questions are formatted correctly, write them out to a JSON file for ingestion in a database later
        """
        if self.is_valid() or ignore_errors:
            with open(filepath, "w") as outf:
                fin_quest = [q.get_as_dict() for q in sorted(self.questions.values())]
                for q in fin_quest:
                    del q["number"]
                    del q["unit_text"]
                outf.write(json.dumps(fin_quest, indent=4))
        else:
            invalid_questions = self.get_invalid_questions()
            if len(invalid_questions) == 0:
                raise Exception("Questions are valid, but the exam is not, check year/month/subject are set")
            else:
                raise Exception("Validation errors on Questions: " + str(invalid_questions))

    def get_question(self, question_number: int) -> Question:
        # This is one indexed, the first question is "question 1"
        return self.questions.get(question_number)


if __name__ == "__main__":
    working_dir = sys.argv[1]
    exam = Exam(working_dir, 2024, "January", "CHEM", working_dir + "\\2024_Jan_chem_exam.txt",
                working_dir + "\\2024_Jan_chem_ans_formatted.txt")
    print(len(exam.get_invalid_questions()))
    for question in sorted(exam.get_invalid_questions()):
        print(str(question.number) + " : " + str(question.get_validation_errors()) + " : " + str(question))
