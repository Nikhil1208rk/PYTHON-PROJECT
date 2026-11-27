**Smart Student Performance Analyzer**
A simple web-based project that helps students get a quick overview of their academic performance and daily study habits.

The user enters their details, subject marks, attendance, study hours, and sleep hours. The application calculates the overall result and displays it on a dashboard with charts, subject-wise details, and suggestions for improvement.

**What the project does**
- Takes the student's name and enrollment number.
- Accepts marks in four subjects: Python, Web Development, DSA, and Calculus.
- Collects attendance percentage, daily study hours, and daily sleep hours.
- Calculates total marks, percentage, strongest subject, and weakest subject.
- Assigns an overall performance category:
  - Excellent: 85% and above
  - Good: 70% to below 85%
  - Average: 50% to below 70%
  - Needs Improvement: below 50%
- Reviews attendance, study time, and sleep time.
- Gives subject-wise recommendations based on marks.
- Shows the results on a dashboard and lets the user download the report.
- 
**Tech use**
  **Technology**                                            **How it is used**
    Python                                 Handles the server request and performs the main calculations
    HTML	                                 Builds the input form and results dashboard
    CSS	                                   Styles the pages, cards, progress bars, and charts
  JavaScript	                             Validates form data, sends the request, and updates the dashboard
    JSON	                                 Transfers student information between the browser and Python server
   Python                                  standard library	Provides the web server, JSON handling, and supporting utilities
