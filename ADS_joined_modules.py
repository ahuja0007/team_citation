import ads
import pandas as pd
import cPickle as pickle
import numpy as np

"""Parse through ArXiv comments to extract page and figure numbers"""
def search_comments(comments_string,page_numbers=np.NAN,figure_numbers=np.NAN):
    comments = comments_string.split(' ')
    page_number_ind = -1
    figure_number_ind = -1
    for i,com in enumerate(comments):
        if com.find('pages')!=-1:
            page_number_ind = i-1
        if com.find('figures')!=-1:
            figure_number_ind = i-1
    if page_number_ind!=-1:
        if comments[page_number_ind].isdigit():
            page_numbers = int(comments[page_number_ind])
    if figure_number_ind!=-1:
        if comments[figure_number_ind].isdigit():
            figure_numbers = int(comments[figure_number_ind])
        
        
    return [page_numbers,figure_numbers]


"""Generate dataframe aggregating all the data, querying ADS by matching paper title with ArXiv"""
def generate_df(arXiv_dict):
    
    df = pd.DataFrame()

    for i,key in enumerate(arXiv_dict.keys()):
        pages,figures = search_comments(arXiv_dict[key]['comment'])

        try:
            ads_paper = list(ads.query(title=str(arXiv_dict[key]['title'])))
            if len(ads_paper)==1:  
                new_row = pd.DataFrame({'Arxiv_key': [arXiv_dict.keys()[i]], 'Title':[ads_paper[0].title],
                                            'Author':[ads_paper[0].author],
                                            'Citation_count':[ads_paper[0].citation_count],
                                            'Year':[ads_paper[0].year],'Pub':[ads_paper[0].pub],
                                            'Pages':[pages],'Figures':[figures]})
                df = df.append(new_row)
        except:
            continue

    return df