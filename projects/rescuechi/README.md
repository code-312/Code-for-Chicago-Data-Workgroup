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

1. Clone this repository.
2. `cd` into the root directory of this project.

To run any of these scripts, you'll need to install the requirements:

```bash
pip install -r projects/rescuechi/petfinder/requirements.txt
```

### Data Getter

To use the functions in this script, you'll need to set up your PetFinder API key
and secret as environment variables.

First, request an API and secret, and put these somewhere safe. You can request an API
key [here](https://www.petfinder.com/developers/).

Next, export your key and secret to your enviornment. For example, you could run:

```bash
export PETFINDER_KEY=<your-api-key>
export PETFINDER_SECRET=<your-api-secret>
```

Now, you're ready to run the script. To pull down the first 100K results for dogs in and
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

This script syncs data to Heroku, and in order to do so, requires you to set up the
database uri as an environment variable. There are two ways to do so, either by copying
the uri manually from the Heroku UI, or through the Heroku CLI.

### Option 1: Manual

To copy the uri manually, you will first need to be part of the team's Heroku account.
Then, navigate to https://data.heroku.com/ and select the datastore called
`postgresql-corrugated-21223`. Click on `settings`, then `View Credentials...`, and look for a variable called `URI`.

From the command line, run the following, replacing the value of `<paste-uri-here>`
with the value you see on Heroku's UI. It should start with `postgres://`:

```bash
export DATABASE_URL=<paste-uri-here>
```

You can test that this worked by running

```bash
echo $DATABASE_URL
```

and checking that it prints back your uri.

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
