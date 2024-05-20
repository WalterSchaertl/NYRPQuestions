import json
import operator
import os
import re
import sys
from typing import Optional
from PIL import Image


class Question:
    compare_error = "Questions must have the same exam to compare"
    diagram_hints = ["diagram", "figure", "plot", "chart"]

    def __init__(self, exam: "Exam", number: int, question_text: Optional[str], a: Optional[str],
                 b: Optional[str], c: Optional[str], d: Optional[str], e: Optional[str], ans: int,
                 unit: Optional[str]):
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
        self.e = e
        self.ans = ans
        self.unit = unit
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
                "D": self.d, "E": self.e, "ans": self.ans, "unit": self.unit, "diagram": self.diagram_path,
                "subject": self.exam.subj, "year": self.exam.year, "month": self.exam.month}

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
                    <td><button class="btn" id= "a" >A</button><font color="black" id="a_text">{q_a}</font></td>
                  </tr>
                  <tr>
                    <td><button class="btn" id= "b" >B</button><font color="black" id="b_text">{q_b}</font></td>
                  </tr>
                  <tr>
                    <td><button class="btn" id= "c" >C</button><font color="black" id="c_text">{q_c}</font></td>
                  </tr>
                  <tr>
                    <td><button class="btn" id= "d" >D</button><font color="black" id="d_text">{q_d}</font></td>
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
        if self.unit is None:
            errors.append("Unit is not set")
        if self.question_text is None:
            errors.append("Question text is not set")
        if None in [self.a, self.b, self.c, self.d]:
            errors.append("A, B, C, and/or option D is not set")
        return errors

    def get_validation_warnings(self) -> list[str]:
        warnings = list()
        # Check to see if there are indications of a diagram but no diagram set
        if self.question_text is not None and any(x in self.question_text for x in self.diagram_hints):
            warnings.append("Question text indicates it may have a diagram, but no diagram is set.")

    def set_diagram(self, im: Image) -> None:
        # Set the diagram for the question. If an image is provided, save it to the path and set it. If an image
        # is not given, check to see if one exists at the expected path, set it if it does.
        possible_diagram = os.path.join(self.exam.working_dir, self.exam.working_dir + "_" + str(self.number) + ".png")
        if im is not None:
            im.save(possible_diagram)
        if os.path.exists(possible_diagram):
            self.diagram_path = possible_diagram

    def delete_diagram(self) -> None:
        if self.diagram_path is not None and os.path.isfile(self.diagram_path):
            os.remove(self.diagram_path)
            self.diagram_path = None

class Exam:
    def __init__(self, woring_dir: str, year: str, month: str, subj: str, answer_file: str, num_questions: int = 50):
        self.working_dir = woring_dir
        self.year = year
        self.month = month
        self.subj = subj
        self.answers = dict()
        self.num_questions = num_questions
        self.questions = dict()

        # Read in the correct answer
        with open(answer_file) as f:
            for line in f.readlines():
                if line.strip() != "":
                    q, a = line.split()
                    self.answers[int(q)] = int(a)

    def __eq__(self, other):
        if isinstance(other, Exam):
            return self.year == other.year and self.month == other.month and self.subj == other.subj
        else:
            raise TypeError("Only exams can be compared to each other")

    def generate_questions_from_file(self, questions_file: str):
        # Read in and parse the exam
        with open(questions_file) as f:
            lines = f.readlines()
        self.generate_questions_from_text(lines)

    def generate_questions_from_text(self, lines: list):
        for i in range(len(lines)):
            # Search for the start of a question
            match = re.compile(r"^\d+ ").match(lines[i])
            if match is not None and int(match.group(0)) <= 50:
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
                    print("Failed to find all answers for question " + str(question_number))

                self.questions[question_number] = Question(self, question_number, question_text,
                                                           opts[1], opts[2], opts[3], opts[4], None,
                                                           self.answers[question_number], None)
        # Create empty questions for those we couldn't find
        for i in range(self.num_questions):
            if i + 1 not in self.questions:
                self.questions[i + 1] = Question(self, i + 1, None, None, None, None, None, None, self.answers[i + 1], None)

    def is_valid(self) -> bool:
        questions_valid = len(self.get_invalid_questions()) == 0 and len(self.questions) == self.num_questions
        exam_valid = None not in [self.year, self.month, self.subj]
        return questions_valid and exam_valid

    def get_invalid_questions(self) -> (list, list):
        """
        Returns a tuple, first is a list of invalid question numbers, second is the actual questions
        """
        invalid_questions = list()
        for _, question in self.questions.items():
            if len(question.get_validation_errors()) > 0:
                invalid_questions.append(question)
        return invalid_questions, [q.number for q in invalid_questions]

    def finalize(self, filepath: str) -> None:
        """
        When all questions are formatted correctly, write them out to a JSON file for ingestion in a database later
        """
        if self.is_valid():
            with open(filepath, "w") as outf:
                outf.write(json.dumps(sorted(self.questions.values()), indent=4))
        else:
            invalid_questions = self.get_invalid_questions()[0]
            if len(invalid_questions) == 0:
                raise Exception("Questions are valid, but the exam is not, check year/month/subject are set")
            else:
                raise Exception("Validation errors on Questions: " + str(invalid_questions))

    def get_question(self, question_number: int) -> Question:
        # This is one indexed, the first question is "question 1"
        return self.questions.get(question_number)


if __name__ == "__main__":
    working_dir = sys.argv[1]
    exam = Exam(working_dir, "2024", "Jan", "Chem", working_dir + "\\2024_Jan_chem_exam.txt",
                working_dir + "\\2024_Jan_chem_ans_formatted.txt")
    print(len(exam.get_invalid_questions()))
    for question in sorted(exam.get_invalid_questions()[0]):
        print(str(question.number) + " : " + str(question.get_validation_errors()) + " : " + str(question))
