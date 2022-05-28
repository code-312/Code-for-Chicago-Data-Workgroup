# Setup

To use the functions in this directory, you'll need to set up your PetFinder API key
and secret as environment variables.

First, request an API and secret, and put these somewhere safe. You can request an API
key [here](https://www.petfinder.com/developers/).

Next, export your key and secret to your enviornment. For example, you could run:

```bash
export PETFINDER_KEY=<your-api-key>
export PETFINDER_SECRET=<your-api-secret>
```

Then, install the requirements:

```bash
pip-sync requirements.txt
```

# Running

The code in `data_getter` supports pulling data about either organizations or animals near Chicago from the Petfinder API.

After setting up your environment, you can use the functions `get_organizations` or `get_animals` to collect data, and save it to file.

Running each of these functions will return a pandas DataFrame with the results, and will save the results locally to pickle and CSV files.

# Results

The results of the first 1000 animals pages (basic user daily usage cap), run with default parameters, can be found in the shared Google Drive [here](https://drive.google.com/drive/u/0/folders/16YyhvVVQVecoBtmWOVZOR0rynGKkmYj_).