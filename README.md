# Command to run the server

## prerequisites:
    * conda

## Commands
```
    conda create -n authman python=3.11
    conda activate authman
    pip install -r requirements.txt
    uvicorn main:authman --reload
```
## In case of pyscopg2 error
```
    pip3 install psycopg2-binary
```