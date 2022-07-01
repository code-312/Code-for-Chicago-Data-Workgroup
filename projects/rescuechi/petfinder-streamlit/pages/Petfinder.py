import streamlit as st
import pandas as pd
import numpy as np
import time
import math
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

showQueries = True

st.markdown("# Dynamic Petfinder Database Data")

DATABASE_URL = os.environ['HEROKU_POSTGRESQL_AMBER_URL']
WHERE_START = " WHERE "
AND_START = " AND "

# @st.experimental_singleton
def init_connection(returnDict):
    if returnDict:
        return psycopg2.connect(DATABASE_URL, sslmode='require', cursor_factory=RealDictCursor)
    else:
        return psycopg2.connect(DATABASE_URL, sslmode='require'
                                )


# @st.experimental_memo(ttl=600)
def run_query(query, conn):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def create_data_frame(breeds_los_results):
    df = pd.DataFrame().from_dict(breeds_los_results)
    df.set_index("breed_primary", inplace=True)
    return df


def create_array_of_db_values(db_column):
    # First get the list of values to be used for user interactions
    list_values_query = """
        SELECT DISTINCT(%s) FROM "%s" ORDER BY %s ASC;
        """ % (db_column, DATABASE_TABLE, db_column)
    #st.markdown(list_values_query)
    results = run_query(list_values_query, conn_no_dict)

    values_array = []
    for value in results:
        values_array.append(value[0])

    return values_array

# Create select boxes for the left and right side of charts
def create_select_boxes(db_column, text, col1, col2):
    values = create_array_of_db_values(db_column)
    values.insert(0, "")

    with col1:
        select_box_left = st.selectbox(
            text,
            values,
            key=db_column + "_left"
        )

    with col2:
        select_box_right = st.selectbox(
            text,
            values,
            key=db_column + "_right"
        )
    return {"db_column": db_column, "left": select_box_left, "right": select_box_right}


def create_comparison_chart(column, values, og_where_clause):
    if not og_where_clause:
        comparison_where_clause = WHERE_START
    else:
        comparison_where_clause = og_where_clause + " AND "

    i = 0
    while i < len(values):
        if i > 0 and values[i]["select_box"] and (comparison_where_clause != WHERE_START) and not (comparison_where_clause.endswith(AND_START)):
            comparison_where_clause += " AND "
        if values[i]["select_box"]:
            comparison_where_clause += values[i]["db_column"] + "='" + values[i][
                "select_box"] + "'"  # need to get the attribute key in here (add to object above)
        i += 1

    # this means our where clause is empty, so clear it out
    if comparison_where_clause == WHERE_START:
        comparison_where_clause = ""

    # this means we have breeds set but nothing else, so set back to the breeds where query
    if comparison_where_clause.endswith(AND_START):
        comparison_where_clause = og_where_clause

    comparison_los_by_breed_query = """
        SELECT breed_primary,AVG(los)::bigint as "LOS" FROM "%s" %s GROUP BY breed_primary %s %s;
        """ % (DATABASE_TABLE, comparison_where_clause, los_sort, limit_query)

    with column:
        if showQueries:
            st.markdown("#### Query")
            st.markdown(comparison_los_by_breed_query)
        st.bar_chart(create_data_frame(run_query(comparison_los_by_breed_query, conn_dict)))

if "DATABASE_TABLE" in os.environ:
    DATABASE_TABLE = os.environ['DATABASE_TABLE']
else:
    DATABASE_TABLE = "petfinder_with_dates"
conn_no_dict = init_connection(False)
conn_dict = init_connection(True)

# First get the list of breeds to be used for user interactions
list_breeds_query = """
    SELECT DISTINCT(breed_primary) FROM "%s" ORDER BY breed_primary ASC;
    """ % (DATABASE_TABLE)
st.markdown(list_breeds_query)
breeds_results = run_query(list_breeds_query, conn_no_dict)

breeds_array = []
breeds_array_default = []
for breed in breeds_results:
    breeds_array.append(breed[0])
total_num_breeds = len(breeds_array)
# i = 0
# while i < len(breeds_results):
#    breeds_array.append(breeds_results[i][0])
#    i+=1

#    if i > number_of_breeds_slider:
#        break

#######################################################
# Sidebar inputs for users to customize their results #
#######################################################
if "selected_breeds" not in st.session_state:
    st.session_state['selected_breeds'] = []

# st.write(st.session_state)

breeds_list = st.sidebar.multiselect(
    'Choose the breeds you want to see (will ignore the number of breeds set below if this field is set)',
    breeds_array, st.session_state.selected_breeds, key="selected_breeds"
)

if len(breeds_list) <= 0:
    number_of_breeds_slider = st.sidebar.slider(
        'How many breeds would you like to see?',
        1, 100, (20)
    )
else:
    number_of_breeds_slider = 0

los_sort_selectbox = st.sidebar.selectbox(
    'Sort By Length of Stay',
    ('DESC', 'ASC', 'NONE')
)
#######################################################
#               End sidebar inputs                    #
#######################################################

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
limit_query = ""
if number_of_breeds_slider > 0:
    limit_query = "LIMIT %s" % number_of_breeds_slider
los_by_breed_query = """
    SELECT breed_primary,AVG(los)::bigint as "Length of Stay (Avg)" FROM "%s" %s GROUP BY breed_primary %s %s;
    """ % (DATABASE_TABLE, where_clause, los_sort, limit_query)

if showQueries:
    st.markdown("#### Query")
    st.markdown(los_by_breed_query)

st.bar_chart(create_data_frame(run_query(los_by_breed_query, conn_dict)))

#######################################################
#                Side by Side Charts                  #
#######################################################
leftCol, rightCol = st.columns(2)
# limit_query = ""
original_where_clause = where_clause

# create the select boxes for all the comparison attributes
all_select_boxes = [
    create_select_boxes("gender", "Gender", leftCol, rightCol),
    create_select_boxes("size", "Size", leftCol, rightCol),
    create_select_boxes("coat", "Coat", leftCol, rightCol)
]

# now find all selected values to use to build queries
left_values = []
right_values = []
for select_boxes in all_select_boxes:
    left_values.append({"db_column": select_boxes["db_column"], "select_box": select_boxes["left"]})
    right_values.append({"db_column": select_boxes["db_column"], "select_box": select_boxes["right"]})

# Create comparison charts
create_comparison_chart(leftCol, left_values, original_where_clause)
create_comparison_chart(rightCol, right_values, original_where_clause)