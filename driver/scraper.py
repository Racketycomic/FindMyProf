from bs4 import BeautifulSoup
import re

def find_prof_name(html_list):
    prof_list = []
    for html in html_list:
        soup = BeautifulSoup(html,features='html.parser')
        professor_list = soup.find_all("a",{"class":"person-name"})
        for prof in professor_list:
            prof_list.append(prof.get_text(strip=True))
    return prof_list
    

def get_author_profile_link(html,className):
    soup = BeautifulSoup(html,features='html.parser')
    atag = soup.find_all("a",{"class":className},href=True)
    gscholar_link = atag[0]['href']
    pattern = r"^(https?:\/\/scholar\.google\.[a-z.]+\/)"
    print("link",gscholar_link)
    if re.match(pattern,gscholar_link):
        return gscholar_link
    else:
        return None

def get_paper_links(html,className):
    soup = BeautifulSoup(html,features='html.parser')
    atag = soup.find_all("a",{"class":className},href=True)
    return [a['href'] for a in atag]

def get_paper_description(html,descriptionId,titleClass):
    soup = BeautifulSoup(html,features='html.parser')
    description = soup.find("div",{"id":descriptionId})
    title = soup.find("a",{"class":titleClass},href=True)
    return { "description": description.text if description is not None else '',
            "title": title.text if title is not None else '',
            "paperLink":title['href'] if title is not None else ''}
    