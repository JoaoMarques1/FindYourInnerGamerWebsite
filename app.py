import streamlit as st
import requests
from utils import get_img, get_data_from_gcp
import streamlit as st

#API url
url = 'https://find-your-inner-gamer-7oqykbx6lq-ew.a.run.app/predict'

# configuring page with wide view
st.set_page_config(
    page_title="Find Your Inner Gamer!",
    page_icon="🕹️", layout="wide"
)

# setting default value for clik variable to False
clik = False

# Creating three columns and putting title in the middle
st.markdown("<h1 style='text-align: center;'>🎮 Find Your Inner Gamer</h1>", unsafe_allow_html=True)
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
            st.write("Review Scale:")
            st.write("🦠 - Negative;")
            st.write("★ - Positive;")
            response = requests.get(url, params)
            pred = response.json()
            clik = True


# creating font
st.markdown("""
<style>
.tags {
    height: 3em;
    line-height: 1.6;
    margin: 2em auto;
}

.review{
    height: 3em;
    line-height: 1.6;
    margin: 1em auto;
}

.desc{
    height: 3em;
    line-height: 1.6;
    margin: 1em auto;
}

.title{
    height: 3em;
    margin: 1em auto;
}
</style>
""", unsafe_allow_html=True)



# displaying recommended titles
if clik == False:
    col1, col2, col3 = st.columns([1, 2, 1])

    col2.image('https://images.newscientist.com/wp-content/uploads/2021/10/27162905/PRI_207080436.jpg?crop=16:9,smart&width=1200&height=675&upscale=true')
else:
    cols = st.columns(2)
    i = 0

    reviews_scale = {
        "Overwhelmingly Negative": '🦠'*5,
        "Very Negative": '🦠'*4,
        "Negative": '🦠'*3,
        "Mostly Negative": '🦠'*2,
        'Mixed': '★' + '☆'*4,
        "Mostly Positive": '★'*2 + '☆'*3,
        "Positive": '★'*3 + '☆'*2,
        "Very Positive": '★'*4 + '☆',
        "Overwhelmingly Positive": '★'*5
    }

    for game in pred['title'][1:]:

        row = df[df['name']== game]
        url = row['url'].iloc[0]
        tags = row['popular_tags'].iloc[0]
        desc = row['desc_snippet'].iloc[0]
        review = row['reviews'].iloc[0]


        cols[i].markdown(f"<h1 class='title'><a href='{url}'>{game}</a></h1>", unsafe_allow_html=True)
        cols[i].markdown(f"<p class='tags'>{tags}</p>", unsafe_allow_html=True)
        cols[i].image(get_img(url),
                    use_column_width=True, # Manually Adjust the width of the image as per requirement
        )
        cols[i].markdown(
            f"<p class='review'>{review} {reviews_scale[review]}</p>",
            unsafe_allow_html=True
        )

        cols[i].markdown(
            f"<p class='desc'>{desc}</p>",
            unsafe_allow_html=True
        )

        if i == 0:
            i = 1
        else:
            i = 0
