import urllib,time
from bs4 import BeautifulSoup
import pickle

"""Parse the results for a single paper"""
def parse_data_from_arxiv_api(soup):
    output={}
    try:
        output['query']=soup.title.get_text()
        output['title']=soup.find_all('title')[-1].get_text() #this may be done better?
        output['id']=soup.id.get_text()
        output['authors']=[a.get_text().strip('\n') for a in soup.find_all('author')]
        output['published']=soup.published.get_text()
        output['updated']=soup.updated.get_text()
        output['summary']=soup.summary.get_text()
        output['comment']=soup.find('arxiv:comment').get_text() 
        output['href']=soup.find_all('link')[-1]['href']
        
    except Exception as e:
	 return False
    return output


"""Scrape Arxiv and return a dictionary of dictionaries(each sub dictionary is a paper)"""
def scrape_arxiv_api_convert_to_dict(category,start,max_number): 
        papers_scraped={}
        url = 'http://export.arxiv.org/api/query?search_query=all:%s&start=%s&max_results=%s&sortBy=submittedDate&sortOrder=ascending'%(category,start,max_number)
        try:
            data = urllib.urlopen(url).read()
            soup=BeautifulSoup(data)
        except:
            print "cannot contact arxiv"
            
        entries=[e for e in soup.find_all('entry')]
        for entry in entries:
            parsed_data=parse_data_from_arxiv_api(entry)
            if parsed_data:
            	papers_scraped[parsed_data['id']]=parsed_data
        return papers_scraped,category+'start'+str(start)+'max'+str(max_number)
    
def save_into_pickle(papers,query):
    try:
        fout = open('results_arxiv_api/'+query+'.pkl', 'wb')
    except Exception as e:
        print e
        print "Write failed"
        return 
    pickle.dump(papers,fout)
    
