from time import sleep

from colorama import Fore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def login_test(driver):
    sleep(4)
    driver.find_element(By.ID, "navbarLogin").click()
    sleep(5)
    driver.find_element(By.ID, "userInput").send_keys("receptionuser")
    driver.find_element(By.ID, "passwordInput").send_keys("admin")
    sleep(5)
    driver.find_element(By.CSS_SELECTOR, ".login_button").click()

    try:
        driver.find_element(By.ID, "navbarLogout")
        print(Fore.GREEN + "Login system working succesfully")
    except:
        print(Fore.RED + "Login system failed")


def check_reception_view(driver):
    try:
        driver.find_element(By.ID, "navbarRecepcio")
        print(Fore.GREEN + "Reception view working succesfully")
    except:
        print(Fore.RED + "Reception view failed")


def logout_test(driver):
    driver.find_element(By.ID, "navbarLogout").click()
    sleep(5)
    try:
        driver.find_element(By.ID, "navbarLogin")
        print(Fore.GREEN + "Logout system working succesfully")
    except:
        print(Fore.RED + "Logout system failed")


def run_tests():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/")
    login_test(driver)
    check_reception_view(driver)
    sleep(5)
    logout_test(driver)
    sleep(2)
    driver.close()


if __name__ == '__main__':
    run_tests()
