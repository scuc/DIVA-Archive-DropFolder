import logging
import logging.config
import os
from datetime import datetime
from sys import platform
from time import localtime, strftime

import yaml

import check_root_paths as crp
import config as cfg
import dropfolder_check_csv as dfc
import permissions_fix as permissions

config = cfg.get_config()

script_root = config["paths"]["script_root"]
mac_root_folders = config["paths"]["mac_root_path"]
drop_folders = [
    os.path.join(x, config["paths"]["drop_folder"]) for x in mac_root_folders
]

logger = logging.getLogger(__name__)


def set_logger():
    """
    Setup logging configuration
    """
    path = os.path.join(script_root, "logging.yaml")

    with open(path, "rt") as f:
        config = yaml.safe_load(f.read())

        # get the file name from the handlers, append the date to the filename.
        for i in config["handlers"].keys():
            local_datetime = str(strftime("%A, %d. %B %Y %I:%M%p", localtime()))

            if "filename" in config["handlers"][i]:
                log_filename = config["handlers"][i]["filename"]
                base, extension = os.path.splitext(log_filename)
                today = datetime.today()

                log_filename = "{}_{}{}".format(
                    base, today.strftime("%Y%m%d"), extension
                )
                config["handlers"][i]["filename"] = log_filename
            else:
                continue

        logger = logging.config.dictConfig(config)

    return logger


def main():
    """
    This function is the entry point of the DIVA Archive Script.
    It performs various tasks related to archiving and logging.

    Returns:
        None
    """

    os.chdir(script_root)
    date_start = str(strftime("%A, %d. %B %Y %I:%M%p", localtime()))

    start_msg = f"\n\
    ================================================================\n\
                DIVA Archive Script - Start\n\
                    {date_start}\n\
    ================================================================\n\
   "

    logger.info(start_msg)

    root_paths = crp.check_root_paths()

    # if root_paths is not False:
    #     dfc.create_csv()
    # else:
    #     pass

    if platform == "darwin" and root_paths is not False:
        p = permissions.chmod_chown(drop_folders)
    else:
        p = None

    if p != "error" or platform != "darwin":
        dfc.create_csv()
    else:
        pass

    date_end = str(strftime("%A, %d. %B %Y %I:%M%p", localtime()))

    complete_msg = f"\n\
    ================================================================\n\
                DIVA WatchFolder Check - Complete\n\
                    {date_end}\n\
    ================================================================\n\
    "
    logger.info(complete_msg)
    return


if __name__ == "__main__":
    set_logger()
    main()
