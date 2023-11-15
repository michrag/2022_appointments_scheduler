# RESTful web API for Appointments Scheduling
The assignment has been implemented in Python(3.7), using the [Flask-RESTful framework](https://flask-restful.readthedocs.io/en/latest/index.html) (an extension of the [Flask framework](https://flask.palletsprojects.com/en/2.1.x/)).


## Usage (and Requirements)
The application requires Python 3.7 or newer, so in the following `python` could stand for `python3` (depending on your Python installation(s) configuration).

If you prefer, you can create a virtual environment like:

> `python -m venv venv`

and activate it with:

> `venv\Scripts\activate.bat`

(under Windows, otherwise: `source venv/bin/activate`).

Then install the required packages with:

> `python -m pip install -r requirements.txt`

Now you can run the script with:

> `python web_server.py`

To test the application, open a separate shell, activate the same virtual environment as explained above, and run:

> `python web_server_tester.py`

> Note: the results of some tests will be different depending on if the application has found the database files at startup, or not. See next paragraph for details.

When finished, you can deactivate the virtual environment simply with:

> `deactivate`
>

## Notes on the database implementation
The "persistent" database has been implemented as a couple of `json` files, stored in the `db` folder. When the application starts, it tries to load data from the files: if a file is not found, it is created (empty). During the execution of the application, the files are *not* written (for simplicity and efficiency reasons): they are written only when the application is closed. 