while ! nc -z localhost 8000; do
  sleep 0.1 # wait for 1/10 of the second before check again
done
python manage.py recordings_check