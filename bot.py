from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from scraper import find_prof_name

class bot:
    def __init__(self):
        self.driver = None
        self.next_button_css = "button[aria-label='Next Page']"
        
    def create_driver(self):
        self.driver = webdriver.Firefox()
    
    def get_prof_site(self,URL):
        self.driver.get(URL)
        self.driver.maximize_window()
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "person-name")))
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
        print("src",prof_list)         
            
    def click_button(self,xpath):
        btn = self.driver.find_element(By.CSS_SELECTOR,xpath)
        print("Inside click button")
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "person-name")))
        except:
            print("Element not found")
            self.driver.quit()
        finally:
            self.driver.execute_script("arguments[0].click()",btn)
            
            
    def go_next_page(self):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "person-name")))
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
        
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "person-name")))
        except:
            print("Element not found")
            self.driver.quit()
        finally:
            btn = self.driver.find_element(By.CSS_SELECTOR,"button[data-id='next']")
            self.driver.execute_script("arguments[0].click()",btn)