# Currency Test

## Requirements:
- python 3.7 or newer
- pytest 5.4.2 or newer
- requests 2.23.0 or newer
- responses 0.10.14 or newer
- requests_cache 0.8.1 or newer

## Installation:
Use virtual environment where you can install requiremets by running:
   
```bash

  $ python3.7 -m venv venv
  
  $ source venv/bin/activate

  $ (venv) pip install -r requirements.txt
```
## Then run tests with:
```bash
$ pytest
```
If you would like more detailed output (one test per line), then you may use the verbose option:
```bash
$ pytest --verbose
```
or
```bash
$ pytest --log-cli-level=INFO 
```
