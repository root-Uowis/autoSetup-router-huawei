#!/opt/homebrew/bin/python3
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)
    # driver.set_window_size(1920, 1080)
    driver.get('http://192.168.8.1')
    time.sleep(8)
    start = time.time()
    login = driver.find_element(By.ID, "login_password")
    login.send_keys(sys.argv[1])
    login.send_keys(Keys.ENTER)
    time.sleep(3)

    def LoginAndResetMdp():
        PopUpAgree = driver.find_elements(By.ID, "privacyAgreen")
        flag = 0
        while PopUpAgree != []:
            flag += 1
            if flag == 3:
                break
            else:
                for e in PopUpAgree:
                    e.click()
                    time.sleep(1)

        isVisibleAgreeUpg = driver.find_element(
            By.ID, "guide_agreeUpg_btn").is_displayed()

        if isVisibleAgreeUpg:
            driver.find_element(By.ID, "guide_agreeUpg_btn").click()

        time.sleep(1)

        isVisibleNextWifi = driver.find_element(
            By.ID, "guide_wifi_to_next").is_displayed()

        if isVisibleNextWifi:
            driver.find_element(By.ID, "guide_wifi_to_next").click()

        isVisibleNewPwd = driver.find_element(
            By.ID, "new_password").is_displayed()

        if isVisibleNewPwd:
            driver.find_element(By.ID, "new_password").send_keys("Password0")
            driver.find_element(By.ID, "guide_modify_password").click()

        time.sleep(5)

    def TurnOnRoaming():
        driver.get("http://192.168.8.1/html/content.html#mobileconnection")
        time.sleep(2)
        roamingSwitch = driver.find_element(By.ID, "data_roaming_switch")
        switchState = roamingSwitch.get_attribute('class')
        if switchState == "switch_off":
            roamingSwitch.click()
            time.sleep(2)
            driver.find_element(By.ID, "confirm_confirm").click()

    def TurnOffWifi():
        driver.get('http://192.168.8.1/html/content.html#wifieasy')
        time.sleep(2)

        newWifiDisplayed = driver.find_element(
            By.ID, "wifi_2g_switch").is_displayed()

        if newWifiDisplayed:
            wifiSwitch = driver.find_element(By.ID, "wifi_2g_switch")
            switchState = wifiSwitch.get_attribute('class')
            if switchState == "switch_on":
                wifiSwitch.click()
                time.sleep(2)
                driver.find_element(By.ID, "confirm_confirm").click()

        oldWifiDisplayed = driver.find_element(
            By.ID, "wifi_singlechip_switch").is_displayed()

        if oldWifiDisplayed:
            oldWifiSwitch = driver.find_element(
                By.ID, "wifi_singlechip_switch")
            oldWifiSwitchState = oldWifiSwitch.get_attribute('class')
            if oldWifiSwitchState == "switch_on":
                oldWifiSwitch.click()
                time.sleep(2)
                driver.find_element(By.ID, "confirm_confirm").click()

    def ChangeIpOfDhcp():
        driver.get('http://192.168.8.1/html/content.html#dhcp')
        time.sleep(2)
        byteString = "dhcp_gatewayip_byte{}"

        for x, i in zip(range(1, 5), range(2, 6)):
            byteFormatted = byteString.format(x)
            driver.find_element(By.ID, byteFormatted).clear()
            driver.find_element(By.ID, byteFormatted).send_keys(sys.argv[i])

        time.sleep(1)
        driver.find_element(By.ID, "dhcp_btn_save").click()
        driver.find_element(By.ID, "confirm_confirm").click()
        try:
            element_present = EC.visibility_of_element_located(
                (By.ID, 'login_password'))
            WebDriverWait(driver, 60).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            loginNewIp = driver.find_element(By.ID, "login_password")
            loginNewIp.send_keys("Password0")
            loginNewIp.send_keys(Keys.ENTER)

    def DisablePingWan():

        driver.get("http://" + newIP + "/html/content.html#firewallswitch")

        time.sleep(1)

        isVisibleOldWanPing = driver.find_elements(
            By.ID, "firewall_checkbox_firewallWanPortPingSwitch_label")

        if isVisibleOldWanPing != []:
            oldWanCheckBox = driver.find_element(
                By.ID, "firewall_checkbox_firewallWanPortPingSwitch_label")
            oldWanCheckBoxState = oldWanCheckBox.get_attribute('class')
            if "checked" in oldWanCheckBoxState:
                oldWanCheckBox.click()
                driver.find_element(By.ID, "firewall_apply_button").click()

        isVisibleWanPing = driver.find_elements(
            By.ID, "checkbox_firewallWanPortPingSwitch_label")

        if isVisibleWanPing != []:
            wanCheckBox = driver.find_element(
                By.ID, "checkbox_firewallWanPortPingSwitch_label")
            wanCheckBoxState = wanCheckBox.get_attribute('class')
            if "checked" in wanCheckBoxState:
                wanCheckBox.click()
                driver.find_element(By.ID, "firewall_apply_button").click()

    def TurnOnDMZ():
        stateDmz = driver.find_element(
            By.ID, "dmz_switch").get_attribute('class')
        if stateDmz == "switch_off":
            driver.find_element(By.ID, "dmz_switch").click()
            time.sleep(1)
            driver.find_element(By.ID, "macfilter_vendor_dmz").click()
            driver.find_element(
                By.ID, "macfilter_vendor_dmz_list_item_0").click()
            time.sleep(1)
            ip = str(sys.argv[2]) + '.' + str(sys.argv[3]) + \
                '.' + str(sys.argv[4]) + '.100'
            driver.find_element(By.ID, "dmz_ip_address").clear()
            driver.find_element(By.ID, "dmz_ip_address").send_keys(ip)
            driver.find_element(By.ID, "dmz_submit_btn").click()

    if sys.argv[1] != "Password0":
        LoginAndResetMdp()

    isVisibleWanSett = driver.find_element(
        By.ID, "menu_top_wanconfig").is_displayed()

    if isVisibleWanSett:
        TurnOnRoaming()

    time.sleep(2)

    isVisibleWifiSett = driver.find_element(
        By.ID, "menu_top_wifisettings").is_displayed()

    if isVisibleWifiSett:
        TurnOffWifi()

    time.sleep(2)

    isVisibleAdvanced = driver.find_element(
        By.ID, "menu_advanceset").is_displayed()

    if isVisibleAdvanced:
        ChangeIpOfDhcp()

    time.sleep(2)

    newIP = str(str(sys.argv[2]) + '.' + str(sys.argv[3]) +
                '.' + str(sys.argv[4]) + '.' + str(sys.argv[5]))

    if isVisibleAdvanced:
        DisablePingWan()

    time.sleep(2)

    driver.get("http://" + newIP + "/html/content.html#dmzsettings")

    time.sleep(2)

    isVisibleDmzSwitch = driver.find_element(
        By.ID, "dmz_switch").is_displayed()

    if isVisibleDmzSwitch:
        TurnOnDMZ()

    time.sleep(2)

    driver.get("http://" + newIP + "/html/content.html#sipalgsettings")

    time.sleep(2)

    isVisibleSipSwitch = driver.find_element(
        By.ID, "sip_switch").is_displayed()

    if isVisibleSipSwitch:
        stateSIP = driver.find_element(
            By.ID, "sip_switch").get_attribute('class')
        if stateSIP == "switch_on":
            driver.find_element(By.ID, "sip_switch").click()

    time.sleep(2)

    driver.get("http://" + newIP + "/html/content.html#deviceinformation")

    time.sleep(2)

    array = ["DeviceName", "SerialNumber", "Imei", "Imsi", "MacAddress1"]
    string = "di-{}"

    for x in array:
        stringFormatted = string.format(x)
        isVisible = driver.find_element(
            By.ID, stringFormatted).is_displayed()

        if isVisible:
            parentElement = driver.find_element(By.ID, stringFormatted)
            childElement = parentElement.find_element(By.XPATH, ".//*")
            value = childElement.get_attribute("innerHTML")
            print(x, ":", value)

    end = time.time()
    print("Setup finished in :", int(end - start), "seconds.")
