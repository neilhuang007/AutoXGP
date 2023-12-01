import pathlib
import sys
import urllib

import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os, json, string, random
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import pyperclip

from multithreading.useragents import default_header_user_agent


#load proxies
#proxy_response = requests.get("https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=60&filterUpTime=90&country=US&speed=fast&protocols=socks4&anonymityLevel=elite")

def randomUsername(length=16):
    base_Str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    random_str = ''
    for i in range(length):
        random_str += base_Str[random.randint(0, (len(base_Str) - 1))]
    return random_str

def copy_text(text):
    pyperclip.copy(text)


def purchasecheck():
    try:
        success = driver.find_element(By.XPATH,
                                      '/html/body/reach-portal/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]/div[3]/a')
        success = int(success)
        if success == '<selenium.webdriver.remote.webelement.WebElement (session="9a245c8242c7806aae13821738d81698", element="23F5752506E09117C6B47DABC432C962_element_221")>':
            s = 1
        else:
            s = 2
    except NoSuchElementException:
        print('等待中......')
        s = 2
        return False


def purchase():
    try:
        time.sleep(3)
        join_button = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[3]/div/div/div/div[2]/div[5]/div[1]/div[2]/section/div/div/ul/li[1]/div/div[1]/div[2]/a").click()
    except NoSuchElementException:
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, "a[data-bi-source='CFQ7TTC0KGQ8']").click()

#random proxy generator
def RandomProxy():
    proxytemp = ""
    proxyip = ""
    proxyport = ""
    proxytype = ""
    validproxy = False;
    s = 0;
    json_path = pathlib.Path('proxies/proxies.json')
    if not json_path.exists():
        print("GETAPI.json file not exists!")
        raise ValueError

    with open(json_path.resolve(), mode="r", encoding="utf8") as j:
        try:
            datas = json.loads(j.read())
            print(f"proxies 加载完成,数目:{len(datas)}")
            while validproxy != True:
                proxytemp = datas[s]
                proxyip = proxytemp['ip']
                proxyport = proxytemp['port']
                s +=1
                print("testing",proxyip, proxyport)
                if isValid(proxyip,proxyport):
                    validproxy = True
                    vp = proxyip + ':' + proxyport
                    print(proxyip,proxyport)
                    return vp
                else:
                    print("proxy failed",proxyip,proxyport)

        except Exception as why:
            print(f"Json file syntax error:{why}")
            raise ValueError

def isValid(ip,port):
    try:
        proxies = {
            'https': 'socks4://' + ip + ':' + port
        }
        response = requests.get('https://www.baidu.com', proxies=proxies, timeout=5)
        print(ip, port, response.status_code)
        if response.status_code == 200:
            return True
        else:
            return False

    except requests.exceptions.RequestException:
        return False



#random string generator
def randomString(length=16):
    base_Str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    random_str = ''
    for i in range(length):
        random_str += base_Str[random.randint(0, (len(base_Str) - 1))]
    return random_str

def register_XboxGamePass_and_refund(email,password):
    Xbox_User = 'Alt' + randomUsername(6)
    IGN = 'Alt' + randomUsername(2) + 'D' + randomUsername(4)

    # 打开微软账户管理页面
    print('[Debugger]即将打开浏览器并自动购买......')
    driver.get('https://www.xbox.com/zh-HK/xbox-game-pass#join')
    # 在页面上查找29港币的PC Game pass
    print("在页面上查找29港币的PC Game pass")
    purchase()
    WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.NAME, 'loginfmt'))).send_keys(email)
    # 输入邮箱
    print('[Debugger]即将自动输入邮箱密码登录......')
    # 点击下一步
    print("点击下一步")
    next_button = driver.find_element(By.ID, 'idSIButton9').click()
    time.sleep(4)
    # 输入密码
    print("输入密码")
    WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.NAME, 'passwd'))).send_keys(password)
    print("点击登录")
    WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.ID, 'idSIButton9'))).click()
    # 点击保持登录状态
    print("点击保持登录状态")
    try:
        WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.ID, 'idSIButton9'))).click()
    except NoSuchElementException:
        skip_button = driver.find_element(By.ID, 'iShowSkip').click()
        time.sleep(5)
        keep_login_button = driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(5)
        cancel_button_1 = driver.find_element(By.ID, 'iCancel').click()
        time.sleep(30)
    print("重置页面...")
    driver.get('https://www.xbox.com/zh-HK/xbox-game-pass#join')
    print("等待...")
    print("当前URL：" + driver.current_url)
    time.sleep(5)
    target_url = "https://www.xbox.com/zh-HK/xbox-game-pass#join"
    target_url = str(target_url)
    if target_url == str(driver.current_url):
        print("页面正确，继续操作")
        pass
    else:
        print("当前页面不合规，尝试关闭此页面....！")
        driver.close()
    WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.XPATH,
                                                                        "/html/body/div[1]/div/div/div[3]/div/div/div/div[2]/div[5]/div[1]/div[2]/section/div/div/ul/li[1]/div/div[1]/div[2]/a"))).click()
    # 输入Xbox用户名
    try:
        print("输入Xbox用户名")
        print('[Debugger]即将自动设置Xbox用户名......（15sec）')
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'create-account-gamertag-input'))).send_keys(Xbox_User)
        print("确认ID有效之后按下回车(不要操作页面！)")
        b = input("")
        # 这个脑残 容易卡在这里 所以手动确认一下
        print("你已经确认")
        # 点击开始按钮
        print("点击开始按钮...8sec")
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'inline-continue-control'))).click()
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@aria-label="下一步"]'))).click()
        # 点击下一步按钮
    except TimeoutException:
        print("没有发现取名页面,正在判断位置")
        WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@aria-label="下一步"]'))).click()
        time.sleep(8)
        # 添加付款方式
    print('[Debugger]即将自动添加支付宝付款......')
    driver.switch_to.frame('purchase-sdk-hosted-iframe')
    WebDriverWait(driver, 2000).until(
        EC.visibility_of_element_located((By.XPATH, '//button[@class="primary--DXmYtnzQ base--kY64RzQE"]'))).click()
    time.sleep(5)
    # 选择PayPal或Alipay支付
    print("选择PayPal或Alipay支付")
    print("喘气")
    time.sleep(5)
    try:
        # driver.find_element(By.XPATH, '/html/body/section/div[1]/div/div/div/div/div[2]/div/div[4]/button[2]').click()
        WebDriverWait(driver, 2000).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="displayId_ewallet"]'))).click()
        WebDriverWait(driver, 2000).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="displayId_ewallet_alipay_billing_agreement"]'))).click()
        try:
            print("填写姓名")
            # 尝试填写姓名
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,
                                                                             "/html/body/section/div[1]/div/div/div/div/div[2]/div/section/div[2]/div[1]/input"))).send_keys(
                randomUsername(5))
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,
                                                                             "/html/body/section/div[1]/div/div/div/div/div[2]/div/section/div[2]/div[2]/input"))).send_keys(
                randomUsername(5))
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/section/div[1]/div/div/div/div/div[2]/div/section/div[3]/input[2]"))).click()
            time.sleep(4)
        except NoSuchElementException:
            print("未发现姓名填写页面，跳过")
    except NoSuchElementException:
        print("没有发现二维码，可能之前你已经开通过了，请确认页面位于支付宝签约二维码处，然后点击回车")
        print(
            "如果你发现页面上面已经有一个支付宝选项 则说明这个账号已经有人绑定过支付宝了 如果确定继续，请按照如下步骤操作:")
        print("1，点击确定")
        print("2.点击新增付款方式")
        a = input("3.选择支付宝 确认页面位于支付宝签约二维码处，然后点击回车")
    # 等待扫码
    WebDriverWait(driver, 2000).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/section/div[1]/div/div/div/div/div[2]/div/section/div[3]/input[2]"))).click()
    print('[Debugger]等待支付宝扫码...')
    print("开通后按回车")
    a = input("")
    print("你已经手动确认,3s")
    # 点击继续
    print("点击继续")
    continue_button = driver.find_element(By.ID, 'pidlddc-button-alipayContinueButton').click()
    time.sleep(3)
    # 输入城市 & 地址
    try:
        print("输入城市 & 地址")
        WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.ID, 'city'))).send_keys('1')
        WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.ID, 'address_line1'))).send_keys('1')
        # 点击储存按钮
        print("点击储存按钮")
        save_button = driver.find_element(By.ID, 'pidlddc-button-saveButton').click()
        time.sleep(12)
    except NoSuchElementException:
        print(
            "未发现设置地址的页面 按照推测 你已经到达订阅页面 这属于极端情况 说明很有可能这不是新号 如果想继续 请继续")
        pass
    # 点击订阅按钮
    print("点击订阅按钮")
    WebDriverWait(driver, 2000).until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/section/div[1]/div/div/div/div/div[2]/div/div[4]/button[2]"))).click()
    # 等待购买成功
    print("等待购买成功")
    time.sleep(18)
    '''while s == 1:
            pass
        else:
            print("等待购买结果中....")'''
    print('[Debugger]购买成功!')
    # 打开官网设置ID
    print('[Debugger]即将跳转官网为您自动设置ID.....')
    driver.get('https://www.minecraft.net/en-us/msaprofile/mygames/editprofile')
    time.sleep(10)
    # 点击登录按钮
    WebDriverWait(driver, 2000).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a[aria-label='Sign in with Microsoft account']"))).click()
    WebDriverWait(driver, 2000).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='profileName']"))).send_keys('KWZE_' + IGN)
    # 输入随机ID
    # 确认
    try:
        WebDriverWait(driver, 2000).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "button[aria-label='Set up your Profile Name']"))).click()
    except NoSuchElementException:
        print('按钮不可点击 稍等....4sec')
        time.sleep(4)
        WebDriverWait(driver, 2000).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "button[aria-label='Set up your Profile Name']"))).click()
    time.sleep(6)
    print('[Debugger]ID设置成功! ID为:' + 'KWZE_' + IGN)
    # 打开微软退款
    print('[Debugger]即将打开退款链接并自动退款......')
    driver.get('https://account.microsoft.com/services/pcgamepass/cancel?fref=billing-cancel&lang=en-US')
    time.sleep(20)
    try:
        WebDriverWait(driver, 2000).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Cancel subscription']"))).click()
    # 点击保持登录
    except NoSuchElementException:
        # 点击取消订阅按钮
        driver.implicitly_wait(5)
        WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.ID, 'id__0'))).click()
        WebDriverWait(driver, 2000).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Cancel subscription']"))).click()
    # 选择立即退款按钮
    refund_button = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Cancel now and get refund']").click()
    # 点击取消订阅按钮
    cancel_button = driver.find_element(By.ID, 'cancel-select-cancel').click()
    time.sleep(15)
    print('[Debugger]已经成功退款！')

def createOutlookGen(email,password):
    driver.get(
        "https://signup.live.com/signup?lcid=1033&wa=wsignin1.0&rpsnv=13&ct=1605407946&rver=7.0.6738.0&wp=MBI_SSL&wreply=https:%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-signin%3Fru%3Dhttps%253A%252F%252Faccount.microsoft.com%252F%253Frefp%253Dsignedout-index&lc=1033&id=292666&lw=1&fl=easi2&mkt=en-CN")
    time.sleep(0.5)
    try:
        driver.find_element(By.XPATH, '//*[@id="iSignupAction"]').click()
    except NoSuchElementException:
        pass
    driver.find_element(By.XPATH, '//*[@id="MemberName"]').send_keys('a' + email + '@outlook.com')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="iSignupAction"]').click()
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="PasswordInput"]'))).click()
    driver.find_element(By.XPATH, '//*[@id="PasswordInput"]').send_keys('b' + password)
    driver.find_element(By.XPATH, '//*[@id="iSignupAction"]').click()
    WebDriverWait(driver, 200).until((EC.visibility_of_element_located((By.ID, "Country")))).click()
    Select(driver.find_element(By.ID, "Country")).select_by_value("US")
    Select(driver.find_element(By.ID, "BirthMonth")).select_by_value("1")
    Select(driver.find_element(By.ID, "BirthDay")).select_by_value("1")
    driver.find_element(By.ID, "BirthYear").send_keys("1984")
    driver.find_element(By.ID, "iSignupAction").click()
    WebDriverWait(driver, 20000).until(EC.visibility_of_element_located((By.ID, "enforcementFrame"))).click()
    print("请通过人机验证")
    WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="id__0"]'))).click()
    try:
        driver.find_element(By.XPATH, '//*[@id="id__0"]').click()
    except NoSuchElementException:
        pass
    WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="idSIButton9"]'))).click()


#调用driver并配置driver
PROXY = RandomProxy()
caps= webdriver.DesiredCapabilities.CHROME.copy()
caps['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL",
    "socksProxy": PROXY,
    "socksVersion":4

}
driver = webdriver.Chrome(desired_capabilities=caps)
wait = WebDriverWait(driver, 30)

# amount = int(input("你想要创建多少个账号？\n> "))
#
# for x in range(amount):
#     email = randomString(10)
#     # now create a outlook account
#     for y in range(5):
#         b = random.randint(0, 3)
#     if b == 0:
#         password = randomString(8)
#     elif b == 1:
#         password = randomString(5) + "!" + randomString(1)
#     else:
#         password = randomString(3) + "A" + randomString(2) + "!" + randomString(1)
#     createOutlookGen(email, password)
#     register_XboxGamePass_and_refund(email, password)
#     print("Your Account is: " + 'a' + email + '@outlook.com')
#     print("Your password is: " + 'b' + password)
#     email = str(email)
#     with open("accounts.txt", "a") as f:
#         f.write(f"{'a' + email + '@outlook.com'}----{'b' + password}\n")





