# Raw Data Transformation

In this task we need you to convert an algorithm written by a data scientist into
a proper engineered python code.

## Data description
- The file `dataengr_interview.ipynb` contains the actual logic of transforming raw data for
one of our golfers from their Arccos account into a normalised Clippd account
- The `round.json`, `terrain.json` and `2020-12-03T12_20_14.080Z.json` files contain sample data
for a round of golf played in a particular day.
- PGA benchmarks and Data Dictionary are common data schemas and mapping that
we is provided for interview purposes only.

## Task
Convert the jupyter notebook into modular code that could be evaluated for one or more
rounds of golf data from Arccos.

## What is evaluated
- Code logic/functionality
- Organisation of the code (python modules)
- Reduction of complexity (removal of inline functions and testable)
- Performance considerations
- Data processing/cleaning in efficient manner
- Handle failure conditions (unavailability of files / data) in graceful manner
- Proper linting and formatting (using the attached precommit configuration)
- Full Unit Testing with coverage (unittests or pytest)
- Documentation (mainly docstrings)
