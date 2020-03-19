from pathlib import Path

import pandas as pd

from stripping import setup_stripping

file_path = "iris.csv"
current_dir = Path(__file__).parent.absolute()
st, ctx = setup_stripping('.stripping')


@st.step()
def load_dataset():
    ctx.ds = pd.read_csv(file_path)


@st.step()
def save_new_version_9d122046_e311_4125_baa7_128eb59d048d():
    new_name = f"iris_0_1_0.csv"
    ctx.ds.to_csv(new_name, mode="w+", encoding='utf-8', index=False)

st.execute()
