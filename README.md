[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/mohitkh7/Easy-Learning/pulls)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Slack Status](https://img.shields.io/badge/Chat%20on-Slack-orange.svg)](https://join.slack.com/t/easylearninggroup/shared_invite/enQtNDk2ODgwMTYwMjI1LTllN2Q2OWVmODgwMzZlYjc2MjAwM2Y3NmU0NTBjZTYzYWRhZjM0Y2VlNmM3MGFkNzNmOGMwNDQ2ODVmYmRmMjQ)

# Easy-Learning
Easy Learning will be a comprehensive web based interactive tool with a complete list of resources to learn any stuff, skills, subject based on community feedback, further tailored according to your learning ability which will also be filterable and searchable.

## Setup Instruction
* Create a new directory at desired place in your file system
```
mkdir name_of_your_choice
cd name_of_your_choice
```

* Create a virtual environment in recetly created directory and activate it:
```
python3 -m venv env
source env/bin/activate
```

* Clone the repository and enter to the repository:
```
git clone https://github.com/mohitkh7/Easy-Learning.git
cd Easy-Learning
```

* Next, install the dependencies using pip:
```
pip install -r requirements.txt
```

* After this create database in mysql:
```
mysql -u root -p<your_mysql_password>
CREATE DATABASE easylearning CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON easylearning.* TO admin@localhost IDENTIFIED BY 'thepassword';
FLUSH PRIVILEGES;
```
Here `admin` and `thepassword` should be same as USER and PASSWORD defined in database settings in `startlearning/settings.py`.

* Once the database table is created, Migrate your database.
```
python3 manage.py migrate
```

* Then create a superuser account for Django:
```
python manage.py createsuperuser
```

* Finally, you’re ready to start the development server:
```
python manage.py runserver
```
Visit [localhost:8000](http://127.0.0.1:8000/) in your browser to see how it looks.


## Contributing
You can contribute in several ways. If you know how to code or are a designer, you are welcome to contribute using pull requests.

You can also contribute by [opening issues](https://github.com/mohitkh7/Easy-Learning/issues) about defects and things that could be improved or request entirely new features that you think would help others.

Join the [Slack Communication Channel](https://join.slack.com/t/easylearninggroup/shared_invite/enQtNDk2ODgwMTYwMjI1LTllN2Q2OWVmODgwMzZlYjc2MjAwM2Y3NmU0NTBjZTYzYWRhZjM0Y2VlNmM3MGFkNzNmOGMwNDQ2ODVmYmRmMjQ) 
