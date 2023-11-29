import sys
from os.path import abspath, dirname

# Add the project's root directory to the Python path
sys.path.insert(0, abspath(dirname(__file__)))

from app.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
