import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird - Easy Mode", layout="centered")

st.title("🐣 Flappy Bird – Easy Mode")
st.write("Click or press space to flap. Game starts after your first move!")

with open("flappy.html", "r") as f:
    html = f.read()
components.html(html, height=600)
