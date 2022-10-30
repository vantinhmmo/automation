from ast import Try
from lib2to3.pgen2 import driver
import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from threading import Lock
from selenium.webdriver.firefox.options import Options
import time


def paste_keys(driver, keysssEl, text):
    os.system("echo %s| clip" % text.strip())
    keysssEl.send_keys(Keys.CONTROL, 'v')

def confirmApprovalFromMetamask(driver, EXTENSION_ID):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    wait = WebDriverWait(driver, 15)
    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    # confirm approval from metamask
    confirm1 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div/div[2]/div/div[3]/div[2]/button[2]')))
    driver.execute_script("arguments[0].click();", confirm1)

    confirm2 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]')))
    driver.execute_script("arguments[0].click();", confirm2)

    print("Approval transaction confirmed")
    # switch to dafi
    print(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)


def check_link(driver, wait):
    print('check_links')
    likeCheck = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, 'chakra-link')))
    like = driver.find_elements(By.CLASS_NAME, 'chakra-link')
    links = []
    for x in range(0, len(like)):
        if "New" in like[x].text and "3" in like[x].text:
            links.append(like[x].get_attribute('href'))
    return links


def clickDaily(driver, wait):
    like = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, 'Earn_daily-box__4IIlc')))
    like = driver.find_elements(By.CLASS_NAME, 'Earn_daily-box__4IIlc')
    for x in range(0, len(like)):
        sleep(0.3)
        like[x].click()


def setUpWallet(txt, driver, lock, n):
    print('set up wallet', n)
    wait = WebDriverWait(driver, 10)
    startEl = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/button')))
    startEl.click()

    startE2 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]')))
    startE2.click()

    importEl = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button')))
 
    importEl.click()
    keysssEl = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="import-srp__srp-word-0"]')))
    with lock:
        paste_keys(driver, keysssEl, txt)
    sleep(1)
    try:
        ElMess = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/div[1]/div[4]/div')
        if ElMess.text == 'Invalid Secret Recovery Phrase' or ElMess.text == 'Secret Recovery Phrases contain 12, 15, 18, 21, or 24 words':
            print('Fail 12 key', txt)
            clearBrowser(driver)
            return False
    except:
        pass
    your_input1 = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="password"]')))
    your_input1.send_keys('22222222')

    your_input2 = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="confirm-password"]')))
    your_input2.send_keys('22222222')

    c1 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="create-new-vault__terms-checkbox"]')))
    c1.click()

    b1 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button')))
    b1.click()

    completedWalletSetup = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div/div[2]/div/div/button')))
    completedWalletSetup.click()
    print('set up wallet end', n)
    return True

def taskMobula(driver, n):
    print('start task mobula', n)
    currentUrl = driver.current_url
    extensionId = currentUrl.split('/')[2]
    wait = WebDriverWait(driver, 10)
    driver.get("https://mobula.fi/earn")
    mb1 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div[2]/div/div/div[3]/div[2]/button[1]')))
    mb1.click()

    metaBtn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div[2]/div/div/div[3]/div[6]/button[1]')))
    metaBtn.click()

    confirmApprovalFromMetamask(driver, extensionId)
    clickDaily(driver, wait)
    links = check_link(driver, wait)
    for link in links:
        driver.get(link)
        sleep(2)
        driver.back()
        sleep(1)
        driver.refresh()
        sleep(1)
    
    # mbss23232 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[4]/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[2]/button')))
    # mbss23232.click()
    # sleep(2)
    print('End------ task mobula', n)

def setupWebDriver():
    print('set up webdriver')
    Options = webdriver.ChromeOptions()
    path = "./metamask-chrome-10.21.0.zip"
    Options.add_extension(path)
    Options.add_argument("--window-size=800x600")
    Options.add_experimental_option("useAutomationExtension", False)
    Options.add_argument("start-maximized")
    Options.add_argument("disable-infobars")
    Options.add_argument('--no-sandbox')
    Options.add_argument('--disable-application-cache')
    Options.add_argument('--disable-gpu')
    Options.add_argument("--disable-dev-shm-usage")
    Options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=Options)
    sleep(2)
    print('set up webdriver end')
    return driver

def clearBrowser(driver):
    driver.close()
    driver.quit()

def run_test(n, data, lock):
    try:
        txt = data[n]
        print("dang chay luong %d --- %s", n, txt)
        driver = setupWebDriver()
        driver.switch_to.window(driver.window_handles[0])
        if setUpWallet(txt, driver, lock, n) == True:
            pass
        else:
            clearBrowser(driver)
            return True
        taskMobula(driver, n)
        clearBrowser(driver)
        return True
    except OSError as err:
        error = ("OS error: {0}".format(err))
        print(error)
        clearBrowser(driver)
        raise Exception(error)

    except ValueError:
        print("Could not convert data to an integer.")
        clearBrowser(driver)
        raise Exception(f'Could not convert data to an integer.')

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        clearBrowser(driver)
        raise Exception(err)


def retry(future, futures, executor, data, lock):
    # get the associated data for the task
    dataRetry = futures[future]
    print('fur', dataRetry)

    # # submit the task again
    retry = executor.submit(run_test, dataRetry, data, lock)
    # store so we can track the retries
    futures[retry] = dataRetry
    return dataRetry


def main():
    data = []
    with open(u'D:\Coin\AutoKey\Run.txt', 'r') as infile:  # Open file for read
        for line in infile:  # Iterate Each line
            line = line.strip()  # Strip leading and trailing space
            if line:  # Check if line is empty
                data.append(line)  # Append repo name to list.

    completed = 0
    lock = Lock()
    with ThreadPoolExecutor(max_workers=7) as executor:
        futures = {}
        for n in range(450, 850):
            sleep(2)
            future = executor.submit(run_test, n, data, lock)
            futures[future] = n
        while completed < 400:
            print('total completed', completed)
            for future in as_completed(futures):
                try:
                    if future.exception():
                        # retry the task
                        dataRetry = retry(future, futures, executor, data, lock)
                        # report the failure
                        print(f'Failure, retrying {dataRetry}')
                    else:
                        completed += 1
                        print('completed', future.result())
                    futures.pop(future)
                except:
                    print("some error")
        print('Done.')


# entry point
if __name__ == '__main__':
    main()
