from hypothesis import strategies as st, given, Verbosity, settings
import pandas as pd

from hypothesis_for_merging import merge_and_filter

@st.composite
def create_test_samples(
        draw,
        size=10,
        st_id=st.integers(min_value=-1000, max_value=1000),
        st_cat_name=st.from_regex(r'(Mister|Ms) [A-Z][a-z]*pants', fullmatch=True),
        st_human_name=st.from_regex(r'[A-Z][a-z]*', fullmatch=True),
    ):

    id = draw(st.lists(st_id, min_size=size, max_size=size))
    cat_name = draw(st.lists(st_cat_name, min_size=size, max_size=size))
    human_name = draw(st.lists(st_human_name, min_size=size, max_size=size))

    cat = pd.DataFrame(
        {
            "id": id,
            "cat": cat_name,
        }
    )

    human = pd.DataFrame(
        {
            "id": id,
            "human": human_name,
        }
    )

    return cat, human, id, cat_name, human_name


@given(data = create_test_samples())
def test_merging_full(data):
    cat, human, id, cat_name, human_name = data

    merged_df = merge_and_filter(cat, human)
    print('---')
    print(len(cat), len(human))
    print(len(merged_df))
    full_df = cat.merge(human, on="id")

    assert (merged_df.id > 0).all()
    assert len(merged_df) <= len(full_df)
