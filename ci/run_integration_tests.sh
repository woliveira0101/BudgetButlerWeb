set -e
cd mysite &&  FLASK_APP=start_as_flask.py flask  &


cd selenium_tests
pytest
cd ..
