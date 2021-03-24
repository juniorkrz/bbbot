import sys, os
from time import time, sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BBBot:


    def __init__(self):
        self.total_votes = 0
        self.fails = 0
        self.url = 'https://gshow.globo.com/realities/bbb/bbb21/votacao/paredao-bbb21-vote-para-eliminar-carla-diaz-fiuk-ou-rodolffo-6c4bd3d7-da53-40a1-b77d-8436b1230ed9.ghtml'
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=globo") #Path to your chrome profile
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        if getattr(sys, 'frozen', False): 
            chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
            self.driver = webdriver.Chrome(chromedriver_path, options=options)
        else:
            self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(516, 645)
        self.driver.set_window_position(10, 10)
        self.driver.get(self.url)
        self.driver.execute_script("""
            var element = document.querySelector("#banner_votacao1");
            if (element)
                element.parentNode.removeChild(element);
            """)


    def vote(self):
        self.driver.execute_script("""
            var element = document.querySelector("#banner_votacao1");
            if (element)
                element.parentNode.removeChild(element);
            """)
        ac = webdriver.common.action_chains.ActionChains(self.driver)
        html = self.driver.find_element_by_tag_name('html')
        x, y = (95, 356)
        ac.move_to_element_with_offset(html, x, y)
        ac.click()
        ac.perform()

        sleep(1)
        for i in range(3):
            html.send_keys(Keys.HOME)
        ac = webdriver.common.action_chains.ActionChains(self.driver)
        html = self.driver.find_element_by_tag_name('html')
        x, y = (200, 656)
        ac.move_to_element_with_offset(html, x, y)
        ac.click()
        ac.perform()

        timeOut = time() + 3
        while time() < timeOut:
            btn_appears = False
            buttons = self.driver.find_elements_by_tag_name('button')
            for btn in buttons:
                if btn.text.lower() == 'votar novamente':
                    btn_appears = True
                    break
            if btn_appears:
                btn.click()
                self.total_votes += 1
                print(' [ BBBOT ] Votos computados: %s' % self.total_votes)
                for i in range(3):
                    html.send_keys(Keys.HOME)
                return True
            sleep(1)

        return False


    def vote_loop(self):
        while True:
            result = self.vote()
            if result == False:
                self.driver.refresh()
                sleep(2)


bot = BBBot()
os.system('cls')
start = input(' [ BBBOT ] Realize o login e pressione ENTER...')
print(' [ BBBOT ] Iniciando...')
bot.driver.get(bot.url)
sleep(1)
bot.vote_loop()