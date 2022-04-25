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
    ARG_STUDY_NUMBER = "ICA-00048"
    ARG_FROM_HF = "testing"
    ARG_TO_HF = "testing"

    # Health facility specific fields
    CONTACT_VARIABLES = ['community', 'other_community', 'address', 'further_contact_details']

    project_from = redcap.Project(URL, PROJECTS[ARG_FROM_HF])
    project_to = redcap.Project(URL, PROJECTS[ARG_TO_HF])

    # Get REDCap record id of study participant to be migrated
    print("Getting records from {}".format(ARG_STUDY_NUMBER))
    api_filter_logic = "[epipenta1_v0_recru_arm_1][study_number] = '{}'".format(ARG_STUDY_NUMBER)
    recruitment_records = project_from.export_records(filter_logic=api_filter_logic)
    record_id = recruitment_records[0]['record_id']
    print("The record id of participant {} is {}".format(ARG_STUDY_NUMBER, record_id))

    # Get the ALL REDCap records (from every event) of this study participant with the record id
    participant_records = project_from.export_records(records=[record_id])
    print(participant_records)

    # Remove contact details in the ID DCI as they refer to the previous residence
    for variable in CONTACT_VARIABLES:
        participant_records[0][variable] = ''

    # Import study participant records to the new HF/REDCap project
    # todo: There's a bug when migrating participants that have some SAE with the ICD10 code completed, the API does not
    #       allow to import data on this kind of fields
    print("Importing data from {} to a new record into {}".format(ARG_STUDY_NUMBER, ARG_TO_HF))
    response = project_to.import_records(participant_records, force_auto_number=True)
    print(response)
