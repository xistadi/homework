from Packages import reaper
from Packages import master

all_rate = reaper.scrape_from_api()
reaper.insert_sql(all_rate)
master.input_api()
