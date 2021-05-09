# FastAPIServer

## Always up
- For better convenience I've deployed the API on Google APP Engine, so it can be accessed anytime
- You can access Swagger UI on the following URL: `https://usersandgroupsgoapi.nw.r.appspot.com/docs`

## Usage
- Usage of the API is documented with fastapi library, which has build in /docs functionality
- You can access the docs on the following URL (after sucessfully running the API on Docker): `http://localhost:8000/docs`

## Used components with versions
- Docker 3.3.3 (64133)
- Python 3.8
- MySQL Community Server (Version: 8.0.24)

## Prerequisites
- Have the latest version of Docker Desktop installed
- For running the test cases you need to have python installed on your machine

## Running the API
1. Download the source code from GitHub and unzip it to a desired location
2. In CMD (Command Line Terminal) move to where you have unzipped the repository on your local machine (to the FastAPIServer-main folder)
3. Run the following command `docker-compose up --build` to build and set up the API in your Docker
4. After sucessfully building and deploying the API on Docker, you can close the Terminal and run the API directly from Docker

## Test cases
- All test cases are included in `FastAPIServer-main/tests/testCases.py`
- You can run the tests by simply typing `pytest tests\testsCases.py` from your Terminal in the folder that you've unzipped the source code (FastAPIServer-main)
- There are four test cases in total (for each method one)
- The API needs to be running in order to run the test cases

## Improvements
- Move some functions in other packages for better code readability
- Write more in depth test cases
- Better responses for POST, PUT and DELETE methods (response in the same format as for GET)
- Dynamic Query-ing (ability to Query the DB with URL parameters instead of using IDs)
- Dynamic Update/Insert/Delete (ability to Update/Insert/Delete multiple records at once and not deleting them by ID)
