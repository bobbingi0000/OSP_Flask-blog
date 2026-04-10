"""Y2K blog development server entry script.

Start the development server by running ``python run.py`` from
the project root. When using Flask CLI (``flask run``), set the
environment variable ``FLASK_APP=run.py`` instead.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
