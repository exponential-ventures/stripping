from pathlib import Path

import pandas as pd

from stripping import setup_stripping

file_path = "iris.csv"
current_dir = Path(__file__).parent.absolute()
st, ctx = setup_stripping('.stripping')


@st.step()
def load_dataset():
    ctx.ds = pd.read_csv(file_path)
    # ctx.ds = pd.DataFrame([1, 2, 3, 4])
    # ctx.ds = pd.DataFrame({'name': ["a", "b", "c", "d", "e", "f", "g"],
    #                        'age': [20, 27, 35, 55, 18, 21, 35],
    #                        'designation': ["VP", "CEO", "CFO", "VP", "VP", "CEO", "MD"]})
    # with open(file_path, "r") as f:
    #     ctx.ds = pd.read_csv(f.read())



@st.step()
def access_ctx_ds():
    print(ctx.ds)


st.execute()
