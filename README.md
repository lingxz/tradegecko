# tradegecko object state reconstruction

## Running the app locally

This requires Python 3 install on your computer. 

Clone the repository, in the root folder, install required modules with

```
pip install -r requirements.txt
```

To start the app, do 

```python
python run.py
```

Then go to [localhost:5000](localhost:5000) to view the app. 

Note: If running on windows, multiprocessing comment out this line in [app/__init__.py](app/__init__.py)

```python
# initialize singleton pool handler, if using windows, comment this out.
# multiprocessing works poorly on windows because windows sucks
PoolHandler()
```

and uncomment this line in [run.py](run.py)

```python
# PoolHandler()  # uncomment this if using on windows
```

This is because the multiprocessing module has problems on windows.

## Developing

To install libraries needed for developing, do

```
pip install -r requirements.dev.txt
```


To run tests, do

```python
py.test --cov=app tests/
```