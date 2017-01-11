# skanska
skaska

Note: need mysql to be installed in the system for database.
For Windows:https://corlewsolutions.com/articles/article-21-how-to-install-mysql-server-5-6-on-windows-7-development-machine
For Linux: sudo apt-get install mysql-server

1. Clone the repository.
git clone https://github.com/rmishra7/skanska.git
virtualenv ska_venv
2. Linux: source ska_venv/bin/activate
windows: ska_venv\Scripts\activate
3. cd skanska
4. pip install -r requirements.txt
5. python manage.py runserver