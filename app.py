"""This streamlit app will record audio."""

import datetime
import glob
import re

import librosa
import numpy as np
import pandas as pd
import scipy
import streamlit as st
from audio_recorder_streamlit import audio_recorder


def _read_and_reample_audio(filepath: str, sample_rate: int = 2000) -> np.ndarray:
    """Read wav file and change its sample rate.

    input:
    ------
        filepath: str:
            path of the audio file.
        sample_rate: int:
            desired sample rate for the selected audio. default is 2000.

    output:
    ------
        np.ndarray:
            the signal in numpy array format.
    """
    signal, _ = librosa.load(path=filepath, sr=sample_rate, mono=True, duration=60)
    return signal


def _get_abs_fft(signal: np.ndarray) -> np.ndarray:
    """Gives the absolute value of the fft of the signal.

    input:
    -----
        signal: np.ndarray:
            signal in np array format.

    output:
    ------
        np.ndarray:
            absolute fft in np array format
    """
    return abs(np.fft.fft(signal))


def get_entropy(
    sample_audio_path: str,
    ref_audio_path: str,
    sample_rate: int = 2000,
    duration: float = 60,
) -> float:
    """Gives the entropy of the two distributions.

    input:
    -----
        sample_audio_path: str:
            path of the sample audio.
        ref_audio_path: str:
            path of the refference audio with which entropy to be calculated.
        sample_rate: int:
            sample rate of the signal. default value is 2000.
        duration: float:
            max duration of the audio to be used for entropy calculation. default value is 60 seconds.
    output:
    ------
        float:
         entropy of the two signal fft's.
    """
    sample_audio = _read_and_reample_audio(
        filepath=sample_audio_path, sample_rate=sample_rate
    )
    ref_audio = _read_and_reample_audio(
        filepath=ref_audio_path, sample_rate=sample_rate
    )
    number_of_data_points = min(
        len(sample_audio), len(ref_audio), sample_rate * duration
    )
    fft_sa = _get_abs_fft(sample_audio)
    fft_ra = _get_abs_fft(ref_audio)
    return scipy.stats.entropy(
        fft_sa[:number_of_data_points], fft_ra[:number_of_data_points]
    )


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
)  # object audio_recorder inetiated.

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
            options=df.query("user == @user_selected_2")["machine"].unique(),
        )

        with col_3:

            date_selected_2 = st.radio(
                label="select date",
                options=df.query(
                    "user == @user_selected_2 and machine == @machine_selected_2"
                )["date"].unique(),
            )

            with col_4:
                time_selected_2 = st.radio(
                    label="select time",
                    options=df.query(
                        "user == @user_selected_2 and machine == @machine_selected_2\
                                 and date == @date_selected_2"
                    )["time"].unique(),
                )


# signal_file = df.loc[
#     (df["user"] == user_selected_2)
#     & (df["machine"] == machine_selected_2)
#     & (df["date"] == date_selected_2)
#     & (df["time"] == time_selected_2),
#     "filename",
# ].values[0]
signal_file = df.query(
    "user == @user_selected_2 and machine == @machine_selected_2 \
            and date == @date_selected_2 and time == @time_selected_2"
)["filename"].values[0]


st.audio(signal_file)

st.write("first file selected is ", signal_file)


st.header("Select the :blue[Second file].")
col_1, col_2, col_3, col_4 = st.columns(4)

with col_1:

    user_selected = st.radio(
        label="select user", options=df["user"].unique(), key="2nd"
    )

    with col_2:
        machine_selected = st.radio(
            label="select machine",
            options=df.query("user == @user_selected")["machine"].unique(),
            key="2nd_1",
        )

        with col_3:
            date_selected = st.radio(
                label="select date",
                options=df.query(
                    "user ==@user_selected and machine==@machine_selected"
                )["date"].unique(),
                key="2nd_2",
            )

            with col_4:
                time_selected = st.radio(
                    label="select time",
                    options=df.query(
                        "user ==@user_selected and machine==@machine_selected and date ==@date_selected"
                    )["time"].unique(),
                    key="2nd_3",
                )


# ref_signal_file = df.loc[
#     (df["user"] == user_selected)
#     & (df["machine"] == machine_selected)
#     & (df["date"] == date_selected)
#     & (df["time"] == time_selected),
#     "filename",
# ].values[0]
ref_signal_file = df.query(
    "user == @user_selected and machine == @machine_selected\
        and date == @date_selected and time == @time_selected"
)["filename"].values[0]

st.audio(ref_signal_file)
st.write("Second file selected is ", ref_signal_file)

st.header(":blue[Calculate Entropy.]")
calculate = st.button(label="Click to calculate Entropy")
if calculate:

    st.write(
        "entropy of the given audio's is = ",
        get_entropy(signal_file, ref_signal_file, sample_rate=1000, duration=10),
    )
