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
def init_connection(returnDict):
    if returnDict:
        return psycopg2.connect(DATABASE_URL, sslmode='require', cursor_factory=RealDictCursor)
    else:
        return psycopg2.connect(DATABASE_URL, sslmode='require'
                                )
#@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

if "DATABASE-TABLE" in os.environ:
    DATABASE_TABLE = os.environ['DATABASE_TABLE']
else:
    DATABASE_TABLE = "petfinder_clean"
conn = init_connection(False)

# First get the list of breeds to be used for user interactions
list_breeds_query = """
    SELECT DISTINCT(breed_primary) FROM "%s" ORDER BY breed_primary ASC;
    """ % (DATABASE_TABLE)
st.markdown(list_breeds_query)
breeds_results = run_query(list_breeds_query)

breeds_array = []
breeds_array_default = []
for breed in breeds_results:
    breeds_array.append(breed[0])
total_num_breeds = len(breeds_array)
#i = 0
#while i < len(breeds_results):
#    breeds_array.append(breeds_results[i][0])
#    i+=1

#    if i > number_of_breeds_slider:
#        break

breeds_list = st.sidebar.multiselect(
    'Choose the breeds you want to see',
    breeds_array, []
)

conn = init_connection(True)

# Set up where clause for only the breeds the user has selected, if they selected any
num_iterations = 0
where_clause = ''
if len(breeds_list) > 0 and len(breeds_list) < len(breeds_array):
    where_clause = " WHERE breed_primary IN ("
    for breed in breeds_list:
        if num_iterations > 0:
            where_clause += ","
        where_clause += "'%s'" % breed
        num_iterations += 1
    where_clause += ") "


los_sort = "ORDER BY AVG(los) %s" % los_sort_selectbox if los_sort_selectbox != 'NONE' else ''
los_by_breed_query = """
    SELECT breed_primary,AVG(los)::bigint as "Length of Stay (Avg)" FROM "%s" %s GROUP BY breed_primary %s LIMIT %s;
    """ % (DATABASE_TABLE, where_clause, los_sort, number_of_breeds_slider)

st.markdown("#### Query")
st.markdown(los_by_breed_query)
breeds_los_results = run_query(los_by_breed_query)

df = pd.DataFrame().from_dict(breeds_los_results)
df.set_index("breed_primary", inplace=True)
st.bar_chart(df)