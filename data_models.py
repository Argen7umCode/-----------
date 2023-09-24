from dataclasses import dataclass
from datetime import datetime


@dataclass
class Organization:

    id           : str
    name         : str
    inn          : str
    url          : str
    date_include : datetime
    date_updated : datetime

@dataclass
class SROMember:
    id                         : int = None 
    full_description           : str = None 
    short_description          : str = None 
    director                   : str = None 
    inn                        : str = None 
    inventory_number           : str = None 
    member_status              : str = None 
    member_type                : str = None 
    ogrnip                     : str = None 
    registration_number        : str = None 
    registry_registration_date : datetime = None 
    short_description          : str = None 
    deactivate_message         : str = None 
    sro_full_description       : str = None 
    sro_id                     : int = None 
    sro_registration_number    : str = None 
