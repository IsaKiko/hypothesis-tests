# Hypothesis tests for dataframes

## Running the tests (which is really all there is to this)

```bash
pip install poetry
poetry install
pytest -s
```

## What it does...

Property-based testing (see below) with hypothesis.
The 'main' package code merges two dataframes, drops duplicates and any value where the `id` <= 0.
The tests are set up to create two pandas DataFrames, one with `id` and a `cat_name`, one with an `id` and a `human_name`.

## Different set up for different considerations

* Creating values from Regex (all files)
  * Hypothesis allows to create values that match a particular regular expression. This is neat for well-behaved defaults that can then be overwritten with one test at a time.

* Deterministic structure (test_one_row and test_full_df)
  * This allows for the greatest control when we have lots of tables that need to be merged. Ids can explicitly be set up to be the same across different tables and the same would be true for any other values we use to join tables. Returning these values also allows to construct the expected output data.

* Random lenghts of dataframes (test_pandas_df)
  * Introducing the ability to test along the dimension of the length of a dataframe, but sacrificing some control over joins.
  * This setup is similar to how it would be done with Pandera.

## Why might this be valuable

Instead of passing in a whole dataframe and testing with that, hypothesis allows us to set up a default dataframe (from regex for example) to then only change the values we want to test for, one at a time.