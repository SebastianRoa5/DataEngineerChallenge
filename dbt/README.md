For installing dbt core locally you must have python and then set up an environment
Create your virtual environment (for this setup we are using python 3.9):
python3.9 -m venv env 

Activate your virtual environment:
source env/bin/activate

Verify Python Path:
which python

Run Python:
env/bin/python

then in the environment, run pip install requriements to install packages and the adapter for the posgtgres database

then run dbt init, to initialize the files required by dbt



