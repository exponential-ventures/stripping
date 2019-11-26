import uuid

from stripping import setup_stripping


def set_up_stripping_for_tests():
    tmp_dir = f"/tmp/{str(uuid.uuid4())}/cache/"

    st, context = setup_stripping(tmp_dir)

    # Resetting lists to prevent cross-test contamination
    st.steps = list()
    st.chain_steps = list()

    return st, context
