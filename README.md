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
1. Set up keywords for units for autodetection of unit
2. Add a list to the question of probable errors, even if it parsed correctly. Display these when question is shown. Things like
   1. Misspelled words (probably missing a space somewhere)
   2. Mentions a figure/diagram/graph and none set for the question
   3. Suspected required super/sub scripts (element symbol preceded/followed by a number)
3. Add 'find' to the exam
4. Jump to question
5. Fix Question formats for ingestion
   1. Subject must be all caps
   2. Saving to output, remove number and unit_text
   3. Set E to "" instead of None
   4. Month needs to be the full version
   5. Year needs to be an int not string
   6. Answer needs to be A, B, C, or D, not numeric
   7. Diagram should be a format of "diagrams/{name}" instead of a full path
   8. Add sub/super scrip shift auto-detect

### Other
1. Replace 'Working All Day'
2. Increase font size in question render
3. Jump focus in exam text box and highlight where the question is from

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

