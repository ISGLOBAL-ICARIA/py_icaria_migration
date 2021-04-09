#!/usr/bin/env python
""" Python script to migrate ICARIA study participant records from one health facility to another."""

import redcap
import tokens

__author__ = "Maximo Ramirez Robles"
__copyright__ = "Copyright 2021, ISGlobal Maternal, Child and Reproductive Health"
__credits__ = ["Maximo Ramirez Robles"]
__license__ = "MIT"
__version__ = "0.0.1"
__date__ = "20210409"
__maintainer__ = "Maximo Ramirez Robles"
__email__ = "maximo.ramirez@isglobal.org"
__status__ = "Dev"


if __name__ == '__main__':
    # Connection parameters
    URL = tokens.URL
    PROJECTS = tokens.REDCAP_PROJECTS

    # Arguments
    ARG_STUDY_NUMBER = "ICA-00126"
    ARG_FROM_HF = "HF15"
    ARG_TO_HF = "testing"

    # Health facility specific fields
    SPECIFIC_FIELDS = ['community', 'other_community', 'address', 'further_contact_details']

    project_from = redcap.Project(URL, PROJECTS[ARG_FROM_HF])
    project_to = redcap.Project(URL, PROJECTS[ARG_TO_HF])

    # Get REDCap records of study participant to be migrated
    print("Getting records from {}".format(ARG_STUDY_NUMBER))
    api_filter_logic = "[epipenta1_v0_recru_arm_1][study_number] = '{}'".format(ARG_STUDY_NUMBER)
    participant_records = project_from.export_records(filter_logic=api_filter_logic)
    print(participant_records)

    # Import study participant records to the new HF/REDCap project
    print("Importing data from {} to a new record into {}".format(ARG_STUDY_NUMBER, ARG_TO_HF))
    response = project_to.import_records(participant_records, force_auto_number=True)
    print(response)
