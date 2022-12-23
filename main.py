import selenium
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from latest_user_agents import get_latest_user_agents


def write_thread(
        driver, server: str, board: str, thread: str,
        body: str, name: str = None, mail: str = None
) -> (bool, Optional[str]):
    url = f"https://{server}.5ch.net/test/read.cgi/{board}/{thread}/l50"

    # TODO: エラー処理
    driver.get(url)

    # 要素に値を詰める
    elem = driver.find_element(By.XPATH, '//textarea[@name="MESSAGE"]')
    elem.send_keys(body)
    if name is not None:
        elem = driver.find_element(By.XPATH, '//input[@name="FROM"]')
        elem.send_keys(name)
    if mail is not None:
        elem = driver.find_element(By.XPATH, '//input[@name="mail"]')
        elem.send_keys(mail)

    # 書きこみボタンを押す
    elem = driver.find_element(By.XPATH, '//input[@name="submit"]')
    elem.click()

    # Cookieをセットしてない場合は承諾ボタンを押す
    if "書きこみ＆クッキー確認" in driver.page_source:
        elem = driver.find_element(By.XPATH, '//input[@name="submit"]')
        elem.click()

    if driver.title == "ＥＲＲＯＲ！":
        elem = driver.find_element(By.XPATH, '/html/body/font[1]/b')
        return False, elem.text
    else:
        return True, None


def setup_driver():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/99.0.1150.36'
    # ua_list = get_latest_user_agents()
    # ua = ""
    # for ua_ in ua_list:
    #     if "Windows" in ua_ and "Chrome" in ua_:
    #         ua = ua_
    #         break

    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=' + ua)

    return webdriver.Chrome(chrome_options=options)


if __name__ == '__main__':
    driver = setup_driver()
    print(write_thread(driver, 'mi', 'news4vip', '1671786885', '書きこみてすつ', '>>1', 'mail address'))
