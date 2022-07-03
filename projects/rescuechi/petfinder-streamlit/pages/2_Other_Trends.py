import streamlit as st
import pandas as pd

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