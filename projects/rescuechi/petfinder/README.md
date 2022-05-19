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