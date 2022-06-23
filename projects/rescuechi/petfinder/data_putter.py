from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
TARGET_TABLE_NAME = "test_petfinder_table"

# this should probably be collected programmatically?
uri = "postgres://nojihrddrslbgo:776d62b321194d8811fca195eedb1d45a18361ddc6d3ff4bc2dc1e82fb5e9350@ec2-34-201-95-176.compute-1.amazonaws.com:5432/dbphfvpp1tnhjv"

# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# link to your database
engine = create_engine(uri, echo = False)

# this is the data we'll append to the database
df = pd.read_pickle(DATA_DIR / "chicago_animals.pkl")

# TEMP - drop table if exists if desired
engine.execute(f"DROP TABLE IF EXISTS {TARGET_TABLE_NAME}")

# this is one place where we might do some cleanup on the file
# at a minimum, can't have dictionaries as data elements
df = df[
    ["id", "type", "species", "age", "gender", "size", "coat", "name", "description", "status", "status_changed_at", "published_at"]
]

# we don't really need all the data for testing, just take a few rows
df = df.head(100)

df.to_sql(TARGET_TABLE_NAME, con = engine, if_exists='append')

# run a quick test to see how many rows there are
print(engine.execute(f"SELECT count(*) FROM {TARGET_TABLE_NAME}").fetchone())

# delete any duplicate records, in case the same data gets added in multiple times
delete_dupes_query = f"""
DELETE FROM {TARGET_TABLE_NAME} a USING (
    SELECT MIN(ctid) as ctid, id
    FROM {TARGET_TABLE_NAME} 
    GROUP BY id HAVING COUNT(*) > 1
) b
WHERE a.id = b.id 
AND a.ctid <> b.ctid
"""
engine.execute(delete_dupes_query)

# check final number of rows left in the table
print(engine.execute(f"SELECT count(*) FROM {TARGET_TABLE_NAME}").fetchone())