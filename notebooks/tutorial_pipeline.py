import pathlib
import datajoint as dj
from element_animal import subject, surgery
from element_animal.subject import Subject  # Dependency for session schema
from element_animal.surgery import Implantation  # Dependency for optogenetics schema
from element_lab import lab
from element_lab.lab import Lab, Project, Protocol, Source, User
from element_session import session_with_id as session
from element_session.session_with_id import Session
from element_optogenetics import optogenetics


if "custom" not in dj.config:
    dj.config["custom"] = {}

# overwrite dj.config['custom'] values with environment variables if available

dj.config["custom"]["database.prefix"] = os.getenv(
    "DATABASE_PREFIX", dj.config["custom"].get("database.prefix", "")
)

db_prefix = dj.config["custom"].get("database.prefix", "")


# Activate schemas
lab.activate(db_prefix + "lab")
subject.activate(db_prefix + "subject", linking_module=__name__)

Experimenter = User
session.activate(db_prefix + "session", linking_module=__name__)


optogenetics.activate(db_prefix + "optogenetics", linking_module=__name__)
