export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=app.py
source venv/bin/activate
nohup flask run --host=0.0.0.0 --port=1489
