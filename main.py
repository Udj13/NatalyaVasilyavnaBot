import conf
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

from datetime import date
from datetime import timedelta

from transaction_class import Transaction
from storage import Storage

import telebot

# from xvfbwrapper import Xvfb

# Downloads new version: https://sites.google.com/a/chromium.org/chromedriver/downloads
USERNAME = conf.usr
PASSWORD = conf.pwd

debugMode = False


class Bank:
    today_as_string = ""
    yesterday_as_string = ""
    new_transactions = []

    def __init__(self):
        if not debugMode:
            self.vdisplay = Xvfb()
            self.vdisplay.start()

        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-setuid-sandbox")
        self.driver = webdriver.Chrome(conf.path_to_driver, options=self.chrome_options)

        self.set_date_variables()
        self.storage = Storage()

    def close(self):
        self.storage.close()
        self.driver.close()
        if not debugMode:
            self.vdisplay.stop()

    def login(self):
        self.driver.get(conf.path_to_site)
        time.sleep(5)
        self.driver.find_element_by_name("LG").send_keys(USERNAME)
        self.driver.find_element_by_name("PW").send_keys(PASSWORD)
        self.driver.find_element_by_id("SF").click()

    def set_date_variables(self):
        today = date.today()
        self.today_as_string = str(format(today.strftime('%d%m%Y')))
        # Yesterday date
        yesterday = today - timedelta(days=1)
        self.yesterday_as_string = format(yesterday.strftime('%d%m%Y'))

    def set_date_field(self):
        first_date = self.driver.find_element_by_id("FDATE0")
        first_date.send_keys(Keys.HOME)
        first_date.send_keys(self.yesterday_as_string)

        second_date = self.driver.find_element_by_id("FDATE1")
        second_date.send_keys(Keys.HOME)
        second_date.send_keys(self.today_as_string)

    def show_ip_transactions(self):
        self.set_date_field()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="selectMain"]/option[2]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="FormBody"]/table/tbody/tr[2]/td[4]/button[1]').click()

    def show_ooo_transactions(self):
        self.set_date_field()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="selectMain"]/option[1]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="FormBody"]/table/tbody/tr[2]/td[4]/button[1]').click()

    def read_all_transactions(self):
        self.new_transactions = []
        content = self.driver.find_elements_by_class_name('CB')
        for c in content:
            td_list = c.find_elements_by_tag_name('td')
            pp_num = td_list[1].text
            pp_name_of_client = td_list[3].text
            pp_inn = td_list[4].text
            pp_summ = td_list[7].text
            pp_info = td_list[8].text

            new_transacton = Transaction()
            new_transacton.pp_num = pp_num
            new_transacton.pp_name_of_client = pp_name_of_client
            new_transacton.pp_inn = pp_inn
            new_transacton.pp_summ = pp_summ
            new_transacton.pp_info = pp_info

            self.new_transactions.append(new_transacton)

    def read_and_send_total(self, text):
        content = self.driver.find_elements_by_id('HT')
        send_text = text + ": " + content[3].text
        bot.send_message(conf.total_chat_id, send_text)

    def filter_new_ip_transactions(self):
        self.new_transactions = self.storage.check_new_ip_transactions(bank.new_transactions)

    def filter_new_ooo_transactions(self):
        self.new_transactions = self.storage.check_new_ooo_transactions(bank.new_transactions)

    def send(self, text):
        if len(self.new_transactions) == 0:
            return

        bot.send_message(conf.chat_id, text)
        for t in self.new_transactions:
            send_text = t.pp_name_of_client + " (" + t.pp_inn + " )" + "\n" + t.pp_summ + "\n" + t.pp_info + "\n" + "пп " + t.pp_num
            bot.send_message(conf.chat_id, send_text)
            if t.pp_info.find(conf.filter_tag) != -1:   # раскидываем по чатикам
                bot.send_message(conf.altrnative_chat_id, send_text)
                bot.send_message(conf.chat_id, '💳')
            if t.pp_info.find("бонент") != -1:          # абонентка
                bot.send_message(conf.chat_id, '🛰')

        if len(self.new_transactions) > 0:
            bank.read_and_send_total(text)


try:
    bot = telebot.TeleBot(conf.key_api)

    bank = Bank()
    bank.login()
    time.sleep(2)

    bank.show_ip_transactions()
    time.sleep(2)
    bank.read_all_transactions()
    bank.filter_new_ip_transactions()
    bank.send("Организация 1")

    time.sleep(2)
    bank.show_ooo_transactions()
    time.sleep(2)
    bank.read_all_transactions()
    bank.filter_new_ooo_transactions()
    bank.send("организация 2")


finally:
    bank.close()
