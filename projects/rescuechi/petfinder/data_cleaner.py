import pandas as pd
from pathlib import Path

DATA_FOLDER = Path(__file__).parent / "data"

def calc_los(raw_published_col, raw_status_change_col):
    """
    Calculate the length of stay

    Returns
    -------
    Column with the length of stay for each animal, as an integer with units of number
    of days
    """

    published_dt = pd.to_datetime(raw_published_col)
    status_change_dt = pd.to_datetime(raw_status_change_col)

    los_days = (status_change_dt - published_dt).dt.days
    los_days.name = "los"
    return los_days

def explode_column(col, col_prefix):
    """
    Take a column that cocntains a dictionary (e.g. breed, colors) and split it into
    multiple columns, one for each key of the dictionary
    """
    exploded = col.apply(pd.Series)
    exploded.columns = [f"{col_prefix}_{c}" for c in exploded.columns]

    return exploded

if __name__ == "__main__":

    data_file = DATA_FOLDER / "chicago_animals.pkl"
    df_raw = pd.read_pickle(data_file)

    # calculate the length of stay
    los = calc_los(df_raw["published_at"], df_raw["status_changed_at"])

    # clean up the columns that are dictionaries
    breeds = explode_column(df_raw["breeds"], "breed")
    colors = explode_column(df_raw["colors"], "color")
    environ = explode_column(df_raw["environment"], "good_with")
    attributes = explode_column(df_raw["attributes"], "attribute")

    # we can keep some columns as-is
    cols_as_is = ["id", "organization_id", "age", "gender", "size", "coat", "name"]

    # concatenate the final columns
    df_final = pd.concat([df_raw[cols_as_is], los, breeds, colors, environ, attributes], axis=1)
    
    # save cleaned dataframe to a pickle file
    df_final.to_pickle(DATA_FOLDER / "chicago_animals_cleaned.pkl")
