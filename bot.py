from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scraper import find_prof_name,get_author_profile_link,get_paper_links,get_paper_description
import time 
from selenium.webdriver.chrome.options import Options



class bot:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--disable-dev-shm-usage") 
        self.options.add_experimental_option('useAutomationExtension', False) 
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=self.options)


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
        self.driver.quit()
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
        
        # try:
        #     element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, self.waitEle)))
        # except:
        #     print("Element not found")
        #     # self.driver.quit()
        # finally:
        btn = self.driver.find_element(By.CSS_SELECTOR,"button[data-id='next']")
        self.driver.execute_script("arguments[0].click()",btn)
            

class scholar_bot(bot):
    
    def __init__(self,google,gscholar,fn,ln):
        super().__init__()
        self.url =google
        self.gscholar = gscholar
        self.searchbox = "APjFqb"
        self.atag = "zReHs"
        self.showmoreBtn = "gsc_bpf_more"
        self.paperLink = "gsc_a_at"
        self.descriptionId = "gsc_oci_descr"
        self.titleClass = "gsc_oci_title_link"
        self.fn = fn
        self.ln = ln
        
        
    def get_single_prof_Detail(self):
        gscholar_link = self.navigate_search_page()
        self.driver.get(gscholar_link)
        time.sleep(2)
        self.check_show_more()
        paper_list = get_paper_links(self.driver.page_source,self.paperLink)
        self.get_paper_description(paper_list)
        
        
        
    
    def navigate_search_page(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        searchbox = self.driver.find_element(By.ID,self.searchbox)
        searchbox.send_keys(f"{self.fn} {self.ln} Arizona State University Google Scholar")
        searchbox.send_keys(Keys.RETURN)
        time.sleep(1)
        gscholar_link = get_author_profile_link(self.driver.page_source,self.atag)
        return gscholar_link
        
    def check_show_more(self):
        while True:
            shw_more = self.driver.find_element(By.ID,self.showmoreBtn)
            print(shw_more.is_enabled())
            if shw_more.is_enabled():
                shw_more.click()
                time.sleep(1)
            else:
                break
            
    def get_paper_description(self,paper_list):
        p_list = []
        for paper in paper_list:
            self.driver.get(self.gscholar+paper)
            time.sleep(1)
            paper_Det = get_paper_description(self.driver.page_source,self.descriptionId,self.titleClass)
            print(paper_Det)
            p_list.append(paper_Det)
        
        
    def testground(self):
        self.driver.get('https://scholar.google.com.co/citations?user=J-CWgIkAAAAJ&hl=vi')
        self.check_show_more()
        get_paper_links(self.driver.page_source,self.paperLink)
