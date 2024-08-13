import os

from rich import print

from dotenv import load_dotenv

import nutshell
from nutshell import methods

load_dotenv()

find_activities = methods.FindActivityTypes()
ns = nutshell.NutshellAPI(os.getenv("NUTSHELL_USERNAME"), password=os.getenv("NUTSHELL_KEY"))
ns.api_calls = find_activities
activity_types = ns.call_api()
print(activity_types)
