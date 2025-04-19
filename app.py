import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird on Streamlit", layout="centered")

st.title("🐦 Flappy Bird (Streamlit Edition)")
st.write("Click or press space to flap and avoid the pipes!")

# Load HTML + JS game
with open("flappy.html", "r") as f:
    game_html = f.read()

components.html(game_html, height=600)
