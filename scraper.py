from bs4 import BeautifulSoup


def find_prof_name(html_list):
    prof_list = []
    for html in html_list:
        soup = BeautifulSoup(html,features='html.parser')
        professor_list = soup.find_all("a",{"class":"person-name"})
        for prof in professor_list:
            prof_list.append(prof.get_text(strip=True))
    return prof_list
    
def check_if_next_is_disabled(html):
    soup = BeautifulSoup(html,features='html.parser')
    button = soup.find_all("button",{"aria-label":"Next Page"})
    