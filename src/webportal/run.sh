redis-server &
sleep 1
celery -A "webportal" worker --loglevel=INFO &
sleep 1
python3 webportal.py
