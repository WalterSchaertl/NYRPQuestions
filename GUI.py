import datetime
import traceback
from tkinter import *
from tkinter import filedialog
import DocumentControl
import Exam


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
        self.text_of_exam = "<Load an exam to populate this text box>"
        self.pdf_text = Text(self)
        self.pdf_text.insert(END, self.text_of_exam)
        self.pdf_text.grid(row=1, rowspan=9, column=6, columnspan=5, padx=20, pady=5, sticky="nsew")

        # self.create_widgets()

        # Load/finish buttons
        load_file = Button(self, text="Load File", command=self.file_conversion)
        load_file.grid(column=0, row=0, sticky="nsew", padx=20, pady=5)
        finish = Button(self, text="Finish")
        finish.grid(column=10, row=0, sticky="nsew", padx=20, pady=5)

        # Rendered question
        rend_q = Text(self)
        rend_q.insert(END, "The HTML rendition of the question")
        rend_q.grid(row=1, rowspan=4, column=0, columnspan=6, padx=20, pady=5, sticky="nsew")

        # Operation buttons
        prev_q = Button(self, text="Previous", command=self.previous_question)
        prev_q.grid(row=5, column=0, padx=(20, 2), sticky="nsew")
        upload_pic = Button(self, text="Upload Pic")
        upload_pic.grid(row=5, column=1, padx=2, sticky="nsew")
        take_pic = Button(self, text="Take Pic")
        take_pic.grid(row=5, column=2, padx=2, sticky="nsew")
        hyper = Button(self, text="Hyperscript")
        hyper.grid(row=5, column=3, padx=2, sticky="nsew")
        sub = Button(self, text="Subscript")
        sub.grid(row=5, column=4, padx=2, sticky="nsew")
        next_q = Button(self, text="Next", command=self.next_question)
        next_q.grid(row=5, column=5, padx=(2, 20), sticky="nsew")

        # Question Text
        self.raw_q = Text(self)
        self.raw_q.insert(END, "Just the question layout")
        self.raw_q.grid(row=6, rowspan=4, column=0, columnspan=6, padx=20, pady=5, sticky="nsew")

        # Bottom Label
        bottom_l = Label(self, text="Working all day")
        bottom_l.grid(row=10, column=0, columnspan=5, padx=5, pady=5)

        # Read the Text and make the questions
        generate_questions = Button(self, text="Generate Questions", command=self.create_questions)
        generate_questions.grid(row=10, column=6, columnspan=5, padx=5, pady=5)

    def next_question(self):
        self.current_question = min(self.current_question + 1, self.exam.num_questions)
        self.render_question()

    def previous_question(self):
        self.current_question = max(self.current_question - 1, 1)
        self.render_question()

    def render_question(self):
        self.raw_q.delete("1.0", END)
        self.raw_q.insert("1.0", self.exam.get_question(self.current_question).pretty_format())

    def create_questions(self):
        self.exam.generate_questions_from_text(self.pdf_text.get("1.0", "end-1c").splitlines())
        self.render_question()

    def file_conversion(self):
        """
        Pop up window when the user wants to load the exam and answer files.
        """
        def select_file(label_to_update: Label, parent_frame: Toplevel) -> None:
            filename = filedialog.askopenfilename(initialdir=DocumentControl.DOCUMENT_ROOT,
                                                  title="Select a File",
                                                  filetypes=( ("Text files", "*.txt*"), ("PDF files", "*.pdf*")))
            label_to_update.configure(text=filename)
            parent_frame.focus_force()

        def load_files(exam_year: str, exam_month: str, exam_subj: str, exam_file: str, ans_file: str) -> None:
            status_l.config(text="Process started, this make take up to 10 seconds", fg="blue")
            self.update()
            try:
                # Load the selected files in to Document Control to be parsed, get back the formated text exam/answers
                self.doc_control = DocumentControl.DocumentControl(exam_year, exam_month, exam_subj)
                text_exam = self.doc_control.get_conversion(exam_file, "exam")
                with(open(text_exam, "r")) as infile:
                    self.text_of_exam = infile.read()
                    self.pdf_text.insert(END, self.text_of_exam)
                # TODO this is a hack, find a real solution that doesn't relay on magic names to
                # determine if an answer text file should really be processed or not
                text_ans = self.doc_control.get_conversion(ans_file, "ans" if "formatted" not in ans_file else "ans_formatted")
                text_ans_formatted = self.doc_control.reformat_answer_key(text_ans)
                # Load it into the exam and let the user edit the text box before making questions.
                self.exam = Exam.Exam(self.doc_control.working_dir, exam_year, exam_month, exam_subj, text_ans_formatted)
                status_l.config(text="Finished! You can close this now", fg="green")
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
        local_exam = Button(win, text="Select exam PDF/TXT", command=lambda: select_file(local_exam_l, win))
        local_exam.grid(row=5, column=2, columnspan=3, padx=(20, 2), sticky="nsew")

        local_ans_l = Label(win)
        local_ans_l.grid(row=6, column=7, columnspan=3, sticky="w")
        local_ans = Button(win, text="Select answer PDF/TXT", command=lambda: select_file(local_ans_l, win))
        local_ans.grid(row=6, column=2, columnspan=3, padx=(20, 2), sticky="nsew")

        load_local_files = Button(win, text="Load Local Files",
                                  command=lambda: load_files(str(year.get()), month.get(), subject.get(),
                                                             local_exam_l.cget("text"), local_ans_l.cget("text")))
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
                                  command=lambda: load_files(str(year.get()), month.get(), subject.get(),
                                                             remote_exam.get(), remote_ans.get()))
        remote_load_files.grid(row=8, column=10, rowspan=2, sticky="nsew", padx=5, pady=5)

        status_l = Label(win, fg="red")
        status_l.grid(row=10, column=0, columnspan=10)

        close_file_select = Button(win, text="Close", command=win.destroy)
        close_file_select.grid(row=0, column=10)


if __name__ == "__main__":
   app = GUI()
   app.mainloop()
