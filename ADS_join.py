
# coding: utf-8

# In[119]:

import ads
import pandas as pd
import cPickle as pickle


# In[296]:

pkl_file = open('./results_arxiv_api/astro-phstart2000max1000.pkl','rb')
arXiv_dict=pickle.load(pkl_file)


# In[297]:

arXiv_dict = pickle.load(file('./results_arxiv_api/astro-phstart2000max1000.pkl'))


# In[ ]:

def create_df(papers_list):
    return pd.DataFrame({'Title':[foo.title for foo in papers_list],
                  'Author':[foo.author for foo in papers_list],
                  'Citation_count':[foo.citation_count for foo in papers_list],
                  'Year':[foo.year for foo in papers_list],
                  'Pub':[foo.pub for foo in papers_list]})


# In[272]:

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


# In[273]:

df = pd.DataFrame()
for i,key in enumerate(arXiv_dict.keys()):
    pages,figures = search_comments(arXiv_dict[key]['comment'])
    try:
        ads_paper = list(ads.query(title=str(arXiv_dict[key]['title'])))
        if len(ads_paper)==1:
            new_row = pd.DataFrame({'Title':[ads_paper[0].title],                          'Author':[ads_paper[0].author],                          'Citation_count':[ads_paper[0].citation_count],                          'Year':[ads_paper[0].year],                          'Pub':[ads_paper[0].pub],                          'Pages':[pages],'Figures':[figures]})
        else:
            print i,'key',key,'has multiple query returns'
        df = df.append(new_row)
    except:
        continue
#    except error:
#       continue


# In[282]:

df.plot(x='Pages',y='Citation_count',kind='scatter')

