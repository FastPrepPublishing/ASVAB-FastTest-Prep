# ASVAB Master Trainer

A complete ASVAB preparation web app that supports:

- Section-based practice (over 770 real questions)
- Full-length simulations (2 full ASVAB tests)
- Session memory (pause, resume, score tracking)

## Getting Started

1. Clone the repo
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python app.py
   ```

Then open your browser at `http://localhost:5000`.

## File Structure

- `app.py`: Flask backend
- `questions_practice_full.json`: Practice questions
- `questions_simulations_full.json`: Simulations
- `asvab_session_manager.py`: Session memory
- `templates/index.html`: Web interface

Deployable to Heroku, Render, or any Flask-compatible platform.