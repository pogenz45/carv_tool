from appium import webdriver
import asyncio
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_connection import AppiumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from loguru import logger
from simplegmail import Gmail
from simplegmail.query import construct_query
from bs4 import BeautifulSoup
import random
from random_username.generate import generate_username
import requests
import re
from appium.webdriver.common.appiumby import AppiumBy
import pyperclip

class CustomAppiumConnection(AppiumConnection):
    # Can add your own methods for the custom class
    pass

custom_executor = CustomAppiumConnection(remote_server_addr='http://127.0.0.1:4723/wd/hub')

options = XCUITestOptions().load_capabilities({
    "platformName": "Android",
    "platformVersion": "15",
    "automationName": "uiautomator2",
    "deviceName": "pixel_7",
    "udid": "emulator-5554",
    # "appPackage": "com.android.vending",
    # "appActivity": "com.android.vending.AssetBrowserActivity",
    "app": "/Users/vta45/Downloads/coin_tool/carv_tool/carv.apk"
})

async def get_mail(email):
    gmail = Gmail()
    query_params = {
        "recipient": email,
    }
    messages = gmail.get_messages(query=construct_query(query_params))
    soup = BeautifulSoup(messages[0].html, "html.parser")
    pattern = r'\b\d{6}\b'
    url = soup.find_all("td")
    string_code = url[1].text
    match = re.search(pattern, string_code)
    if match:
        verification_code = match.group(0)
        return verification_code
    else:
        print("Verification code not found.")
        return 
    
def check_driver_click(driver,element):
    try:
        if element.is_displayed():
            element.click()
        else:
            print(f"Element with ID '{element}' exists but is not visible.")
    except Exception as e:
        print(f"Element with ID '{element}' does not exist.")


async def run():
    driver = webdriver.Remote(custom_executor, options=options)
    # Download from chplay
    # driver.implicitly_wait(5)
    # driver.find_element(By.XPATH,"//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[2]").click()
    # driver.implicitly_wait(4)
    # driver.find_element(By.XPATH,"//android.widget.EditText").send_keys("carv")
    # driver.implicitly_wait(4)
    # driver.find_element(By.XPATH,"//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[2]").click()
    # driver.implicitly_wait(4)
    # path_item = "//android.widget.TextView[@content-desc='enter the data-to-earn era! own, control and monetize your data!']"
    # driver.find_element(By.XPATH,path_item).click()
    # driver.implicitly_wait(4)
    # driver.find_element(By.XPATH,"//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]/android.view.View[5]/android.widget.Button").click()
    # await asyncio.sleep(25)
    # driver.implicitly_wait(4)
    # driver.find_element(By.XPATH,'//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]/android.view.View[5]/android.widget.Button').click()

    # Get from apk
    await asyncio.sleep(5)
    driver.implicitly_wait(8)
    driver.find_element(AppiumBy.ID,"com.android.permissioncontroller:id/permission_allow_button").click()
    # driver.implicitly_wait(8)

    driver.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="Earn more SOUL"]/android.widget.ImageView').click()
    driver.implicitly_wait(8)
    await asyncio.sleep(2)
    driver.find_element(By.XPATH,"//android.widget.TextView[@text='Next']").click()
    logger.info("next1")
    driver.implicitly_wait(8)
    await asyncio.sleep(0.5)
    driver.find_element(By.XPATH,"//android.widget.TextView[@text='Next']").click()
    logger.info("next2")
    driver.implicitly_wait(8)
    await asyncio.sleep(0.5)
    driver.find_element(By.XPATH,'//android.widget.TextView[@text="Finish"]').click()
    logger.info("finish")

    # await asyncio.sleep(1)
    driver.find_element(By.XPATH,'//android.view.View[@content-desc="Profile"]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView').click()
    driver.implicitly_wait(8)
    await asyncio.sleep(1)
    driver.find_element(By.XPATH,'//android.view.ViewGroup[@content-desc="Email"]/android.view.ViewGroup').click()
    driver.implicitly_wait(8)
    await asyncio.sleep(1)
    usmeme = str(generate_username(1)[0])[:7] + str(random.randrange(1, 99999))
    email = f"{usmeme.strip()}@pogenz.xyz"
    driver.implicitly_wait(8)
    driver.find_element(By.XPATH,'//android.widget.EditText[@text="Email address"]').send_keys(email)
    driver.implicitly_wait(8)
    driver.find_element(By.XPATH,'//android.view.ViewGroup[@content-desc="Send Code"]').click()
    await asyncio.sleep(25)
    code_res = await get_mail(email)
    logger.info("Wait 30s to get code")
    # await asyncio.sleep(20)
    if not code_res:
        logger.info("error")
        return None
    try:
        logger.info(code_res)
        code = f"{code_res}".strip()
        await asyncio.sleep(0.5)
        driver.implicitly_wait(5)
        driver.find_element(AppiumBy.XPATH,'//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText[1]').send_keys(code[0])
        # await asyncio.sleep(0.5)
        driver.implicitly_wait(5)
        driver.find_element(AppiumBy.XPATH,'//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText[2]').send_keys(code[1])
        # await asyncio.sleep(0.5)
        driver.implicitly_wait(5)
        driver.find_element(AppiumBy.XPATH,'//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText[3]').send_keys(code[2])
        # await asyncio.sleep(0.5)
        driver.implicitly_wait(5)
        driver.find_element(AppiumBy.XPATH,'//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText[4]').send_keys(code[3])
        # await asyncio.sleep(0.5)
        driver.implicitly_wait(5)
        driver.find_element(AppiumBy.XPATH,'//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText[5]').send_keys(code[4])
        # await asyncio.sleep(0.5)
        driver.implicitly_wait(5)
        driver.find_element(AppiumBy.XPATH,'//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText[6]').send_keys(code[5])
        # await asyncio.sleep(0.5)
        driver.implicitly_wait(5)
        driver.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="Verify"]').click()
        await asyncio.sleep(3)
        driver.implicitly_wait(8)
        driver.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="Authorize"]').click()
        await asyncio.sleep(6)
        # driver.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="Earn more SOUL"]/android.widget.ImageView').click()
        # driver.implicitly_wait(8)
        # logger.info("click earn more soul")
        await asyncio.sleep(1)
        
        # driver.find_element(By.XPATH,"//android.widget.TextView[@text='Next']").click()
        # logger.info("next1")
        # driver.implicitly_wait(8)
        # await asyncio.sleep(0.5)
        # driver.find_element(By.XPATH,"//android.widget.TextView[@text='Next']").click()
        # logger.info("next2")
        # driver.implicitly_wait(8)
        # await asyncio.sleep(0.5)
        # driver.find_element(By.XPATH,'//android.widget.TextView[@text="Finish"]').click()
        # logger.info("finish")
        # await asyncio.sleep(2)
        # logger.info("next complete")
        ref_code = "3L3M2F"
        pyperclip.copy(ref_code)
        # await asyncio.sleep(1)
        # driver.find_element(By.XPATH,'(//android.widget.SeekBar[@content-desc="Bottom Sheet"])[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[1]').send_keys(ref_code[0])
        # driver.implicitly_wait(5)
        # # await asyncio.sleep(0.5)
        # driver.find_element(By.XPATH,'//android.widget.SeekBar[@content-desc="Bottom Sheet"])[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]').send_keys(ref_code[1])
        # driver.implicitly_wait(5)
        # # await asyncio.sleep(0.5)
        # driver.find_element(AppiumBy.XPATH,'(//android.widget.SeekBar[@content-desc="Bottom Sheet"])[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[3]').send_keys(ref_code[2])
        # driver.implicitly_wait(5)
        # # await asyncio.sleep(0.5)
        # driver.find_element(AppiumBy.XPATH,'(//android.widget.SeekBar[@content-desc="Bottom Sheet"])[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[4]').send_keys(ref_code[3])
        # driver.implicitly_wait(5)
        # # await asyncio.sleep(0.5)
        # driver.find_element(AppiumBy.XPATH,'(//android.widget.SeekBar[@content-desc="Bottom Sheet"])[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[5]').send_keys(ref_code[4])
        # driver.implicitly_wait(5)
        # # await asyncio.sleep(0.5)
        # driver.find_element(AppiumBy.XPATH,'(//android.widget.SeekBar[@content-desc="Bottom Sheet"])[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[6]').send_keys(ref_code[5])
        # driver.implicitly_wait(5)
        await asyncio.sleep(0.5)
        e3 = driver.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="Paste"]')
        check_driver_click(driver,e3)
        e4 = driver.find_element(By.XPATH,'//android.view.ViewGroup[@content-desc="Paste"]').click()
        check_driver_click(driver,e4)
        driver.implicitly_wait(8)
        await asyncio.sleep(0.5)
        submit = driver.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="Submit"]')
        driver.implicitly_wait(8)
        check_driver_click(driver,submit)
        # driver.find_element(AppiumBy.ID,"Submit").click()
        # driver.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="Submit"]').click()
        # driver.find_element(By.XPATH,'//android.view.ViewGroup[@content-desc="Submit"]').click()
        driver.implicitly_wait(8)
        logger.info("Ref success")
        
        
    except Exception as e:
        logger.error(f"encounter error: {e}")
        return None

async def main():
    await run()

if __name__ == "__main__":
    asyncio.run(main())
    






