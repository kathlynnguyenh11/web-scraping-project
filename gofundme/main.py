from bs4 import BeautifulSoup 
import requests
#import re
import pandas as pd
from urllib.request import Request, urlopen

#Look up campaign
def get_gofundme():
    output={}

    base_url='https://www.gofundme.com/mvc.php?route=homepage_norma/search&term='
    keyword=input("Look up campaign by location, people, title: ")
    keyword=keyword.replace(' ','%20')
    search_url=base_url+keyword

    page = requests.get(search_url)
    soup = BeautifulSoup(page.text,'html.parser')
    
    #OUTPUT to show to users
    output=""
    
    #DATA to store in csv file
    data={
        'Title':[],
        'Location':[],
        'Progress':[],
        'Link':[],
    }
    
    for campaign in soup.find_all('div',attrs={'class':'react-campaign-tile-details'}):
        result={}
        result['Title']=campaign.find('div',attrs={'class':'fund-title truncate-single-line show-for-medium'}).text.strip() 
        title=result['Title']
        
        result['Location']=campaign.find('div',attrs={'class':'fund-item fund-location truncate-single-line'}).text.strip()
        location=result['Location']
        
        for prog in campaign.find_all('div',attrs={'class':'show-for-medium'}):
            if "raised" in prog.text:
                result['Progress']=prog.text.strip()
                progress=result['Progress']  
        
        result['Link']=campaign.find('a').get('href')
        link=result['Link']

        for res in result:
            output+=res
            output+="\t"
            output+=result[res]
            output+="\n"
        output+="\n===============#===============\n"
        
        data['Title'].append(title)
        data['Location'].append(location)
        data['Progress'].append(progress)
        data['Link'].append(link)
        table = pd.DataFrame(data, columns=['Title', 'Location', 'Progress', 'Link'])
        table.index = table.index + 1
        table.to_csv(f'gofundme.csv', sep=',', encoding='utf-8', index=False)
    
    return output

def get_successStories():
    output={}
    successUrl='https://www.gofundme.com/c/heroes'

    successPage=requests.get(successUrl)
    successSoup = BeautifulSoup(successPage.text,'html.parser')
    print(successSoup)
    if successPage.status_code == requests.codes.ok:
        print('Everything is cool!')
    else:
        print('no')
    for story in successSoup.find_all('div',attrs={'class':'story-card story-card-flip grid-x'}):
        result={}
        result['Title']=story.find('a',attrs={'class':'text-black'}).text.strip()
        print(result['Title']+'test')
        result['Description']=story.find('p',attrs={'class':'medium-gray mb2x text-small'}).text.strip()
        result['Link']='https://www.gofundme.com/f/'+story.find('a').get('href').text

        for res in result:
            output+=res
            output+="\t"
            output+=result[res]
            output+="\n"
            output+="\n===============#===============\n"
    return output
#Option board - prompts for user input
def board(opt):
    options={
        1: get_gofundme,
        2: get_successStories,
    }
    return options.get(opt,"nothing")()

#DRIVER        
if __name__ == "__main__": 
    print("1. Look up campaigns")
    print("2. Read Gofundme success stories")
    opt = int(input("Pick one option"))
    print(board(opt))