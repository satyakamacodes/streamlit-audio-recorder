"""This streamlit app will record audio."""

import datetime
import glob
import re

import pandas as pd
import streamlit as st
from audio_recorder_streamlit import audio_recorder

USERS = ["abd", "xyz", "noq", "apd"]
MACHINE = ["machine-1", "machine-2", "machine-3"]
df = pd.DataFrame(columns=["user", "machine", "date", "time", "filename"])

st.title(":green[Audio Analysis]")
st.header(":red[Record audio here.]")
col1, col2 = st.columns(2)
with col1:
    user = st.selectbox(label="Select User", options=USERS)


with col2:
    machine = st.selectbox(label="Select Machine", options=MACHINE)
st.text(f"{user} is using {machine}")

audio_bytes = audio_recorder(
    text="Click the mic to record", energy_threshold=(-1.0, 1.0), pause_threshold=10.0
)

if audio_bytes:
    st.audio(data=audio_bytes, format="audio/wav")

    if st.button("save"):
        filename = f"./recordings/__{user}__{machine}__{datetime.datetime.now().strftime('%d-%m-%Y__%H-%M-%S')}__.wav"
        # st.text("file saved") # dispaly the file name of the saved audio.
        with open(filename, "wb") as file:
            file.write(audio_bytes)
            st.text("Audio files saved.")

# section 2: selecting a particular saved audio file.
files_present = glob.glob("./recordings/*.wav")

# st.text(files_present)  # display the files present in the recording folder

for filename in files_present:
    matches = re.findall(pattern="_([^_]+)_", string=filename)
    new_row = {
        "user": matches[0],
        "machine": matches[1],
        "date": matches[2],
        "time": matches[3],
        "filename": filename,
    }
    # df = df.append(new_row, ignore_index=True)
    new_row_df = pd.DataFrame(new_row, index=[0])
    df = pd.concat([df, new_row_df], ignore_index=True)

    # df = df.set_index("filename")

# st.dataframe(df)   # display the data frame for audio selection


st.header("Select the :blue[First file].")
col_1, col_2, col_3, col_4 = st.columns(4)

with col_1:
    user_selected_2 = st.radio(label="select user", options=df["user"].unique())

    with col_2:
        machine_selected_2 = st.radio(
            label="select machine",
            options=df.loc[df["user"] == user_selected_2, "machine"].unique(),
        )

        with col_3:
            date_selected_2 = st.radio(
                label="select date",
                options=df.loc[
                    (df["user"] == user_selected_2)
                    & (df["machine"] == machine_selected_2),
                    "date",
                ].unique(),
            )

            with col_4:
                time_selected_2 = st.radio(
                    label="select time",
                    options=df.loc[
                        (df["user"] == user_selected_2)
                        & (df["machine"] == machine_selected_2)
                        & (df["date"] == date_selected_2),
                        "time",
                    ],
                )


selected_file_1 = df.loc[
    (df["user"] == user_selected_2)
    & (df["machine"] == machine_selected_2)
    & (df["date"] == date_selected_2)
    & (df["time"] == time_selected_2),
    "filename",
].values[0]


st.audio(selected_file_1)

st.write("first file selected is ", selected_file_1)

# def select_file(df: pd.DataFrame, promt: str) -> str:
#     """Select path of the file by user, machine, date and time.
#     Gives option to hear the audio too."""
#     st.header(f"Select the :blue[{promt}].")

#     col_1, col_2, col_3, col_4 = st.columns(4)

#     with col_1:
#         user_selected = st.radio(label="select user", options=df["user"].unique())

#         with col_2:
#             machine_selected = st.radio(
#                 label="select machine",
#                 options=df.loc[df["user"] == user_selected, "machine"].unique(),
#             )

#             with col_3:
#                 date_selected = st.radio(
#                     label="select date",
#                     options=df.loc[
#                         (df["user"] == user_selected)
#                         & (df["machine"] == machine_selected),
#                         "date",
#                     ].unique(),
#                 )

#                 with col_4:
#                     time_selected = st.radio(
#                         label="select time",
#                         options=df.loc[
#                             (df["user"] == user_selected)
#                             & (df["machine"] == machine_selected)
#                             & (df["date"] == date_selected),
#                             "time",
#                         ],
#                     )

#     selected_file = df.loc[
#         (df["user"] == user_selected)
#         & (df["machine"] == machine_selected)
#         & (df["date"] == date_selected)
#         & (df["time"] == time_selected),
#         "filename",
#     ].values[0]

#     st.audio(selected_file)

#     return selected_file


# first_audio_path = select_file(df=df, promt="First audio")
# second_audio_path = select_file(df=df, promt="Second audio")


st.header("Select the :blue[Second file].")
col_1, col_2, col_3, col_4 = st.columns(4)

with col_1:
    user_selected = st.radio(
        label="select user", options=df["user"].unique(), key="2nd"
    )

    with col_2:
        machine_selected = st.radio(
            label="select machine",
            options=df.loc[df["user"] == user_selected, "machine"].unique(),
            key="2nd_1",
        )

        with col_3:
            date_selected = st.radio(
                label="select date",
                options=df.loc[
                    (df["user"] == user_selected) & (df["machine"] == machine_selected),
                    "date",
                ].unique(),
                key="2nd_2",
            )

            with col_4:
                time_selected = st.radio(
                    label="select time",
                    options=df.loc[
                        (df["user"] == user_selected)
                        & (df["machine"] == machine_selected)
                        & (df["date"] == date_selected),
                        "time",
                    ],
                    key="2nd_3",
                )


selected_file = df.loc[
    (df["user"] == user_selected)
    & (df["machine"] == machine_selected)
    & (df["date"] == date_selected)
    & (df["time"] == time_selected),
    "filename",
].values[0]


st.audio(selected_file)
st.write("Second file selected is ", selected_file)
