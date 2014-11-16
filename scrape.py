from arxiv_scraper import *
import sys
categories=['hep-th','astro-ph']
output,query=scrape_arxiv_api_convert_to_dict(categories[1],int(sys.argv[1]),int(sys.argv[2]))
keys=output.keys()
output[keys[1]] #example for the data of one paper
save_into_pickle(output,query)
#pkl_file = open('results_arxiv_api/'+query+'.pkl', 'rb')
#recovered_pickle=pickle.load(pkl_file)
#recovered_pickle[output.keys()[1]]
