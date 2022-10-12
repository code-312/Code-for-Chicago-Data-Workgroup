<h1 align="center">Rescue Chicago</h1>
<h4 align="center">PetFinder Dashboard for Rescue Dogs</h4>

<div align="center"><img src="https://user-images.githubusercontent.com/89172742/193910009-1faf3fe1-d991-4ccf-afde-fa4d448f27aa.png" width="552" height="278" /></div>

<h5 align="center">  By:  <a href="https://github.com/kaylarobinson077">Kayla Robinson</a>, <a href="https://github.com/TheeChris">Chris Lynch</a>, <a href="https://github.com/ecooperman">Evan Cooperman</a>, Joseph Adorno, Cara Karter - <a href="https://codeforchicago-rescuechi.herokuapp.com/"><i>Live site</i></h5>

### Table of Contents
- [Main purpose](#main)
- [How to use this application](#how-to-use-this-application)
- [What's next?](#whats-next)
- [Conclusion and Contributions](#conclusion-and-contributions)

## Main

In 2021 alone, Chicago Animal Care and Control, the city’s only publicly funded shelter, took in 4,122 stray, surrendered, or confiscated dogs. While some of the dogs who end up in the municipal shelter will be returned to their owner or adopted out directly, more than half of these animals are transferred to another animal rescue organization through the shelter’s Homeward Bound partnerships.

To learn more about the journeys of these rescued pups, we pulled data from the Petfinder API for dogs located within 100 miles of Chicago. Petfinder is the most widely used online database of adoptable pets. Many Chicago animal rescue organizations maintain their own organization pages and adoptable pet listings on the site. We are building an interactive data visualization dashboard to explore how different dog characteristics affect the average length of stay of these Chicagoland dogs in a shelter or foster placement prior to adoption.

- We heard from Chicago animal rescue volunteers that if they knew why dogs weren't leaving the Chicago municipal shelter quickly then they could share that information with press/media to encourage volunteering and adopting.

- To answer this question, and ultimately work toward getting more animals out of shelters into forever homes, we pulled data from the Petfinder API for dogs within 100 miles of Chicago.

- We then created a first iteration of a publicly-available, interactive data dashboard that can be used to analyze how different dog characteristics may correlate with average length of stay in a shelter prior to adoption.

#### Key Features
- Breed Trends by Length of Stay
- Other Trends by Length of Stay
- Breed Trends by Count
- Other Trends by Count

#### Technology used

![alt text](https://github.com/Workshape/tech-icons/blob/master/icons/git.svg)
![alt text](https://github.com/Workshape/tech-icons/blob/master/icons/heroku.svg)
![alt text](https://github.com/Workshape/tech-icons/blob/master/icons/postgres.svg)
![alt text](https://github.com/Workshape/tech-icons/blob/master/icons/python.svg)

<h4>Data Scraping and Cleaning</h4> <sub>- Python (requests, pandas)</sub>

<h4>Database</h4> <sub>- Python (sqlalchemy, pandas), SQL, PostgreSQL, Heroku</sub>

<h4>Visualization and App</h4> <sub>- Python (streamlit, pandas, matplotlib), SQL, Heroku</sub>

## How to use this application

1. Clone the repository with Git:

```bash
https://github.com/Code-For-Chicago/Code-for-Chicago-Data-Workgroup.git
```
2. Create a file called `.env` in the root directory. This file is ignored via the .gitignore file to avoid committing secrets.

3. Open `.env` in a text editor and add this as the contents, replacing the second part with your personal API keys. There is also a .env.example to follow for more help.

4. You can request a Petfinder API
key and secret [here](https://www.petfinder.com/developers/).
```
PETFINDER_KEY=REPLACE_ME_WITH_PETFINDER_KEY
PETFINDER_SECRET=REPLACE_ME_WITH_PETFINDER_SECRET
DATABASE_URL=postgresql://username_goes_here:password_goes_here@localhost/app_name_here
PETFINDER_STREAMLIT_SHOW_QUERIES=False
PETFINDER_STREAMLIT_CHART_TYPE=advanced
HEROKU_POSTGRESQL_AMBER_URL=REPLACE_ME_WITH_HEROKU_URI
```
- Set PETFINDER_STREAMLIT_SHOW_QUERIES to False or True if you want to see queries shown on the frontend. False is the default.
- Set PETFINDER_STREAMLIT_CHART_TYPE to simple, advanced or all, depending which type of chart you would like to see. advanced is the default.
- Scroll down to [Option 1: Manual](#option-1-manual) on how to setup HEROKU_POSTGRESQL_AMBER_URL
- ** **OPTIONAL** ** - Scroll down to [Local PostgreSQL Setup](#local-postgresql-setup) on how to setup a local psql database.

Now install required modules in requirements.txt:

```bash
pip install -r requirements.txt
```

To start Streamlit locally:
```bash
streamlit run projects/rescuechi/petfinder-streamlit/Home.py
```
Open the Network URL it gives you in your browser.

### Data Getter

To pull down the first 100K results for dogs in and
around Chicago, you can run:

```python
python data_getter.py
```

This will create a file called `chicago_animals.pkl` in the `rescuechi/petfinder/data`
folder.

### Data Cleaner

This script reads and saves files locally, so no extra set-up beyond installing the
python requirements is needed.

The script can be run by calling:

```python
python data_cleaner.py
```

This will create a file called `chicago_animals_clean.pkl` in the
`rescuechi/petfinder/data` folder.


### Data Putter

This script syncs data to Heroku's PostgreSQL database. If you want the script to sync data locally, set the uri variable to DATABASE_URL.

```python
python data_putter.py
```

### Option 1: Manual

To copy the uri manually, you will first need to be part of the team's Heroku account.
Then, navigate to https://data.heroku.com/ and select the datastore called
`postgresql-corrugated-21223`. Click on `settings`, then `View Credentials...`, and look for a variable called `URI`.

### Option 2: CLI

To use the Heroku CLI to get the database URI, first you will need to install the Heroku
CLI by following the instructions [here](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli).

After this is installed and configured, you can run the following command:

```bash
export DATABASE_URL=$(heroku config:get HEROKU_POSTGRESQL_AMBER_URL --app  codeforchicago-rescuechi)
```

You can test that this worked by running

```bash
echo $DATABASE_URL
```

and checking that it prints back your uri.

### Local PostgreSQL Setup
If you have PostgreSQL installed locally, in the terminal type psql and enter the commands:

```bash
CREATE USER username WITH PASSWORD 'password' CREATEDB;
```

```bash
CREATE DATABASE app_name WITH OWNER username;
```

Add your updated username, password and database name to your .env file. The DATABASE_URL line in your .env file should look like this with your details instead.
> DATABASE_URL=postgresql://username:password@localhost/app_name

Once that's done you can follow the Data Getter & Setter guide up above. In the Data Putter, you will need to set the uri variable to DATABASE_URL instead of HEROKU_URL. I recommend using [Postbird](https://github.com/Paxa/postbird) or a similar app to view the data.

<sub>* **Note** - While you can see the data locally with postbird, it doesn't work through Streamlit yet.</sub>

## What's next
Expand dataset to other major metro areas in the US to look at differences.
Add other fields from Petfinder to the dashboard including organizations and listing content. Expand to other pets.

## Conclusion and Contributions
<h5>Project made during Women Who Code Hackathon for Social Good 2022.</h5>

### [Rescue Chicago](https://rescuechi.org/)
<img src="https://user-images.githubusercontent.com/89172742/193914404-16b5c6b5-bdf0-46e1-9e52-78c8b3cdd381.png" width="594" height="303" />

### [Code for Chicago](https://codeforchicago.org/)
<img src="https://user-images.githubusercontent.com/89172742/193916463-96b92d44-9696-4207-b82b-bafe52f8ce61.png" width="594" height="303" />


### Contributers -
**Kayla Robinson, Chris Lynch, Evan Cooperman, Joseph Adorno, Cara Karter**
