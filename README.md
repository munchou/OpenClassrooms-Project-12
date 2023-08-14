# ABOUT

**OpenClassrooms - Développeur d'application Python - Projet #12: Develop a secured back-end architecture with Python and SQL**

_Tested with Windows 10 and Python 3.10.2_

_IMPORTANT NOTE: the project's requirements have evolved after I started it. Although it is asked to build a back-end architecture based on command lines, I developed a whole terminal interface that allows the users to do whatever they want without having to have to type any annoying commands.
In a nutshell, I did more than what was asked, which took way too much time._

# Hao2do (Windows)

The following steps are only to setup your machine and start the program.
Before starting the latter, ready yourself a nice coffee, [DOWNLOAD THE DOCUMENTATION](documentation/P12%20-%20Documentation.pdf) and read it.


## Installing PostgreSQL
Beware: the installation of PostgreSQL is mandatory. Please do so before trying to run the program.
A recommended website with step-by-step instructions (also available for macOS and Linux):
https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/
The official website: https://www.postgresql.org/
Go to the Download section and choose the version that suits your OS.
Important: if ou chose to use pgAdmin 4 (like I did) and your program seems to be stuck in a loop right after starting it, download and install a previous version. There seems to be serious issues with the latest versions (as of July 2023), I had to install v7.1 to get it to run.
You can also choose another client rather than pgAdmin.

## Retrieving a copy of the "depository"

- `git clone https://github.com/munchou/OpenClassrooms-Project-12.git`

or download the ZIP file and extract it in a chosen folder.


## Creating and activating the virtual environment
(Python must have been installed)
- `cd OpenClassrooms-Project-12` (or any folder where the project is located)
- `python -m venv ENV` where ENV is the name of the folder where the environment will be created.
- Activation : `env/Scripts/activate`
    

## Installing the needed modules

- `pip install -r requirements.txt`


## Starting the program
Absolutely everything goes through the program. Yes, EVE-RY-THING! Which means unlike most things you’ll find, you do not need to run ANY commands to create your database or connect to it. Some would say it’s strange or not even recommended, and I would disagree. The thing is: ONLY the superuser (the user that was created when PostgreSQL was installed) has the rights to do so. Any other user is NOT supposed to know the username, let alone the password to connect to the databases. So be it through psql or within my program, as long as you got the right IDs, you can do whatever you want.

Still in the command window where you activated your virtual environment, type:
`python –m main`


## Getting to the application
See the [DOCUMENTATION](documentation/P12%20-%20Documentation.pdf)


## Testing process
- ### Unit and integration tests
The test were run using pytest.
You simply need to type `pytest` and let the magic do its deed (to get more details about the tests, you can type `pytest -v -s`).
If the terminal displays any red, it's NOT normal!

IMPORTANT: not EVERYTHING was tested, only the features and important functionalities. The program is based on the MVC architecture, so the VIEWS (inputs and prints) were, for the most part, NOT tested.
The part of the program that controls the setup of the database was also NOT included (but obviously tested).
Therefore, the overall coverage is about 60%, whereas the functionalities's coverage is actually above 85%.


- ### Unit and integration tests coverage
Type `pytest --cov`