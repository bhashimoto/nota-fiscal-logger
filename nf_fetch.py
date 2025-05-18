from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import datetime

def element_exists(driver, by, value):
    try:
        element = driver.find_element(by, value)
    except NoSuchElementException:
        return None
    return element




class NFFetcher:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)


    def get_nf_header_data(self) -> dict:
        block = self.driver.find_element(By.XPATH, '//*[@id="infos"]/div[1]/div/ul/li').text
        text = block.split('Emissão: ')[1]
        text = text.split(' ')[0]
        date_parts = text.split('/')
        date = datetime.date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))

        nf = block.split("Número: ")[1]
        nf = nf.split(" ")[0]

        series = block.split("Série: ")[1]
        series = series.split(" ")[0]

        ret = {
            "number": int(nf),
            "series": int(series),
            "issue_date": date,
            "cnpj": self.get_nf_cnpj()
        }
        return ret

    def get_nf_cnpj(self) -> str:
        cnpj = self.driver.find_element(By.XPATH, '//*[@id="conteudo"]/div[2]/div[2]').text
        cnpj = cnpj.split(' ')[1]
        return cnpj

    def fetch_nf(self, url) -> dict:
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located((By.ID, 'tabResult')))
        retrieved_data = {
            'header': self.get_nf_header_data(),
            'items':[],
        }

        curr_row = 1
        keep_running = True

        while keep_running:
            element = element_exists(self.driver, By.ID, f"Item + {curr_row}")
            if element is None:
                keep_running = False
            else:
                item_name = element.find_element(By.CLASS_NAME, 'txtTit').text
                valor_total_item = element.find_element(By.CLASS_NAME, 'valor').text
                
                retrieved_data['items'].append({'issue_date': retrieved_data['header']["issue_date"],'name': item_name, 'value': float(valor_total_item.replace(',', '.'))})

                curr_row += 1
        self.driver.close()
        return retrieved_data
