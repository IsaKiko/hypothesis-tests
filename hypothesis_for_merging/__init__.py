def merge_and_filter(df1, df2):
    df = df1.merge(df2, on='id').query("id > 0")
    df.drop_duplicates(subset=['id', 'cat', 'human'], inplace=True)
    return df