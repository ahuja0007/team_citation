from arxiv_scraper import *
import sys
categories=['hep-th','astro-ph']
output,query=scrape_arxiv_api_convert_to_dict(categories[1],int(sys.argv[1]),int(sys.argv[2]))
save_into_pickle(output,query)
