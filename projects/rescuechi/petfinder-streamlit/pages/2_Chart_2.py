"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import math

st.markdown("# Chart 2️")
st.sidebar.markdown("# Chart 2️")

range_for_chart = st.sidebar.slider(
    'Select a range of values to be generated',
    0, 100
)

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, range_for_chart):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    percent_complete = math.ceil((1/range_for_chart) * (i+1) * 100)
    #percent_complete = i
    status_text.text("%i%% Complete" % percent_complete)
    chart.add_rows(new_rows)
    progress_bar.progress(percent_complete)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
