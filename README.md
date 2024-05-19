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

### Missing Required Functionality
1. HTML render of questions
2. Capturing of diagrams for questions
3. Hyper/Sub script buttons
4. Save results to JSON and uploading to NYRP project
5. Popup with which questions could not be generated

### Non Required Improvements
1. When regenerating questions, keep the files/topics from the old questions
2. Set up keywords for units for autodetection of unit
3. Add a list to the question of probable errors, even if it parsed correctly. Display these when question is shown. Things like
   1. Unicode in the question/answer
   2. Misspelled words (probably missing a space somewhere)
   3. Mentions a figure/diagram/graph and none set for the question
   4. Suspected required super/sub scripts (element symbol preceded/followed by a number)
4. Project save file for quick resume where it was left off
5. Undo/Redo operations when editing exam text
6. Add scroll bar and 'find' to the exam

### Other
1. Replace 'Working All Day'
2. Increase font size in question render
3. Jump focus in exam text box and highlight where the question is from
4. Auto close window to select exams on successful generation, auto trigger Exam creation when text is populated
5. Drop E, subject, year, month from question render
