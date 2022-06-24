import streamlit as st
import pandas as pd
import numpy as np
import time
import math
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

st.markdown("# Dynamic Petfinder Database Data")

number_of_breeds_slider = st.sidebar.slider(
    'How many breeds would you like to see?',
    1, 100, (20)
)

los_sort_selectbox = st.sidebar.selectbox(
    'Sort By Length of Stay',
    ('DESC', 'ASC', 'NONE')
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

los_sort = "ORDER BY AVG(los) %s" % los_sort_selectbox if los_sort_selectbox != 'NONE' else ''

los_by_breed_query = """
    SELECT breed_primary,AVG(los)::bigint as "Length of Stay (Avg)" FROM "%s" GROUP BY breed_primary %s LIMIT %s;
    """ % (DATABASE_TABLE, los_sort, number_of_breeds_slider)
st.markdown("#### Query")
st.markdown(los_by_breed_query)
results = run_query(los_by_breed_query)

#results = pd.DataFrame(results)

dogs_dict = {}
count = 0

# Convert SQL results into a dict
for row in results:
    dogs_dict[count] = row
    count = count+1

df = pd.DataFrame().from_dict(dogs_dict, orient="index")
df.set_index("breed_primary", inplace=True)
#df
st.bar_chart(df)

st.markdown("# Static Petfinder JSON Data")

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