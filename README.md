# MindSprint AI Quiz — Streamlit Project

## What is included
- `app.py`: interactive Streamlit quiz app
- `questions.json`: 50-question bank with topics, formats, difficulty, correct answers and explanations
- `requirements.txt`: Python package requirement
- `REPORT_TEMPLATE.md`: report draft to personalise after testing

## Step 1 — Check whether Python is installed
On Windows:
1. Press `Windows` key, type `cmd`, and open Command Prompt.
2. Run: `py --version`
3. If that does not work, run: `python --version`
4. If either prints a version such as `Python 3.12.x`, Python is installed.
5. If neither works, install Python 3 from https://www.python.org/downloads/ . During installation, tick **Add python.exe to PATH** if that option appears.

## Step 2 — Open the project folder
Extract this ZIP file to a folder you can find easily, such as `Documents\MindSprintAIQuiz`.
Open that folder in VS Code, or use Command Prompt and change into that folder.

## Step 3 — Install Streamlit
Run:
```bash
py -m pip install -r requirements.txt
```
If `py` does not work but `python` does, use:
```bash
python -m pip install -r requirements.txt
```

## Step 4 — Run the app
```bash
py -m streamlit run app.py
```
Or:
```bash
python -m streamlit run app.py
```
A browser tab should open. If it does not, copy the local URL printed in Command Prompt (usually `http://localhost:8501`) into Chrome.

## Step 5 — Test before submission
- Start a 10-question quiz.
- Submit a correct and an incorrect answer to verify feedback.
- Finish the quiz and inspect score, percentage, explanations and CSV download.
- Try a topic filter and a difficulty filter.
- Take screenshots of the home page, a question with feedback, and results.

## Notes
- The question bank contains 50 questions and is filtered by topic/difficulty.
- Quiz options are single-select to keep the interaction simple and reliable. Some source formats (such as matching and fill-in-the-blank) are represented as multiple-choice questions, with the original format labelled in the interface.
- The timer reports elapsed time at the end; it is not a countdown timer.
- Results are downloadable as CSV. This starter version does not keep a shared online leaderboard or save scores across separate sessions.


## Updated interactive formats
The updated app uses actual True/False options, a text input for Fill in the Blank, a matching activity, and an optional hint button. Assertion–Reason, scenario and problem-solving items remain selectable MCQs.
