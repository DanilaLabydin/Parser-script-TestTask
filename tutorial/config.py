import os
import logging
from configparser import ConfigParser


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    # change handler name
    handlers=[logging.FileHandler("/tmp/crm_logger.log"), logging.StreamHandler()],
)


LOGGER = logging.getLogger(__name__)


if not os.path.isfile("database.ini"):
    raise Exception("No database.ini file found")


def db_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()

    parser.read(filename)

    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return db_config
