import datetime
import os
import tkinter.scrolledtext
import traceback
from tkinter import *
from tkinter import filedialog
from typing import Optional

import DocumentControl
import Exam
# Custom fork to support super and sub scripts, if you want to run this yourself, changing the package to tkhtmlview
# will support everything but those tags.
from tk_html_widgets import HTMLLabel
from pynput import mouse
from PIL import ImageGrab

import Units


class GUI(Tk):
    def __init__(self):
        self.exam = None
        self.current_question = 1

        super().__init__()

        # TODO refactor major GUI components as classes
        self.title('Question Creator')
        self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(tuple(range(11)), weight=1)
        self.rowconfigure(tuple(range(11)), weight=1)

        self.resizable(True, True)
        self.doc_control = None

        # text view of the test
        self.pdf_text = tkinter.scrolledtext.ScrolledText(self, undo=True)
        self.pdf_text.insert(END,  "<Load an exam to populate this text box>")
        self.pdf_text.grid(row=1, rowspan=10, column=6, columnspan=5, padx=20, pady=5, sticky="nsew")

        # Load/finish buttons
        load_file = Button(self, text="Load File", command=self.file_conversion)
        load_file.grid(column=0, row=0, sticky="nsew", padx=20, pady=5)
        finish = Button(self, text="Finish", command=self.save_and_exit)
        finish.grid(column=10, row=0, sticky="nsew", padx=20, pady=5)

        # Rendered question
        self.rend_q = HTMLLabel(self, html="The HTML rendition of the question")
        self.rend_q.grid(row=1, rowspan=6, column=0, columnspan=6, padx=20, pady=5, sticky="nsew")

        # Operation buttons
        button_frame = Frame(self, bg="green")
        button_frame.grid(row=7, column=0, columnspan=6, sticky="nsew", padx=20, pady=5)
        self.selected_unit = StringVar()
        self.selected_unit.set("Load an exam to select a label")
        self.select_unit = OptionMenu(button_frame, self.selected_unit, "Load an exam to select a label")

        prev_q = Button(button_frame, text="Previous", command=self.previous_question)
        upload_pic = Button(button_frame, text="Delete Diagram", command=self.delete_diagram)
        take_pic = Button(button_frame, text="Capture Diagram", command=self.get_diagram)
        hyper = Button(button_frame, text="Superscript", command=lambda: self.format_text("super"))
        sub = Button(button_frame, text="Subscript", command=lambda: self.format_text("sub"))
        save_unit = Button(button_frame, text="Set Unit", command=self.save_unit_to_question)
        next_q = Button(button_frame, text="Next", command=self.next_question)
        for button in [prev_q, upload_pic, take_pic, self.select_unit, save_unit, hyper, sub, next_q]:
            button.pack(expand=True, fill='both', side=tkinter.LEFT)

        # Math formatting buttons
        math_button_frame = Frame(self, bg="green")
        math_button_frame.grid(row=8, column=0, columnspan=6, sticky="nsew", padx=20, pady=5)
        math_char = Button(math_button_frame, text="Convert Chars", command=lambda: self.format_text("ital"))
        lte = Button(math_button_frame, text="≤", command=lambda: self.pdf_text.insert(self.pdf_text.index(INSERT), "≤"))
        gte = Button(math_button_frame, text="≥", command=lambda: self.pdf_text.insert(self.pdf_text.index(INSERT), "≥"))
        times = Button(math_button_frame, text="•", command=lambda: self.pdf_text.insert(self.pdf_text.index(INSERT), "•"))
        rad = Button(math_button_frame, text="√", command=lambda:self.format_text("rad"))
        for button in [math_char, lte, gte, times, rad]:
            button.pack(expand=True, fill='both', side=tkinter.LEFT)

        # Question Text
        self.raw_q = Text(self)
        self.raw_q.insert(END, "Just the question layout")
        self.raw_q.grid(row=9, rowspan=2, column=0, columnspan=6, padx=20, pady=5, sticky="nsew")

        # Bottom Label
        self.bottom_l = Label(self, text="Working all day")
        self.bottom_l.grid(row=11, column=0, columnspan=5, padx=5, pady=5)

        # Read the Text and make the questions
        generate_questions = Button(self, text="Generate Questions", command=self.create_questions)
        generate_questions.grid(row=11, column=6, columnspan=1, padx=5, pady=5)

        # Save edits made to the exam in a _in_progress file
        save_exam_file = Button(self, text="Save Exam Text", command=self.save_file)
        save_exam_file.grid(row=11, column=7, columnspan=1, padx=20, pady=5)
        self.exam_filename = None

        # Trigger the final generation of the exam, to be read into the sql db by NYRP
        submit_questions = Button(self, text="Submit Questions", command=self.submit_questions)
        submit_questions.grid(row=11, column=8, columnspan=1, padx=20, pady=5)

    def save_and_exit(self):
        self.save_file()
        self.destroy()

    # TODO is this the right place for this? Might belong in document control
    def save_file(self):
        if self.exam_filename is not None:
            # TODO better way of track in progress files without overwriting the original
            saved_exam_file = self.exam_filename[0: self.exam_filename.rfind(".")]
            if not saved_exam_file.endswith("_in_progress"):
                saved_exam_file += "_in_progress"
            try:
                with open(saved_exam_file + ".txt", "w", encoding="utf-8") as outex:
                    outex.write(self.pdf_text.get(1.0, "end-1c"))
                self.bottom_l.config(text="Exam saved!", fg="green")
                with open(self.exam.formatted_answer_file, "w") as outa:
                    for i in range(1, self.exam.num_questions + 1):
                        quest = self.exam.get_question(i)
                        unit = quest.unit if quest.unit is not None else ""
                        outa.write(str(i) + " " + str(quest.ans) + " " + str(unit) + "\n")
            except UnicodeEncodeError as e:
                self.bottom_l.config(text="Failed to save file: " + str(e), fg="red")
        else:
            self.bottom_l.config(text="No Exam loaded to save", fg="red")

    def refresh_unit_menu(self, default: Optional[str]):
        menu = self.select_unit.children["menu"]
        menu.delete(0, "end")
        labels = [label for _, label in Units.get_units(self.exam.subj)]
        for new_label in labels:
            menu.add_command(label=new_label, command=lambda v=new_label: self.selected_unit.set(v))
        if default is not None:
            self.selected_unit.set(default)
        else:
            self.selected_unit.set(labels[0])

    def save_unit_to_question(self):
        self.exam.get_question(self.current_question).set_unit(self.selected_unit.get())
        self.render_question()

    def next_question(self):
        if self.exam is None:
            self.bottom_l.config(text="An exam must be loaded before questions can be selected", fg="red")
            return
        self.save_unit_to_question()
        self.current_question = min(self.current_question + 1, self.exam.num_questions)
        self.render_question()

    def previous_question(self):
        if self.exam is None:
            self.bottom_l.config(text="An exam must be loaded before questions can be selected", fg="red")
            return
        self.save_unit_to_question()
        self.current_question = max(self.current_question - 1, 1)
        self.render_question()

    def render_question(self):
        self.raw_q.delete("1.0", END)
        self.raw_q.insert("1.0", self.exam.get_question(self.current_question).pretty_format())
        self.rend_q.html_parser.cached_images = {}  # Force a reread of the image captured
        current_question = self.exam.get_question(self.current_question)
        self.rend_q.set_html(current_question.get_as_html())
        self.refresh_unit_menu(current_question.unit_text)

    def create_questions(self):
        if self.exam is None:
            self.bottom_l.config(text="An exam must be loaded before questions can be generated", fg="red")
            return
        errors = self.exam.generate_questions_from_text(self.pdf_text.get("1.0", "end-1c").splitlines())
        self.render_question()
        self.bottom_l.config(text="Questions rendered!", fg="green")
        if len(errors) > 0:
            # Popup with the exam loading failures
            win = Toplevel(self)
            win.title("Errors in question generation")
            error_text_label = tkinter.scrolledtext.ScrolledText(win)
            error_text_label.pack(expand=True, fill='both', side=tkinter.LEFT)
            error_text_label.insert("1.0", "\n".join(sorted(errors)))

    def get_diagram(self):
        if self.exam is None:
            self.bottom_l.config(text="An exam must be loaded before Diagrams can be obtained", fg="red")
            return
        # TODO refactor as an invisible window, draw rectangle when mouse is held down (currently two clicks to
        #  stop text from being highlighted on a drag), release to capture
        self.bottom_l.configure(text="Click the left mouse button at the corners of the image")
        coords = [-1, -1, -1, -1]

        def on_click(x, y, button, pressed):
            if button == mouse.Button.left and pressed:
                if coords[0] == -1:
                    coords[0] = x
                    coords[1] = y
                else:
                    coords[2] = x
                    coords[3] = y
                    return False
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        listener.join()
        bbox = (min(coords[0], coords[2]), min(coords[1], coords[3]), max(coords[0], coords[2]), max(coords[1], coords[3]))
        self.exam.get_question(self.current_question).set_diagram(ImageGrab.grab(bbox=bbox, all_screens=True))
        self.render_question()
        self.bottom_l.configure(text="")

    def delete_diagram(self):
        if self.exam is None:
            self.bottom_l.config(text="An exam must be loaded before Diagrams can be deleted", fg="red")
            return
        self.exam.get_question(self.current_question).delete_diagram()
        self.render_question()

    def format_text(self, operation):
        if operation == "super":
            self.pdf_text.insert("sel.first", "<sup>")
            self.pdf_text.insert("sel.last", "</sup>")
        elif operation == "sub":
            self.pdf_text.insert("sel.first", "<sub>")
            self.pdf_text.insert("sel.last", "</sub>")
        elif operation == "rad":
            self.pdf_text.insert("sel.first", "√(")
            self.pdf_text.insert("sel.last", ")")
        elif operation == "ital":
            # This is far from a perfect solution, it can get confused by lone '>' and '<' thinking they're html tags,
            # and will tag characters individually tht could be combined, but it still works better than setting italics
            # for the entire of each selection
            text = self.pdf_text.get('sel.first', 'sel.last')
            if "<i>" in text:
                self.pdf_text.replace("sel.first", "sel.last", text.replace("<i>", "").replace("</i>", ""))
            else:
                replace_text = list()
                skip_tag = False
                for char in text:
                    # Skip characters in tags
                    if char == "<":
                        skip_tag = True
                    elif char == ">":
                        skip_tag = False
                        replace_text.append(char)
                        continue
                    if skip_tag or ord(char) < ord('A') or ord('Z') < ord(char) < ord('a') or ord(char) > ord('z'):
                        replace_text.append(char)
                    else:
                        replace_text.extend([c for c in "<i>" + char + "</i>"])
                self.pdf_text.replace("sel.first", "sel.last", "".join(replace_text))
        else:
            self.bottom_l.config(text="Unrecognized operation " + operation, fg="red")

    # def convert_to_from_math(self):
    #     # Within a highlighted area, convert each letter to a math letter (or back from a math letter)
    #     # This is showing some issues on Text display and exam ingestion, so for now it's being left
    #     # unused and should be an improvement for the future.
    #     # Start of the conversion block, minus the offset of normal characters
    #     math_upper_start = ord('𝐴')
    #     math_lower_start = ord('𝑎')
    #     uppercase_offset = math_upper_start - ord('A')
    #     lowercase_offset = math_lower_start - ord('a')
    #     skip_tag = False
    #     # Iterate over all characters in the selection, replace with their math versions
    #     chars_to_convert = list(self.pdf_text.get('sel.first', 'sel.last'))
    #     for index in range(len(chars_to_convert)):
    #         replace_char = chars_to_convert[index]
    #         # Skip characters in tags
    #         if replace_char == "<":
    #             skip_tag = True
    #         elif replace_char == ">":
    #             skip_tag = False
    #             chars_to_convert[index] = replace_char
    #             continue
    #
    #         if skip_tag:
    #             chars_to_convert[index] = replace_char
    #         # Special case, math h doesn't exist where it 'should'
    #         elif replace_char == 'h':
    #             chars_to_convert[index] = 'ℎ'
    #         elif replace_char == 'ℎ':
    #             chars_to_convert[index] = 'h'
    #         # Convert uppercase normal to math versions
    #         elif ord('A') <= ord(replace_char) <= ord('Z'):
    #             chars_to_convert[index] = chr(ord(replace_char) + uppercase_offset)
    #         elif ord('a') <= ord(replace_char) <= ord('z'):
    #             chars_to_convert[index] = chr(ord(replace_char) + lowercase_offset)
    #         # Convert math versions to normal
    #         elif math_upper_start <= ord(replace_char) < math_upper_start + 26:
    #             chars_to_convert[index] = chr(ord(replace_char) - uppercase_offset)
    #         elif math_lower_start <= ord(replace_char) < math_lower_start + 26:
    #             chars_to_convert[index] = chr(ord(replace_char) - lowercase_offset)
    #     self.pdf_text.replace("sel.first", "sel.last", "".join(chars_to_convert))

    def submit_questions(self):
        if self.exam is None:
            self.bottom_l.config(text="An exam must be loaded before it can be finalized", fg="red")
            return
        if self.exam.is_valid():
            self.bottom_l.config(text="Saving valid exam!", fg="green")
            self.exam.finalize(os.path.join(self.exam.working_dir, "saved_exam.json"))
        else:
            self.bottom_l.config(text="Fix exam errors before the exam can be saved", fg="red")
            # Popup with the invalid questions and their errors
            win = Toplevel(self)
            win.title("Questions with errors")
            error_text_label = tkinter.scrolledtext.ScrolledText(win)
            error_text_label.pack(expand=True, fill='both', side=tkinter.LEFT)
            text = ""
            for q in sorted(self.exam.get_invalid_questions(), key=lambda q: q.number):
                text += str(q.number) + "\n"
                errors = q.get_validation_errors()
                # Question is flagged as invalid, but no errors for it
                if len(errors) == 0:
                    errors.append("Question has the same question text as another question")
                for error in errors:
                    text += "  " + error + "\n"

            error_text_label.insert("1.0", text)

            submit_anyway = Button(win, text="Submit Anyways", command=lambda: self.submit_anyways(win))
            submit_anyway.pack(expand=True, fill='both', side=tkinter.LEFT)

    def submit_anyways(self, win):
        self.exam.finalize(os.path.join(self.exam.working_dir, "saved_exam.json"), True)
        self.bottom_l.config(text="Saving invalid exam!", fg="blue")
        win.destroy()

    def file_conversion(self):
        """
        Pop up window when the user wants to load the exam and answer files.
        """
        def select_file(label_to_update: Label, parent_frame: Toplevel, title: str="Select a File") -> None:
            filename = filedialog.askopenfilename(initialdir=DocumentControl.DOCUMENT_ROOT,
                                                  title=title,
                                                  filetypes=( ("Text files", "*.txt*"), ("PDF files", "*.pdf*")))
            label_to_update.configure(text=filename)
            parent_frame.focus_force()

        def load_files(exam_year: int, exam_month: str, exam_subj: str, exam_file: str, ans_file: str, win: Toplevel) -> None:
            # User checking that the year/month/subject don't match the exam and answer file names
            if ans_file != "" and exam_file != "" and "http" not in ans_file and "http" not in exam_file:
                for check_in in [str(x).lower() for x in [exam_year, exam_month, exam_subj]]:
                    if check_in not in exam_file.lower() or check_in not in ans_file.lower():
                        status_l.config(text="Year, month, and/or subject not in both answer and exam filename.", fg="red")
                        status_l.update()
                        return
            self.doc_control = DocumentControl.DocumentControl(exam_year, exam_month, exam_subj)
            # If the local exam file or answer files aren't set, see if we can get them based on the year/month/subject
            base_name = os.path.join(self.doc_control.working_dir, self.doc_control.working_dir + "_")
            if exam_file == "":
                exam_file = base_name + "exam_in_progress.txt"
            if ans_file == "":
                ans_file = base_name + "ans_formatted.txt"
            # Validate all files saved
            if "" in [exam_year, exam_month, exam_subj, exam_file, ans_file]:
                status_l.config(text="Missing one or more of: year, month, subject, exam file, answer file.", fg="red")
                status_l.update()
                return
            status_l.config(text="Process started, this make take up to 10 seconds", fg="blue")
            self.update()
            try:
                # Load the selected files in to Document Control to be parsed, get back the formatted text exam/answers
                text_exam = self.doc_control.get_conversion(exam_file, "exam")
                with(open(text_exam, "r", encoding='utf-8', errors="replace")) as infile:
                    self.pdf_text.delete("1.0", END)
                    # Convert less common unicode characters to their ASCII counterparts
                    transl_table = dict([(ord(x), ord(y)) for x, y in zip(u"‘’´“”–-", u"'''\"\"--")])
                    clean_text_exam = infile.read().translate(transl_table)
                    self.pdf_text.insert("1.0", clean_text_exam)
                    # Save the exam file path of the local version
                    self.exam_filename = text_exam
                # TODO this is a hack, find a real solution that doesn't relay on magic names to
                # determine if an answer text file should really be processed or not
                text_ans = self.doc_control.get_conversion(ans_file, "ans" if "formatted" not in ans_file else "ans_formatted")
                text_ans_formatted = self.doc_control.reformat_answer_key(text_ans, exam_subj)
                # Load it into the exam and let the user edit the text box before making questions.
                self.exam = Exam.Exam(self.doc_control.working_dir, exam_year, exam_month, exam_subj, text_ans_formatted)
                # Auto create questions and close window
                self.create_questions()
                win.destroy()
            except Exception as e:
                traceback.print_exc()
                status_l.config(text=str(e), fg="red")

        win = Toplevel(self)
        win.columnconfigure(tuple(range(10)), weight=1)
        win.rowconfigure(tuple(range(11)), weight=1)
        win.wm_title("File Conversion")

        # form data
        year = IntVar()
        month = StringVar()
        subject = StringVar()
        remote_exam = StringVar()
        remote_ans = StringVar()

        # Year, Month, Subject inputs
        year_l = Label(win, text="Exam year")
        year_l.grid(row=0, column=2, columnspan=3)
        year.set(datetime.datetime.now().date().strftime("%Y"))
        year_i = Entry(win, textvariable=year)
        year_i.grid(row=0, column=7, columnspan=3)

        month_l = Label(win, text="Exam month")
        month_l.grid(row=1, column=2, columnspan=3)
        month.set(DocumentControl.SUPPORTED_MONTHS[0])
        month_i = OptionMenu(win, month, *DocumentControl.SUPPORTED_MONTHS)
        month_i.grid(row=1, column=7, columnspan=3)

        subj_l = Label(win, text="Exam subject")
        subj_l.grid(row=2, column=2, columnspan=3)
        subject.set(DocumentControl.SUPPORTED_SUBJECTS[0])
        subj_i = OptionMenu(win, subject, *DocumentControl.SUPPORTED_SUBJECTS)
        subj_i.grid(row=2, column=7, columnspan=3)

        input_options_l = Label(win, text="Select ONE of the two methods to load files: local or remote")
        input_options_l.grid(row=3, column=0, columnspan=10)

        # Inputs for a local file to convert, or text file that has already been converted
        local_l = Label(win, text="1) Select the local PDFs to convert, or converted text files")
        local_l.grid(row=4, column=0, columnspan=6, sticky="nsw")
        local_exam_l = Label(win)
        local_exam_l.grid(row=5, column=7, columnspan=3, sticky="w")
        local_exam = Button(win, text="Select exam PDF/TXT", command=lambda: select_file(local_exam_l, win, "Select an Exam"))
        local_exam.grid(row=5, column=2, columnspan=3, padx=(20, 2), sticky="nsew")

        local_ans_l = Label(win)
        local_ans_l.grid(row=6, column=7, columnspan=3, sticky="w")
        local_ans = Button(win, text="Select answer PDF/TXT", command=lambda: select_file(local_ans_l, win, "Select an Answer"))
        local_ans.grid(row=6, column=2, columnspan=3, padx=(20, 2), sticky="nsew")

        load_local_files = Button(win, text="Load Local Files",
                                  command=lambda: load_files(year.get(), month.get(), subject.get(),
                                                             local_exam_l.cget("text"), local_ans_l.cget("text"), win))
        load_local_files.grid(row=5, column=10, rowspan=2, sticky="nsew", padx=5, pady=5)

        # Inputs for a remote URL file to convert
        remote_l = Label(win, text="2) Enter the URLs of the remote PDF files")
        remote_l.grid(row=7, column=0, columnspan=6, sticky="nsw")
        remote_exam_l = Label(win, text="Exam PDF")
        remote_exam_l.grid(row=8, column=2, columnspan=3, sticky="nsew")
        remote_exam = Entry(win, textvariable=remote_exam)
        remote_exam.grid(row=8, column=7, columnspan=3, padx=(20, 2), sticky="nsew")

        remote_ans_l = Label(win, text="Answer PDF")
        remote_ans_l.grid(row=9, column=2, columnspan=3, sticky="nsew")
        remote_ans = Entry(win, textvariable=remote_ans)
        remote_ans.grid(row=9, column=7, columnspan=3, padx=(20, 2), sticky="nsew")

        remote_load_files = Button(win, text="Load Remote Files",
                                  command=lambda: load_files(year.get(), month.get(), subject.get(),
                                                             remote_exam.get(), remote_ans.get(), win))
        remote_load_files.grid(row=8, column=10, rowspan=2, sticky="nsew", padx=5, pady=5)

        status_l = Label(win, fg="red")
        status_l.grid(row=10, column=0, columnspan=10)

        close_file_select = Button(win, text="Close", command=win.destroy)
        close_file_select.grid(row=0, column=10)


if __name__ == "__main__":
   app = GUI()
   app.mainloop()
