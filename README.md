# BiblioTech
BiblioTech is a book discovery web app where users can search books, explore authors and genres, and view summaries, covers, and key info. Users can save favourites, build reading lists, and track books they want to read or purchase, all powered by the Google Books API.

Project docs live in [Docs/Planning.md](Docs/Planning.md). The repo root is the `BiblioTech` folder, which also contains the local virtual environment and Python dependency file.

## Setup
1. Open a terminal in the `BiblioTech` folder.
2. Activate the virtual environment:
	- PowerShell: `..\.venv\Scripts\Activate.ps1`
	- Command Prompt: `..\.venv\Scripts\activate.bat`
3. Install dependencies:
	- `pip install -r requirements.txt`

## Run
The Flask app entrypoint is `app.py`.

- Local development: `python app.py`
- Render / Gunicorn: `gunicorn app:app`
