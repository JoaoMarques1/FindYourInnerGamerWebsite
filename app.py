import enum
import streamlit as st
import requests
from utils import get_img, get_data_from_gcp
import streamlit as st

#API url
url = 'https://find-your-inner-gamer-7oqykbx6lq-ew.a.run.app/predict'

# configuring page with wide view
st.set_page_config(
    page_title="Find Your Inner Gamer!",
    page_icon="🕹️",
    layout="wide",
)

# setting default value for clik variable to False
clik = False

# Creating three columns and putting title in the middle
st.markdown("<h1 class='title'>🎮 Find Your Inner Gamer 🎮</h1>", unsafe_allow_html=True)
st.header("")


# Creating the about this app
with st.sidebar:
    with st.expander("ℹ️ - About this app", expanded=True):
        st.write(
        """
    🦁 Created with Love in Le Wagon by Luis Queiros, Joao Marques, Laura Bonnet 🦁
	    """
    )
    st.markdown("")
    st.markdown("")


    # Creating the drop down for user to choose the game
    @st.cache
    def get_select_box_data():
        return get_data_from_gcp()
    df = get_select_box_data()

    game = st.selectbox('Select your favourite game', df['name'], help="At present, you can choose between 24 000 games. More to come!")
    params = {
            'game': game
        }
    st.markdown('')

    cs, c1, c2 = st.columns([1, 6, 1])
    with c1:
        if st.button('✨ Find Similar Games'):
            response = requests.get(url, params)
            if response.status_code != 200:
                pred = ''
            else:
                pred = response.json()

            clik = True


# creating font
st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display&family=Press+Start+2P&display=swap" rel="stylesheet">

<style>
p {{
    font-family: 'Playfair Display';
    letter-spacing: .1em;
}}

.stars {{
    font-size: 1.5em;
}}

.desc {{
    line-height: 1.6;
    margin-bottom: 2em;
}}

.image {{
    width: 55em;
}}

.symbols{{
    font-size: 1.2em;
}}

.title{{
    font-size: 4em;
    font-family: 'Press Start 2P';
    text-align: center;
    color: #3895d3;
    text-shadow: 3px 3px white;
}}

a {{
    text-decoration: none;
    font-size: .7em;
    font-family: 'Press Start 2P';
}}

a:hover{{
    text-decoration: none;
    font-size: .9em;
}}


.stApp {{
    background: rgba(0, 0, 0, 0.6) url(https://images.unsplash.com/photo-1498736297812-3a08021f206f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2271&q=80);
    background-size: cover;
    background-position: center;
    background-blend-mode: darken;
}}

</style>
""", unsafe_allow_html=True)


# displaying recommended titles
if clik:
    cols = st.columns([15,1,15])
    i = 0

    reviews_scale = {
        "No reviews": '',
        "Overwhelmingly Negative": '',
        "Very Negative": '',
        "Negative": '',
        "Mostly Negative": '',
        'Mixed': '',
        "Mostly Positive": '',
        "Positive": '',
        "Very Positive": '',
        "Overwhelmingly Positive": ''
    }

    for index, value in enumerate(list(reviews_scale.keys())[1:]):
        filled_stars = round(index / 2)
        empty_stars = 5 - filled_stars

        reviews_scale[value] = ' ★ ' * filled_stars + ' ☆ ' * empty_stars


    for game in pred.get('title', ['', ''])[1:]:

        row = df[df['name']== game]
        url = row['url'].iloc[0]
        tags = row['popular_tags'].iloc[0]
        desc = row['desc_snippet'].iloc[0]
        review = row['reviews'].iloc[0]

        if isinstance(tags, float):
            tags = "No tags"

        tags = tags.replace(',', ', ')

        if review == 'no value':
            review = 'No reviews'

        cols[i].markdown(f"<h1><a href='{url}'>{game}</a></h1><p class='stars'>{reviews_scale[review]}</p>", unsafe_allow_html=True)

        # expan_tags = cols[i].expander("Game Tags")
        # expan_tags.markdown(f"<p>{tags}</p>", unsafe_allow_html=True)

        # cols[i].image(get_img(url),
        #             use_column_width=True, # Manually Adjust the width of the image as per requirement
        # )

        cols[i].markdown(f"<div class='description'> <img  class='image' src='{get_img(url)}'> </div>", unsafe_allow_html=True)

        # expan_desc = cols[i].expander("Game Description")
        # expan_desc.markdown(f"<p class='desc'>{desc}</p>", unsafe_allow_html=True)

        if i == 0:
            i = 2
        else:
            i = 0
