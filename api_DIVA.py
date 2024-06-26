import json
import logging
import pprint

import pandas as pd
import requests
from pandas import json_normalize

import config as cfg
import get_authentication as auth

config = cfg.get_config()

url_core_manager = config["urls"]["core_manager_api"]
source_destinations = config["DIVA_Source_Dest"]

logger = logging.getLogger(__name__)


def file_check(objectName):
    """
    Use the DIVA REST API to check object against the DB to see if it already exists
    Status Code 200 = object found in DIVA DB
    Status Code 400 = invalid object name provided
    Status Code 404 = object not found in DIVA DB
    """

    try:
        token = auth.get_auth()
        url_object_byobjectName = f"https://{url_core_manager}/objects/filesAndFolders"

        params = {
            "objectName": objectName,
            "collectionName": "LTFS",
            "listType": 0,
            "startIndex": 1,
            "batchSize": 5,
        }

        headers = {
            "Accept": "application/json",
            "Authorization": token,
        }

        db_check_msg = f"Checking DIVA DB for object name:  {objectName}"
        logger.debug(db_check_msg)

        r = requests.get(
            url_object_byobjectName, headers=headers, params=params, verify=False
        )

        response = r.json()

        code = r.status_code

        status_code_msg = f"DIVA DB Check returned a status code: {code}"
        logger.debug(status_code_msg)

        if code == 404:
            return False
        elif code == 200:
            return True
        else:
            return "error"

    except Exception as e:
        api_exception_msg = f"Exception raised on the DIVA DB check: \n {e} \n"
        logger.error(api_exception_msg)
        return "error"


def get_object_info(objectName):
    """
    400 = Invalid object supplied
    404 = Object not found
    """

    try:
        token = auth.get_auth()
        url = f"https://{url_core_manager}/objects/info"

        params = {
            "objectName": objectName,
            "collectionName": "LTFS",
        }

        headers = {
            "Accept": "application/json",
            "Authorization": token,
        }

        db_check_msg = f"Checking object info for:  {objectName}"
        logger.debug(db_check_msg)

        r = requests.get(url, headers=headers, params=params, verify=False)

        response = r.json()
        logger.debug(f"Status Code = {r.status_code}")

        if r.status_code == 200:
            tapeInstances = len(response["tapeInstances"])
        elif r.status_code == 404:
            tapeInstances = 0
        else:
            tapeInstances = -1

        logger.info(f"tapeInstances = {tapeInstances}")
        return tapeInstances

    except Exception as e:
        api_exception_msg = f"Exception raised on fileInfo check for: \n {e} \n"
        logger.error(api_exception_msg)
        tapeInstances = -1
        return tapeInstances


def get_requests(startDateTime):
    """
    Check DIVA to count the list of archive requests processed since 00:00:00 on the current day.
    The request is submitted with UTC time, and local server is eastern time, for the startDateTime
    is actually "05:00:00" to compensate.

    EXAMPLE FULL RESPONSE:
    {'id': 292865, 'abortReason': {'code': 0, 'description': '', 'name': 'DIVA_AR_NONE'
    }, 'additionalInfo': '<?xml version="1.0" encoding="UTF-8"?>\n<ADDITIONAL_INFO xmlns="http://www.fpdigital.com/divarchive/additionalInfoRequestInfo/v1.0"></ADDITIONAL_INFO>', 'completionDate': 1657682357, 'currentPriority': 66, 'destinationTape': '183375', 'objectName': 'NBLZ89604_LifeBelowZero_ShadowDwellers_2997p_AIR.mov', 'progress': 100, 'sourceTape': ' ', 'stateCode': 3, 'stateName': 'DIVA_COMPLETED', 'stateDescription': 'Completed', 'submissionDate': 1657681383, 'type': 'DIVA_ARCHIVE_REQUEST', 'typeDescription': 'Archive', 'typeCode': 0, 'statusCode': 1000, 'statusDescription': 'success', 'statusName': 'DIVA_OK', 'collectionName': 'AXF'
    }
    """
    try:
        token = auth.get_auth()
        url_requests = f"https://{url_core_manager}/requests"

        params = {
            "sortField": "ID",
            "sortDirection": "ASC",
            "type": "Archive",
            "startDateTime": startDateTime,
            "states": [
                "Running",
                "Waiting for resources",
                "Waiting for operator",
                "Pending",
                "Transferring",
            ],
            "collectionName": "LTFS",
        }

        headers = {
            "Accept": "application/json",
            "Authorization": token,
        }

        db_check_msg = f"Checking DIVA DB for archive requests"
        logger.info(db_check_msg)

        r = requests.get(url_requests, headers=headers, params=params, verify=False)
        response = r.json()
        json_data = json_normalize(response)
        data = json_data["requests"][0]
        df = pd.DataFrame(
            data,
            columns=[
                "id",
                "objectName",
                "progress",
                "stateCode",
                "stateName",
                "stateDescription",
                "statusCode",
                "statusDescription",
            ],
        )
        return df

    except Exception as e:
        api_exception_msg = f"Exception raised on the DIVA DB check: \n {e} \n"
        logger.error(api_exception_msg)
        return "error"


if __name__ == "__main__":
    get_object_info(objectName="")
