import streamlit as st
import pandas as pd
import numpy as np
import time
import math
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

st.markdown("# Petfinder️")
st.sidebar.markdown("# Petfinder️")

data_to_show = st.sidebar.selectbox(
    'Data to view',
    ('age', 'gender')
)

DATABASE_URL = os.environ['DATABASE_URL']

#@st.experimental_singleton
def init_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require', cursor_factory=RealDictCursor)

#@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

if "DATABASE-TABLE" in os.environ:
    DATABASE_TABLE = os.environ['DATABASE_TABLE']
else:
    DATABASE_TABLE = "petfinder_clean"
conn = init_connection()

query = """
    SELECT %s FROM "%s" GROUP BY %s;
    """ % (data_to_show, DATABASE_TABLE, data_to_show)
st.markdown("#### Query")
st.markdown(query)
results = pd.DataFrame(run_query(query))
results
#for row in rows:
    #st.write(f"{row['age']} has a :{row['species']}:")

st.bar_chart(results)

# Opening JSON file
f = open('projects/rescuechi/petfinder-streamlit/example-petfinder-dog-response.json')

# returns JSON object as a dictionary
json_data = json.load(f)

st.markdown("*NOTE: Raw JSON data can be found at the bottom of the page*")

all_breeds = [] # there's probably a better way to do this, but keep track of which breeds we've already seen, and increment them in that case
breed_count = {'Breed Count': {}}

# Iterating through the petfinder json
for i in json_data['animals']:
    this_breed = i['breeds']['primary']
    if this_breed in all_breeds:
        breed_count['Breed Count'][this_breed] = breed_count['Breed Count'][this_breed] + 1
    else:
        all_breeds.append(this_breed)
        breed_count['Breed Count'][this_breed] = 1

# Close file
f.close()

st.markdown("### List of Breeds")
st.markdown(all_breeds)
st.markdown("### List of Breeds With Counts")
st.markdown(breed_count)
st.markdown("### Chart of Breeds and Counts")
breed_chart = pd.DataFrame(breed_count)
breed_chart
st.bar_chart(breed_chart)

st.markdown("### Raw JSON Data")
st.markdown(json_data)