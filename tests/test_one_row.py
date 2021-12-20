from hypothesis import strategies as st, given, Verbosity, settings
import pandas as pd

from hypothesis_for_merging import merge_and_filter

@st.composite
def create_test_samples(
        draw,
        st_id=st.integers(),
        st_cat_name=st.from_regex(r'(Mister|Ms) [A-Z][a-z]*pants', fullmatch=True),
        st_human_name=st.from_regex(r'[A-Z][a-z]*', fullmatch=True),
    ):
    id = draw(st_id)
    cat_name = draw(st_cat_name)
    human_name = draw(st_human_name)

    cat = pd.DataFrame([{"id": id, "cat": cat_name}])
    human = pd.DataFrame([{"id": id, "human": human_name}])

    return cat, human, id, cat_name, human_name


@given(data = create_test_samples(st_id=st.integers(min_value=1)))
def test_merging_healthy(data):
    cat, human, id, cat_name, human_name = data

    merged_df = merge_and_filter(cat, human)
    expected_df = pd.DataFrame([{"id": id, "cat": cat_name, "human": human_name}])
    print(f'Meow: {cat_name}, Hooman: {human_name}')

    assert merged_df.equals(expected_df)


@given(data = create_test_samples(st_id=st.integers(max_value=0)))
def test_merging_unhealthy(data):
    cat, human, id, cat_name, human_name = data
    merged_df = merge_and_filter(cat, human)

    assert len(merged_df) == 0

