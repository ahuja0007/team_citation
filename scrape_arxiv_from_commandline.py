from arxiv_scraper import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", "--category", dest="category",
                  help="choose a category from ['hep-th','astro-ph']",default='astro-ph' )
parser.add_option("-s", "--start",
                   dest="start", default=0,type=int,
                  help="specify the starting position")
parser.add_option("-m","--max", dest="max_number",type=int,help="specify the max number of results",default=1)
(options, args) = parser.parse_args()

print "Working with params: ", options.category,options.start,options.max_number
output,query=scrape_arxiv_api_convert_to_dict(options.category,options.start ,options.max_number)
save_into_pickle(output,query)
