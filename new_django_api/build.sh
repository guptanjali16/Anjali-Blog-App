#!usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
# If you want to run tests, uncomment the following line
# python manage.py test
echo "Build completed successfully."
# echo "You can now run the server using 'python manage.py runserver'."
#!usr/bin/env bash