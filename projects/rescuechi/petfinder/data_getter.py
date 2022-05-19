import os
import pandas as pd

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import petpy

def check_for_secrets():
    assert os.getenv("PETFINDER_KEY") is not None
    assert os.getenv("PETFINDER_SECRET") is not None

# get organizations in the state of illinois
def get_chi_orgs(pf):
    """Get the all orgs within 100 miles of Chicago"""
    # setting pages to none will return all results
    return pf.organizations(location="Chicago, IL", distance=100, results_per_page=50, pages=None)

def get_adoptable_dogs_by_org(pf, org_id):
    """Get dogs for a particular org_id"""
    return pf.animals(animal_type="dog", organization_id=org_id, results_per_page=50, pages=None)