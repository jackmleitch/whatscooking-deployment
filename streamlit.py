import streamlit as st
import pandas as pd
import numpy as np
import SessionState

import config, rec_sys
from ingredient_parser import ingredient_parser

import nltk

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")


def make_clickable(name, link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = name
    return f'<a target="_blank" href="{link}">{text}</a>'


def main():
    st.markdown("# *What's Cooking? :cooking:*")

    st.markdown(
        "An ML powered app by Jack Leitch <a href='https://github.com/jackmleitch/Whatscooking-' > <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/600px-Octicons-mark-github.svg.png' width='20' height='20' > </a> ",
        unsafe_allow_html=True,
    )
    st.header("Given a list of ingredients, what different recipes can I can make?")
    st.markdown(
        "For example, what recipes can I make with the food I have in my apartment? Find out for yourself below!"
    )

    st.text("")

    session_state = SessionState.get(
        recipe_df="", recipes="", model_computed=False, execute_recsys=False
    )

    ingredients = st.text_input("Enter ingredients you would like to cook with")
    session_state.execute_recsys = st.button("Give me recommendations!")

    if session_state.execute_recsys:

        col1, col2, col3 = st.beta_columns([1, 6, 1])
        with col2:
            gif_runner = st.image("input/cooking_gif.gif")
        recipe = rec_sys.RecSys(ingredients)
        gif_runner.empty()

        # link is the column with hyperlinks
        recipe["url"] = recipe.apply(
            lambda row: make_clickable(row["recipe"], row["url"]), axis=1
        )
        recipe_display = recipe[["recipe", "url", "ingredients"]]
        session_state.recipe_display = recipe_display.to_html(escape=False)
        session_state.recipes = recipe.recipe.values.tolist()
        session_state.model_computed = True
        session_state.execute_recsys = False

    if session_state.model_computed:
        # st.write("Either pick a particular recipe or see the top 5 recommendations.")
        recipe_all_box = st.selectbox(
            "Either see the top 5 recommendations or pick a particular recipe ya fancy",
            ["Show me all!", "Just show me one please"],
        )
        if recipe_all_box == "Show me all!":
            st.write(session_state.recipe_display, unsafe_allow_html=True)
        else:
            st.selectbox("Select a delicious recipe", options=session_state.recipes)

    # sidebar stuff
    with st.sidebar.beta_expander("How it works?", expanded=True):
        st.subheader("How it works?")
        st.write(
            "For an in depth overview of the ML methods used and how I created this app, two blog posts are below."
        )
        blog1 = "https://jackmleitch.medium.com/using-beautifulsoup-to-help-make-beautiful-soups-d2670a1d1d52"
        blog2 = "https://towardsdatascience.com/building-a-recipe-recommendation-api-using-scikit-learn-nltk-docker-flask-and-heroku-bfc6c4bdd2d4"
        st.markdown(
            f"1. [Web Scraping Cooking Data With Beautiful Soup](upload:{blog1})"
        )
        st.markdown(
            f"2. [Building a Recipe Recommendation API using Scikit-Learn, NLTK, Docker, Flask, and Heroku](upload:{blog2})"
        )


if __name__ == "__main__":
    main()
