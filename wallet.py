from ast import Try, keyword
from asyncore import write
from distutils.log import error
import os
from unittest import result
from selenium import webdriver
from time import sleep
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from threading import Lock
from selenium.webdriver.firefox.options import Options


def paste_keys(driver, keysssEl, text):
    os.system("echo %s| clip" % text.strip())
    keysssEl.send_keys(Keys.CONTROL, 'v')


def run_test(n, data, lock, handle):
    try:
        txt = data[n]
        print("dang chay luong %d --- %s", n, txt)
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument('--headless')
        # options.headless = True
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        driver = webdriver.Firefox(executable_path=r'.\geckodriver.exe', options=options)

        extension_path = r".\webextension@metamask.io.xpi"
 
        # using webdriver's install_addon API to install the downloaded Firefox extension
        driver.install_addon(extension_path, temporary=True)
        driver.implicitly_wait(0.6)
        driver.switch_to.window(driver.window_handles[1])

        wait = WebDriverWait(driver, 5)
        startEl = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/button')))
        driver.execute_script("arguments[0].click();", startEl)
        print("startE2")
        startE2 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]')))
        driver.execute_script("arguments[0].click();", startE2)
        print("importEl")
        importEl = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button')))
        driver.execute_script("arguments[0].click();", importEl)

        print("keysssEl")
        keysssEl = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="import-srp__srp-word-0"]')))
        with lock:
            print("paste_keys")
            paste_keys(driver, keysssEl, txt)

        try:
            if len(driver.find_elements(By.CLASS_NAME, 'actionable-message__message'))>0:
                print('Successful Login')
                driver.quit()
                return True
        except:
            print("pass")
        print("send_keys")
        your_input1 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="password"]')))
        your_input1.send_keys('22222222')

        your_input2 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="confirm-password"]')))
        your_input2.send_keys('22222222')
        print("c1")
        c1 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="create-new-vault__terms-checkbox"]')))
        driver.execute_script("arguments[0].click();", c1)
        print("b1")
        b1 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button')))
        driver.execute_script("arguments[0].click();", b1)

        print("b11")
        b11 = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/button')))
        driver.execute_script("arguments[0].click();", b11)

        print("cop1")
        cop1 = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/button')))
        driver.execute_script("arguments[0].click();", cop1)
        print("cop2")

        cop2 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="popover-content"]/div[2]/button[1]')))
        driver.execute_script("arguments[0].click();", cop2)

        driver.switch_to.window(driver.window_handles[-1])
        addressE = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainaddress"]')))
        adressB = addressE.text
        driver.get(
            'https://polygonscan.com/token/0x5fef39b578deeefa4485a7e5944c7691677d5dd4?a=' + adressB)
        rs = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="ContentPlaceHolder1_divFilteredHolderBalance"]')))
        numberMobl = rs.text.replace("MOBL", "")
        numberMobl = numberMobl.replace("BALANCE", "")
        numberMobl = numberMobl.replace(" ", "")
        line = txt.rstrip('\n') + ' | ' + adressB.rstrip('\n') + \
            ' | ' + numberMobl.replace('\n', '')
        print('line', line)
        with lock:
            handle.write(line)
            handle.write("\n")
        driver.quit()
        return True
    except OSError as err:
        error = ("OS error: {0}".format(err))
        print(error)
        driver.quit()
        raise Exception(error)

    except ValueError:
        print("Could not convert data to an integer.")
        driver.quit()
        raise Exception(f'Could not convert data to an integer.')

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        driver.quit()
        raise Exception(err)


def retry(future, futures, executor, data, lock, handle):
    # get the associated data for the task
    dataRetry = futures[future]
    print('fur', dataRetry )

    # # submit the task again
    retry = executor.submit(run_test, dataRetry, data, lock, handle)
    # store so we can track the retries
    futures[retry] = dataRetry
    return dataRetry


def main():
    data = []

    with open(u'D:\Coin\checkKey.txt', 'r') as infile:  # Open file for read
        for line in infile:  # Iterate Each line
            line = line.strip()  # Strip leading and trailing space
            if line:  # Check if line is empty
                data.append(line)  # Append repo name to list.


    if os.path.exists("D:\Coin\checkWallet.txt"):
        os.remove("D:\Coin\checkWallet.txt")
    else:
        print("The file does not exist")

    completed = 0
    with open("D:\Coin\checkWallet.txt",  'a') as handle:
        lock = Lock()
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = {executor.submit(run_test, n, data, lock, handle):n for n in range(len(data))}
            
            while completed < len(data):
                for future in as_completed(futures):
                    if future.exception():
                        # retry the task
                        dataRetry = retry(future, futures, executor, data, lock, handle)
                        # report the failure
                        print(f'Failure, retrying {dataRetry}')
                    else:
                        completed += 1
                    futures.pop(future)
    print('Done.')

# entry point
if __name__ == '__main__':
    main()
