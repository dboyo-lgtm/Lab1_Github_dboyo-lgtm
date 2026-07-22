                         README.md file on Grade-evaluator and Archiver organizer

This python program computes a student academic result from a CSV of course grades using the ALU format.
It also uses a bash script that archives the the grade file and logs each time the script is run.

The folder or directory Lab1_Github_dboyo-lgtm contents three files. Which are grade-evaluator.py, organizer.sh
and you will need python 3.6 or newer version, bash systems such as Linux, WSl repectively to be able to run 
the python program and bash script. Last file in this folder is the README.md file.

The grades.csv file is also found in this directory and contains the required input for the program to run.

assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20

From the input above each word from the first column is a header name for a column and the words under the in the
next lines are their values.

How to run the program
After cloning my githhub repository using git clone.
On your local terminal type python3 grade-evaluator.p. Your output will display an academic report.

The program has the following functions when it runs:

1) Grade Validation: Check that the score for every assignment respects the assignment
grade range (between 0 and 100).

2) Weight Validation: Verify that the sum of all assignment weights equals exactly 100.
Ensure all "Summative" assignments add up to exactly 40, and all "Formative"
assignments add up to exactly 60.

3) GPA Calculation: Calculate the final GPA based on the weighted scores. Use the formula:
GPA = (Total Grade / 100) * 5.0.

4) Final Decision (Pass/Fail): A student passes only if they score at or above 50% in both
categories. And finally  prints the final status of the student (PASSED or FAILED).

5) Resubmission Logic: Resubmission is for failed formative assignment that carries the
highest weight. If multiple failed formative assignments share the same highest weight (score below 50)
the program must display all of them as eligible for resubmission.

Next step is the run the organizer.sh script.
first type chmod +x organizer.sh to get permission to be able to run the file.
Then type ./organizer.sh or bash organizer.sh to run the script. 

This script has the followiing function when it runs:

1) Create an archive/ directory if one does not already exist.

2) Generate a timestamp in YYYYMMDD-HHMMSS form.

3) Move grades.csv into archive/ renamed as grades_<timestamp>.csv.

4) Create a fresh, empty grades.csv in the working directory.

5) Append a line to organizer.log recording the timestamp, the original filename, and the archived filename.

The final flow is to execute is:
- Clone the github repository using the link provided by typing git clone the link.git
- python3 grade-evaluator 
- chmod +x organizer.sh
- ./organizer.sh or bash organizer.sh 
