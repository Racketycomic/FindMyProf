from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from mongo_driver.mongo_driver import mongo_bot_helper
from driver.scraper import find_prof_name, get_author_profile_link, get_paper_description, get_paper_links
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random 


class bot:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        # self.options.add_experimental_option("detach",True)
        self.options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=self.options)
        self.mongoClient = mongo_bot_helper()
        
        

    def initiate(self):
        self.driver = webdriver.Chrome(options=self.options)

    def teardown(self):
        self.driver.quit()


class prof_bot(bot):
    def __init__(self):
        super().__init__()

        self.next_button_css = "button[aria-label='Next Page']"
        self.waitEle = "person-name"
        


    def get_prof_site(self,URL):
        self.driver.get(URL)
        self.driver.maximize_window()
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, self.waitEle)))
        except:
            print("Element not found")
            self.driver.quit()
        finally:
            h_list = []
            while True:
                print(len(h_list))
                src,status = self.go_next_page()
                h_list.append(src)
                if status:
                    self.click_button(self.next_button_css)
                else:
                    break
        prof_list = find_prof_name(h_list)
        prof_list = [{"prof_name":p} for p in prof_list]
        self.mongoClient.insert_prof_names(prof_list)
        self.teardown()
        return prof_list
    

    def click_button(self,xpath):
        btn = self.driver.find_element(By.CSS_SELECTOR,xpath)
        print("Inside click button")
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, self.waitEle)))
        except:
            print("Element not found")
            self.driver.quit()
        finally:
            self.driver.execute_script("arguments[0].click()",btn)


    def go_next_page(self):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, self.waitEle)))
        except:
            print("Element not found")
            self.driver.quit()
        finally:
            next_button = self.driver.find_element(By.CSS_SELECTOR,self.next_button_css)
            print("Inside next page")
            if next_button.get_attribute('aria-disabled') == 'false':
                return (self.driver.page_source,True)
            else:
                return (self.driver.page_source,False)

    def testground(self,url):
        self.driver.get(url)
        self.driver.maximize_window()
        btn = self.driver.find_element(By.CSS_SELECTOR,"button[data-id='next']")
        self.driver.execute_script("arguments[0].click()",btn)


class scholar_bot(bot):

    def __init__(self,google,gscholar,mc=None):
        super().__init__()
        self.google =google
        self.gscholar = gscholar
        self.searchbox = "APjFqb"
        self.atag = "zReHs"
        self.showmoreBtn = "gsc_bpf_more"
        self.paperLink = "gsc_a_at"
        self.descriptionId = "gsc_oci_descr"
        self.titleClass = "gsc_oci_title_link"
        if mc is not None:
            self.mongoClient = mc

    
    
    def insert_paper_links(self):
        prof_list = self.mongoClient.get_prof_list()
        print("Inside insert",prof_list)
        for prof in prof_list:
            fn,ln = prof['prof_name'].split(' ')
            paper_links = self.get_paper_list(fn,ln)
            if paper_links is not None:
                paper_list =[{"professor_name":prof['prof_name'],"paper":p,"pid":prof['_id']} for p in paper_links]
                self.mongoClient.insert_papers(paper_list)
            self.teardown()
            self.initiate()
        self.mongoClient.client.close()

    def get_paper_list(self,fn,ln):
        print("Insert get paper")
        gscholar_link = self.navigate_search_page(fn,ln)
        if gscholar_link is not None:
            return self.get_papers_by_authorLink(gscholar_link)
        else:
            print("Professor not Found")




    def navigate_search_page(self,fn,ln):
        self.driver.get(self.google)
        self.driver.maximize_window()
        searchbox = self.driver.find_element(By.ID,self.searchbox)
        searchbox.send_keys(f"{fn} {ln} Arizona State University Google Scholar")
        searchbox.send_keys(Keys.RETURN)
        time.sleep(4)
        gscholar_link = get_author_profile_link(self.driver.page_source,self.atag)
        return gscholar_link

    def check_show_more(self):
        try:
            ele = WebDriverWait(self.driver,10).until(EC.presence_of_element_located(By.ID,self.showmoreBtn))
        except:
            print("Element not found")
        finally:
            while True:
                shw_more = self.driver.find_element(By.ID,self.showmoreBtn)
                print(shw_more.is_enabled())
                if shw_more.is_enabled():
                    shw_more.click()
                    time.sleep(1)
                else:
                    break

    def get_paper_details(self,paper_list):
        print('length of papers:', len(paper_list))
        print(paper_list)
        for paper in paper_list:
            gscholar_link = self.gscholar+paper["paper"]
            self.driver.get(gscholar_link)
            time.sleep(random.uniform(25,50))
            paper_Det = get_paper_description(self.driver.page_source,self.descriptionId,self.titleClass)
            paper_Det['gscholar_link'] = gscholar_link
            self.mongoClient.insert_paper_by_prof(paper["pid"],paper_Det)
            self.mongoClient.delete_paper_from_pool(paper["_id"])


    def random_paper_insert(self):
        paper_list = self.mongoClient.sample_document(5,'papers')
        if len(paper_list) == 0:
            return False
        self.get_paper_details(paper_list)
        return True
        
    def get_papers_by_authorLink(self,authorLink):
        self.driver.get(authorLink)
        time.sleep(1)
        self.check_show_more()
        paper_list = get_paper_links(self.driver.page_source,self.paperLink)
        return paper_list
        
    def testground(self):
        self.driver.get('https://scholar.google.com.co/citations?user=J-CWgIkAAAAJ&hl=vi')
        self.check_show_more()
        get_paper_links(self.driver.page_source,self.paperLink)