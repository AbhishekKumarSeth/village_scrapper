import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import time



def get_html_from_url(url):
    res = requests.get(url)
    return res



def get_link_from_html_content(html_content):
    soup = BeautifulSoup(html_content, features="lxml")
    links = soup.find_all('a')
    return links
	
	
res = get_html_from_url('https://vlist.in/')
print(res.status_code)

state_html = res.content

state_links = get_link_from_html_content(state_html)

state_list = []
for state_link in state_links:
    state_name = state_link.contents[0]
    state_link = state_link.get('href')
    
    state_info = {
        "state_name": state_name,
        "state_link":state_name,
    }
    
    state_list.append(state_info)
    
state_df = pd.DataFrame(state_list)
state_df.to_csv('state_list.csv')


village_list = []
sub_dist_list = []
dist_list = []
for state_link in state_links[4:]:
    state_name = state_link.contents[0]
    state_link = state_link.get('href')
    
    time.sleep(5)
    
    dist_res = get_html_from_url('https://vlist.in/' + state_link)
    dist_html = dist_res.content
    
    dist_links = get_link_from_html_content(dist_html)
    for dist_link in dist_links[1:-1]:
        dist_name = dist_link.contents[0]
        dist_link = dist_link.get('href')
        
        dist_info = {
            "state_name": state_name,
            "dist_name":dist_name,
            "dist_link":dist_link
        }
        
        dist_list.append(dist_info)
        
        
        time.sleep(4)
        
        sub_dist_res = get_html_from_url('https://vlist.in/' + dist_link)
        sub_dist_html = sub_dist_res.content
        
        sub_dist_links = get_link_from_html_content(sub_dist_html)
        
        for sub_dist_link in sub_dist_links[2:-1]:
            sub_dist_name = sub_dist_link.contents[0]
            sub_dist_link = sub_dist_link.get('href')
            
            
            sub_dist_info = {
                "state_name": state_name,
                "dist_name":dist_name,
                "sub_dist_name":sub_dist_name
            }
            
            sub_dist_list.append(sub_dist_info)
            
            
            time.sleep(4)
            
            village_res = get_html_from_url('https://vlist.in/' + sub_dist_link)
            village_html = village_res.content
            
            village_soup = BeautifulSoup(village_html, features="lxml")
            village_trs = village_soup.find_all('tr')


            for village_tr in village_trs[1:]:
                village_tds =village_tr.find_all('td')

                village_name = village_tds[1].get_text()
                village_code = village_tds[2].get_text()
            
                village_info = {
                    "state_name": state_name,
                    "dist_name":dist_name,
                    "sub_dist_name":sub_dist_name,
                    "village_name":village_name,
                    "village_code":village_code
                }
                
                village_list.append(village_info)
    

    dist_df=pd.DataFrame(dist_list)
    dist_df.to_csv(state_name+'_dist_list.csv')

    sub_dist_df = pd.DataFrame(sub_dist_list)
    sub_dist_df.to_csv(state_name+'_sub_dist_list.csv')

    village_df = pd.DataFrame(village_list)
    village_df.to_csv(state_name+'_village_list.csv')