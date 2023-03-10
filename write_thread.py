from typing import Optional

# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
    elem = WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((
            By.XPATH, '//input[@name="submit"]'
        ))
    )
    # ref: https://office54.net/python/scraping/selenium-click-exception
    driver.execute_script("arguments[0].click();", elem)

    # Cookieをセットしてない場合は承諾ボタンを押す
    if "書きこみ＆クッキー確認" in driver.page_source:
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((
                By.XPATH, '//input[@name="submit"]'
            ))
        )
        elem.click()

    if driver.title == "ＥＲＲＯＲ！":
        elem = driver.find_element(By.XPATH, '/html/body/font[1]/b')
        return False, elem.text
    else:
        driver.get("https://www.google.com")
        return True, None


def interceptor_(req):
    if req.path.endswith(('.png', '.jpg', '.gif')):
        req.abort()


def setup_driver():
    ua_list = get_latest_user_agents()
    ua = ""
    for ua_ in ua_list:
        if "Windows" in ua_ and "Chrome" in ua_:
            ua = ua_
            break

    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=' + ua)
    # ref: https://stackoverflow.com/questions/73930313/python-selenium-button-click-causes-browser-console-error
    options.add_argument('--disable-blink-features=AutomationControlled')
    # ref: https://sushiringblog.com/chromedriver-error
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")
    # ref: https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
    options.add_argument('--disable-dev-shm-usage')
    # ref: https://groups.google.com/a/chromium.org/g/headless-dev/c/f_tQUs__Yqw
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--mute-audio")
    options.add_argument("--no-first-run")
    options.add_argument("--safebrowsing-disable-auto-update")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-certificate-errors-spki-list")
    # ref: https://stackoverflow.com/questions/48773031/how-to-prevent-chrome-headless-from-loading-images
    options.add_argument("--blink-settings=imagesEnabled=false")

    # ref: https://stackoverflow.com/questions/46322165/dont-wait-for-a-page-to-load-using-selenium-in-python/46339092#46339092
    caps = DesiredCapabilities().CHROME
    caps['pageLoadStrategy'] = 'eager'

    driver_ = webdriver.Chrome(options=options, desired_capabilities=caps)
    # ref: https://www.zacoding.com/post/selenium-ad-block/
    # driver_.request_interceptor = interceptor_

    return driver_


if __name__ == '__main__':
    import time

    driver = setup_driver()
    print(write_thread(driver, 'mi', 'news4vip', '1671786885', 'Cookieのテスト1', '>>1', 'mail address'))
    time.sleep(60)
    print(write_thread(driver, 'mi', 'news4vip', '1671786885', 'Cookieのテスト2', '>>1', 'mail address'))
