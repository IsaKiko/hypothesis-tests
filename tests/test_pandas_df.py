from hypothesis import strategies as st, given, Verbosity, settings
import pandas as pd

from hypothesis_for_merging import merge_and_filter
from hypothesis.extra.pandas import data_frames, column


@st.composite
def create_test_samples(
        draw,
        size=10,
        st_id=st.integers(min_value=-10, max_value=10),
        st_cat_name=st.from_regex(r'(Mister|Ms) [A-Z][a-z]*pants', fullmatch=True),
        st_human_name=st.from_regex(r'[A-Z][a-z]*', fullmatch=True),
    ):

    st_cat = data_frames(
        columns=[
        column('id', dtype=int), column('cat', dtype=str)],
        rows=st.tuples(st_id, st_cat_name)
    )

    st_human = data_frames(
        columns=[
        column('id', dtype=int), column('human', dtype=str)],
        rows=st.tuples(st_id, st_human_name)
    )

    cat = draw(st_cat)
    human = draw(st_human)

    return cat, human


@given(data = create_test_samples())
@settings(max_examples=1000)
def test_merging_pandas(data):
    cat, human = data

    merged_df = merge_and_filter(cat, human)
    full_df = cat.merge(human, on="id")

    if len(merged_df) > 0:
        print(merged_df)

    assert (merged_df.id > 0).all()
    assert len(merged_df) <= len(full_df)
