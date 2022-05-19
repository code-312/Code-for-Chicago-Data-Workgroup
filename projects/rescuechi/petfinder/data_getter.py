import os
import pandas as pd
import requests
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def check_for_secrets():
    assert os.getenv("PETFINDER_KEY") is not None
    assert os.getenv("PETFINDER_SECRET") is not None

def get_token():
    """
    This is the example of getting a token from the petfinder docs:
    curl -d "grant_type=client_credentials&client_id={CLIENT-ID}&client_secret={CLIENT-SECRET}" https://api.petfinder.com/v2/oauth2/token
    """
    # make sure you have required variables in your environment
    check_for_secrets()
    
    url = "https://api.petfinder.com/v2/oauth2/token"

    CLIENT_ID = os.getenv("PETFINDER_KEY")
    CLIENT_SECRET = os.getenv("PETFINDER_SECRET")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"

    response = requests.post(url, headers=headers, data=data)

    # make sure it succeeded
    assert response.status_code == 200

    # just return the access_token
    return response.json()["access_token"]

# # get organizations in the state of illinois
# def get_chi_orgs(pf):
#     """Get the all orgs within 100 miles of Chicago"""
#     # setting pages to none will return all results
#     return pf.organizations(location="Chicago, IL", distance=100, results_per_page=50, pages=None)

def get_organizations():

    token = get_token()

    url = "https://api.petfinder.com/v2/organizations"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "location": "Chicago, IL",
        "sort": "distance",
        "distance": 100,
        "limit": None,
        "page": 1
    }

    # make the first call, and check how many total pages there are
    response = requests.get(url, headers=headers, params=params)

    # make sure that it actually worked
    assert response.status_code == 200

    pagination = response.json()["pagination"]

    # this is how many pages we need to iterate over
    num_pages = pagination["total_pages"]

    # this is how many total orgs we expect to catch
    total_count = pagination["total_count"]

    # start a list of orgs that we'll append to
    all_orgs = response.json()["organizations"]
    
    # iterate over all pages, starting with the 2nd page
    for page in range(2,num_pages+1):
        # update params for current page
        params["page"] = page

        # make the call
        response = requests.get(url, headers=headers, params=params)

        # append orgs to master list
        all_orgs += response.json()["organizations"]

    # check that we acutally got all organizations
    assert len(all_orgs) == total_count

    # convert to pandas
    df_orgs = pd.DataFrame(all_orgs)

    # save to pickle file
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df_orgs.to_pickle(DATA_DIR / "chicago_orgs.pkl")

    return df_orgs

