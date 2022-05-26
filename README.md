## CSC 4530 Project - Milestone 3

## Table of Contents
* [Overview](#overview)
* [Installation Info](#installation-info)
* [Setup](#setup)
* [API Instruction Documents](#api-instruction-documnets)
* [Technical Issues and Fix (milestone 3)](#technical-issues-and-fix-(milestone-3))
* [Technical Issues and Fix (milestone 2)](#technical-issues-and-fix-(milestone-2))
* [Unresolved Issues and Improvements](#unresolved-issues-and-improvements)

## Overview
- Project milestone 2 created database to store user information, raitings, and comments.

Login and registration function added. 

- Project milestone 1 used API's from The Movie Data Base (TMDB) and Wikipedia.

TMDB api: used to fetch movie information

Wikipedia api: used to fetch the wikipedia url searched using tmdb api's title information. 

## APIs Frameworks and Libraries 
Heroku Database (PostgreSQL)

API Used: Wikipedia, The Movie Data Base

Framework: Flask, flask_login, flask_sqlalchemy

Library: OS, Requests, JSON, Random, 
    
    - OS: Provides functions for interacting with operating system 
    
    - Requests: Allow user to send HTTP request 
    
    - JSON: Converts the python dictionary into a JSON string 
    
    - Random: Generate pseudo-random numbers


## Installation Info
VS Code: 
    - Setup Overview Documnethttps://code.visualstudio.com/docs/setup/setup-overview
    - VS Code Python Extension: https://code.visualstudio.com/docs/python/python-tutorial
    - Pylint installation document: https://code.visualstudio.com/docs/python/linting

requests: pip3 install requests (run this command to install requests)

Homebrew:  
    - heombrew can be installed using: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" 
    - Homebrew Document: https://docs.brew.sh

Heroku: 
    - brew tap heroku/brew && brew install heroku
    - Heroku Install Instruction: https://devcenter.heroku.com/articles/heroku-cli

PostgreSQL:
    - brew install postgresql
    - brew services start postgresql
    - pip3 install psycopg2-binary
    - pip3 install Flask-SQLAlchemy==2.1

Flask_login: 
    -pip3 install flask-login
    - https://flask-login.readthedocs.io/en/latest/ (flask login information)

React Install:
brew update
brew install node
npx create-react-app [name of the directory] //without [ ]

## Setup
Authentication:
For the users forking the program will require to have .gitignore and .env file.
.gitignore can be specified to ignore .env file. 
.env file contains the api-key (api-key can be obtained through tmdb website) and the database_url (export DATABASE_URL = <"database_url">).

After installing PostgreSQL, database can be created in terminal "heroku addons:create heroku-postgresql:hobby-dev -a "name-of-heroku-app""
Database is now setup. 

App.py:
Two tables of database add to app.py to store user information, ratings, and comments. 
login, logout, and registration function added.
user can check their database status through command: 
"heroku pg:psql"
"\d"
"SELECT * FROM {Column name}"

App.py: (milestone1)
Contains the list of movie ids. User can create a list of movie ids.
Movie ID can be found in TMDB website url for a specific movie.
ex. "https://www.themoviedb.org/movie/438631-dune?language=en-US"
    "438631" right before is the movie ID. 
By adding movie ids, when running the program movies in the list will be randomly generated with the information

wikipedia.py:
Generates the URL using the title fetched from tmdb.py
Nothing needs to be done in this file, as long as the movie information is shown on the page, 
program will take care of generating the url. 

If user wants to add extra features using wikipedia api, 
user can check the instruction documents and API sandbox provided in the mediawiki. 

React JS:
- Main page contains the link to react page which users can edit ratings or delete comments. 
- When react page is called backend will pass the information containing currently logged in user's comments, ratings which can be deleted or edit the rating. Once changes are made save needs to be clicked before seeing the effect take place. 

## API Instruction Documents
The Movie Data Base: 
Get Movie Details: https://developers.themoviedb.org/3/movies/get-movie-details 
Images: https://developers.themoviedb.org/3/getting-started/images

Wikipedia (MediaWiki):
Main Page: https://www.mediawiki.org/wiki/API:Main_page
API Sandbox: https://www.mediawiki.org/wiki/Special:ApiSandbox

## Technical Issues and Fix (Milestone 3)
1. Passing JSON between python and react
fetch was used in react from the route in app.py to get database information in JSON format. 
When fetch was used by itself, the client continuously fetched the datas repeatly. 
wrapping up fetch with useEffect resolved solution.

2. Change ratings
created a functon that takes event and index.
Input with number type is added event that is changed are passed to rating list with the corresponding index. 
Min and max values of the rating is set from 0 to 10
Changes made in the react page overwrites the previous ratings.  

3. Review Editing
created two buttons that can delete and save the changes. 
delete button calling function delete which takes the values of what user choose gets taken out of the list, however it only changes the state in react rather than save them in the database. 
Save button and the function save button is calling submit the changes made in react pages to database. 
When save is clicked from the react page, it calls the current saved data in JSON delete the previous record, and update the data called with the changes made. 

## Technical Issues and Fix (Milestone 2)
1. Database control: 
In the beginning of the project-milestone2, only 1 table of database created to store all the information including login and registration. However, within the table when user registers, it would not store the comments and ratings in the same row.
Resolved this issue by creating another database talbe and managed them separated from the movie raitings and comments. 

2. Displaying User ID in comment section: 
Attempted to display user id directly from the database table containing the registered user's information. 

Resolved this issues by tracking the user information When user logs in and store them in the second table of database when user subtmit their comment. 

## Milestone 1 & 2 Comparison
Milestone 1 was created to implement features through TMDB API and displaying the information already stored.
Fetching the information through API and displaying them on a specific page. 

Milestone 2 implemented a database to store and recall the information stored by user and the user information when they sign up.
Storing the information and fetching them at the right place was the main task. 

## Project Overall: 
Throughout the project using React JS might have been the hardest part of learning, passing information from backend to frontend, vice versa. Unfamiliar syntax and managing the routes between app.js and app.py
The most valuable learning experience came from milestone 1. It was the first time creating an app instead of just solving code problems. APIs allowing the communication with one another and access the database. 
