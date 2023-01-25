"""This streamlit app will record audio."""

import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder(text="record audio here")

if audio_bytes:
    st.audio(data=audio_bytes, format="audio/wav")
