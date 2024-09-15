## Background
Many websites that host regents questions are terribly formatted and ugly. 
This project is a subsidiary of NYRP that aids in faster generation of nicely
foramted questions.

## Purpose
Three main goals
1) Download from the New York regents exam website past test
2) Convert those exams and answers to semi-formatted text files
3) A UI that assists the user in turning text into real, formatted questions
4) Turning those questions into JSON blobs and stored media to allow bulk
ingestion into the NYRP website.

Python version: 3.9

##TODOs


### Non Required Improvements
1. Add a list to the question of probable errors, even if it parsed correctly. Display these when question is shown. Things like
   1. Misspelled words (probably missing a space somewhere)
   2. Suspected required super/sub scripts (element symbol preceded/followed by a number)
2. Add 'find' to the exam
3. Jump to question
4. Fix Question formats for ingestion
5. Revised way to do hints that includes plurals and punctuation but not partial words. Maybe switch to regex
6. Chem exam improvements
   1. replace "â†’" with "->"
   2. " 1 " replace with " + "
   3. Detect subscripts within lines, letter followed by 1 or more numbers then space or paren
7. Fix exam reading so functions aren't read as answers. ie '(1) f(2) = 3' is supposed to mean answer #1 is 'f(2) = 3', but it gets parsed as the answer to #1 is f, and the answer to #2 is '=3'
8. So many TODO items that should be addressed.

### Other
1. Replace 'Working All Day'
2. Jump focus in exam text box and highlight where the question is from

### tk_html_widgets
I forked a dependency I was using and made updates to it to render 
super and sub scripts. The orginal is here: https://github.com/paolo-gurisatti/tk_html_widgets
my version is here https://github.com/WalterSchaertl/tk_html_widgets, and if
you want to run this locally and can't live without seeing the super and
sub scripts working (like me), pull my version, build it, install it.
1. In the tk_html_widgets
   1. Create a pyproject.toml (see commit message in that project)
   2. python -m build
2. In the NYRPQuestions project
   1. python -m pip install path_to_tk_html_widgets\tk_html_widgets-0.4.1-py3-none-any.whl --force-reinstall

