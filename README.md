# Section 2: Database & Python ETL

Provision one database of your choosing (SQL, NoSQL, Graph).  Write a python ETL that ingests the provided data, transforms it in some way, and loads it into the database. This should be reproducible code with documentation. (Terraform / Cloudformation / Ansible, docker-compose etc).

I chose to load the csv data into a PostgreSQL database created in a Docker container, transforming the id column into integers, and making the email and gender columns lowercase.

## Pre-requisites

To run the code, you will need:

1. [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
2. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Procedure

Clone the git repo and run the ETL as shown below.

```bash
git clone https://github.com/albertlok/etl-pipeline.git
cd etl-pipeline
make up
make run-etl # run the ETL process
make warehouse # run Postgres to query the warehouse
make down # spins down the containers
```

## Explanations

Folder structure:
.
├── Makefile                                  # Define aliases for complex commands
├── README.md                                 # This file
├── containers
│   ├── loader
│   │   ├── Dockerfile                        # Docker image definition for Python process
│   │   └── requirements.txt                  # For Python in Docker image
│   └── warehouse
│       └── 1_create_user_table.sql
├── docker-compose.yml                        # Define required containers
├── env                                       # Define environment variables required by containers
├── src
│   └── loader
│       ├── DE Data.csv                       # Data file
│       ├── __pycache__
│       └── load_user_data.py                 # Code to load and transform data into warehouse
└── utils
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-39.pyc
    │   ├── db.cpython-39.pyc
    │   └── sfl_config.cpython-39.pyc
    ├── db.py                                 # Establish connection with warehouse
    └── sfl_config.py                         # Read environment variables from env

Image for python 3.9.5 used in the Dockerfile, with add-ons in requirements.txt:
```
psycopg2==2.9.3
pandas==1.4.3
```

An `info` schema and `userinfo` table were created for the warehouse table (1_create_user_table.sql):
```
CREATE TABLE info.userinfo (
    id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50),
    gender VARCHAR(20),
    ip_address VARCHAR(15)
);
```

load_user_data function uses psycopg2's execute_batch to insert each user's data into the table (load_user_data.py):
```
# Function to get data from CSV and insert each user into warehouse
def load_user_data():
    user_data = get_user_data()
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        p.execute_batch(curr, _get_user_data_insert_query(), user_data)
```

To get user data from the csv file and transform it (load_user_data.py):
```
# Read data from CSV, transform some columns, and return as list
def get_user_data(filename='DE Data.csv'):
    data_df = pd.read_csv('./' + filename)      # Can replace file path with desired path on local system
    data_df['id'] = data_df['id'].apply(int)    # Cast id column into integers
    data_df['first_name'] = data_df['first_name'].str.capitalize()  # Names already appear to be capitalized, but just to be sure
    data_df['last_name'] = data_df['last_name'].str.capitalize()    # Names already appear to be capitalized, but just to be sure
    data_df['email'] = data_df['email'].str.lower()     # Lowercase emails for easier potential parsing
    data_df['gender'] = data_df['gender'].str.lower()   # Lowercase gender for easier potential parsing
    return data_df.values.tolist()
```

Some queries to validate once the warehouse has been created and populated with data:
`SELECT COUNT(*) FROM info.userinfo; --1000 entries`
`SELECT * FROM info.userinfo ORDER BY last_name LIMIT 10;`
'\q'

Remember to `make down` after using!
