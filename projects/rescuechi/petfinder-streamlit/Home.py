import streamlit as st

st.markdown("# Chicago Rescue Dog Trends")
intro_text = "In 2021 alone, Chicago Animal Care and Control, the city’s only publicly funded shelter, took in 4," \
             "122 stray, surrendered, or confiscated dogs. While some of the dogs who end up in the municipal shelter " \
             "will be returned to their owner or adopted out directly, more than half of these animals are " \
             "transferred to another animal rescue organization through the shelter’s Homeward Bound partnerships. To " \
             "learn more about the journeys of these rescued pups, we pulled data from the Petfinder API for dogs " \
             "located within 100 miles of Chicago. Petfinder is the most widely used online database of adoptable " \
             "pets. Many Chicago animal rescue organizations maintain their own organization pages and adoptable pet " \
             "listings on the site. The interactive data visualizations on the Breed Trends page and Other Trends can " \
             "be used to illustrate how different dog characteristics affect the average length of stay of these " \
             "Chicagoland dogs in a shelter or foster placement prior to adoption. "
st.write(intro_text)

st.markdown("## Acknowledgements")
acknowledgements_text = "Project documentation is available on Github. The Petfinder API is easily accessible through " \
                        "the Petfinder for Developers webpage. This project was originally inspired by conversations " \
                        "that the Code for Chicago data workgroup had with Rescue Chicago about how data could inform " \
                        "their efforts to support and unify Chicago’s shelter and rescue community. This application " \
                        "was built by Evan Cooperman, Kayla Robinson, Cara Karter, Joseph Adorno, and E. Chris Lynch. "
st.write(acknowledgements_text)

st.markdown("## Visualization Pages")
st.markdown("* <a href=\"/Breed_Trends\" target=\"_self\">Breed Trends</a>", unsafe_allow_html=True)
st.markdown("* <a href=\"/Other_Trends\" target=\"_self\">Other Trends</a>", unsafe_allow_html=True)
