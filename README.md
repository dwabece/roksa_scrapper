# roksa_scrapper
Crawler for roksa's ads.

I made it just to gather information about escorts market in poland for further visualization with Tableau and some machine learning.

Scraped results CSV can be found [here](https://github.com/dwabece/roksa_scrapper/blob/master/exported/dump_30dec.csv) and tableau presentation is [linked here](https://public.tableau.com/profile/mj.krac7854#!/vizhome/rox/Story1) (it's in polish and still under development).

Crawler through search results (with empty filters) and scrapes information from adverts such as:
* divas name
* age
* weight
* height
* breast size
* price per hour
* city
* known languages
* offered services
* description

Fetching ads is being executed by celery (with limit of 50 tasks per minute) and saved to mongodb.
