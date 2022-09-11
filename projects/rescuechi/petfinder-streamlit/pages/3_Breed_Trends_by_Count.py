import streamlit as st
import pandas as pd
import numpy as np
import time
import math
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pfglobals

st.markdown("# Chicago Rescue Dog Trends")
st.markdown("## Breed Trends from Petfinder Data")
st.markdown("### How does dog breed relate to the number of dogs waiting to be adopted?")
st.markdown("Use the filter widget in the sidebar to select specific breeds to visualize, or to select a specific "
            "number of random breeds to see visualized at one time.")


#######################################################
# Sidebar inputs for users to customize their results #
#######################################################
st.sidebar.markdown("## Page-Level Chart Settings")

if "selected_breeds" not in st.session_state:
    st.session_state['selected_breeds'] = []

number_of_breeds_slider = pfglobals.place_breeds_in_sidepanel()
pfglobals.place_los_sort_in_sidepanel(number_of_breeds_slider)

# st.write(st.session_state)

#los_sort_selectbox = st.sidebar.selectbox(
#    'Sort by number of results',
#   ('DESC', 'ASC', 'NONE')
#)

#######################################################
#               End sidebar inputs                    #
#######################################################

# Set up where clause for only the breeds the user has selected, if they selected any
num_iterations = 0
where_clause = ''
if len(pfglobals.breeds_list) > 0 and len(pfglobals.breeds_list) < len(pfglobals.breeds_array):
    where_clause = " WHERE breed_primary IN ("
    for breed in pfglobals.breeds_list:
        if num_iterations > 0:
            where_clause += ","
        where_clause += "'%s'" % breed
        num_iterations += 1
    where_clause += ") "

los_by_breed_query = """
    SELECT breed_primary,Count(*) as "%s" FROM "%s" %s GROUP BY breed_primary %s %s;
    """ % (pfglobals.COUNT_TEXT, pfglobals.DATABASE_TABLE, where_clause, pfglobals.los_sort, pfglobals.limit_query)

if pfglobals.showQueries:
    st.markdown("#### Query")
    st.markdown(los_by_breed_query)

df = pfglobals.create_data_frame(pfglobals.run_query(los_by_breed_query, pfglobals.conn_dict), "breed_primary")
pfglobals.show_bar_chart(df, pfglobals.COUNT_TEXT, "", False)

#######################################################
#                Side by Side Charts                  #
#######################################################
st.markdown("### How do different dog characteristics (gender, size, coat length, age, etc.) interact with breed to "
            "affect the number of dogs waiting to be adopted?")
st.markdown("Use the filter widget in the sidebar to select specific breeds to visualize, or to select a specific "
            "number of random breeds to see visualized at one time. Then select values for other characteristics from "
            "the drop down lists below to compare on the graphs. These side-by-side graphs illustrate how these "
            "characteristics impact average length of stay for dogs of the selected breeds.")

leftCol, rightCol = st.columns(2)
# limit_query = ""
original_where_clause = where_clause

# create the select boxes for all the comparison attributes
all_select_boxes = [
    pfglobals.create_select_boxes("gender", "Gender", leftCol, rightCol, False),
    pfglobals.create_select_boxes("size", "Size", leftCol, rightCol, False),
    pfglobals.create_select_boxes("coat", "Coat", leftCol, rightCol, False),
    pfglobals.create_select_boxes("age", "Age", leftCol, rightCol, False),
    pfglobals.create_select_boxes("good_with_children", "Good With Children", leftCol, rightCol, True),
    pfglobals.create_select_boxes("good_with_dogs", "Good With Dogs", leftCol, rightCol, True),
    pfglobals.create_select_boxes("good_with_cats", "Good With Cats", leftCol, rightCol, True),
    pfglobals.create_select_boxes("breed_mixed", "Is Mixed Breed?", leftCol, rightCol, True),
    pfglobals.create_select_boxes("attribute_special_needs", "Special Needs?", leftCol, rightCol, True),
    pfglobals.create_select_boxes("attribute_shots_current", "Up To Date On Shots?", leftCol, rightCol, True)
]

# now find all selected values to use to build queries
left_values = []
right_values = []
for select_boxes in all_select_boxes:
    left_values.append({"db_column": select_boxes["db_column"], "db_col_type": select_boxes["db_col_type"], "select_box": select_boxes["left"]})
    right_values.append({"db_column": select_boxes["db_column"], "db_col_type": select_boxes["db_col_type"], "select_box": select_boxes["right"]})

# Create comparison charts
pfglobals.create_comparison_chart(leftCol, left_values, original_where_clause, "breed_primary", False)
pfglobals.create_comparison_chart(rightCol, right_values, original_where_clause, "breed_primary", False)
#######################################################
#             End of Side by Side Charts              #
#######################################################
