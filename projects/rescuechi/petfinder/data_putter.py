from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

uri = "postgres://nojihrddrslbgo:776d62b321194d8811fca195eedb1d45a18361ddc6d3ff4bc2dc1e82fb5e9350@ec2-34-201-95-176.compute-1.amazonaws.com:5432/dbphfvpp1tnhjv"

# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# link to your database
engine = create_engine(uri, echo = False)
# attach the data frame (df) to the database with a name of the 
# table; the name can be whatever you like
df = pd.read_pickle(DATA_DIR / "chicago_animals.pkl")

# this is one place where we might do some cleanup on the file
# at a minimum, can't have dictionaries as data elements
df = df[["id", "type", "species", "age", "gender", "size", "coat", "name", "description", "status", "status_changed_at", "published_at"]]

df.to_sql("test_petfinder_table", con = engine, if_exists='append')
# run a quick test 
# print(engine.execute("SELECT * FROM test-petfinder-table").fetchone())

# TODO - run a query that will delete any duplicate records, e.g. in case this gets run multiple times