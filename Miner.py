# coding=utf-8
import datetime
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from pandas import pandas as pd


class MY_Miner():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.set_headless()
        options.add_argument('--disable-gpu')
        self.wb = webdriver.Chrome(options=options)  # 全局变量，保证每次完毕后不关闭
        # self.wb = webdriver.Chrome()  # 全局变量，保证每次完毕后不关闭
        self.wait = WebDriverWait(self.wb, 60)

    def check_ncount(self):
        # 根据现在时间,随时查看倒计时
        time_now = datetime.datetime.now()
        ncount = 60 - time_now.second
        return ncount

    def check_num(self,shade):
        num_1 = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="Results"]/ul[1]/li[1]')
            )
        ).get_attribute("class")
        num_2 = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="Results"]/ul[1]/li[2]')
            )
        ).get_attribute("class")
        num_3 = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="Results"]/ul[1]/li[3]')
            )
        ).get_attribute("class")
        num_total = int(num_1[-1]) + int(num_2[-1]) + int(num_3[-1])
        if shade == '大':
            if num_total > 10:
                print('已中奖，准备退出')
                print('-------------------')
                return True
            else:
                print('未中奖，准备下一轮')
                print('----------------')
                return False
        if shade == '小':
            if num_total > 10:
                print('未中奖，准备下一轮')
                print('-------------------')
                return False
            else:
                print('已中奖，准备退出')
                print('----------------')
                return True

    def check_next_issue(self):
        try:
            confirm = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH,'//*[contains(@id,"layermbox")]/div[2]/div/div/button')
                )
            )
            time.sleep(2)#z这个必须带，不然可能会有点不上的风险
            confirm.click()
        except:
            print('系统异常，再次重试。。。')
            self.check_next_issue()


    def check_issue(self):
        # 根据当前时间,随时查看当前期数
        time_now = datetime.datetime.now()
        issue = str(time_now.year) + str(time_now.month) + str(time_now.day) + str(
            time_now.hour * 60 + time_now.minute + 1)
        return issue

    def goto_room(self):
        room_url = 'http://fh9222.com/lottery/K3/OG1K3'
        self.wb.get(room_url)
        time.sleep(1)
        login_name = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#app > div > div.container.registerPage > ul > li:nth-child(1) > input'))
        )
        login_name.send_keys('*****************')#输入账号
        print('输入账号成功')
        time.sleep(1)
        login_pword = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#app > div > div.container.registerPage > ul > li:nth-child(2) > input'))
        )
        login_pword.send_keys('********')#输入密码
        print('输入密码成功')
        time.sleep(1)
        submit = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#app > div > div.container.registerPage > ul > li:nth-child(3) > a.mainColorBtn.submitBtnBig.ClickShade'))
        )
        submit.click()
        time.sleep(1)
        print('进入房间成功')
        print('---------------')

    def choose_shade(self,small=False,big=False):
        #选择大按钮
        shade_big = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,'//*[@id="app"]/div/div[2]/div[3]/div[1]/div[2]/div[3]/ul/li[17]/a')
            )
        )
        # 选择小按钮
        shade_small = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div[2]/div[3]/ul/li[18]/a')
            )
        )
        time.sleep(1)
        if small == True:
            shade_small.click()
            time.sleep(1)
            print('选择：小')
            shade = '小'
            return shade
        if big == True:
            shade_big.click()
            time.sleep(1)
            print('选择：大')
            shade = '大'
            return shade

    def input_money(self,money):
        # 输入金额
        eachprice = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div[2]/div[5]/table/tbody/tr/td[3]/i/input')
            )
        )
        eachprice.send_keys(money)
        time.sleep(1)
        print('投注金额 ：{}元'.format(money))
    def submit_shade(self):
        # 点击确认投注
        click_confirm = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div[2]/div[6]/a')
            )
        )
        click_confirm.click()
        time.sleep(2)
        # 再次确认投注
        click_confirm2 = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[contains(@id,"layermbox")]/div[2]/div/div/div[2]/span[2]')
            )
        )
        click_confirm2.click()
        time.sleep(2)
        # 投注成功通知确认
        click_confirm3 = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[contains(@id,"layermbox")]/div[2]/div/div/div[2]/span')
            )
        )
        click_confirm3.click()
        time.sleep(2)
        print('投注成功')

    def send_email(self,text=''):
        # 设置服务器
        from email.mime.text import MIMEText

        mail_host = 'smtp.zjvtit.edu.cn'
        mail_user = '**********'#发件人邮箱
        mail_pas = '*********'#发件人邮箱密码

        # 设置用户
        sender = '*****'#发件人
        recivers = ['******']#收件人

        # 设置邮件内容
        message = MIMEMultipart('mixed')

        subject = text
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = Header(sender, 'utf-8')
        message['To'] = Header(';'.join(recivers), 'utf-8')

        # 文字内容
        text_mime = MIMEText('', 'plain', 'utf-8')
        message.attach(text_mime)

        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pas)
        smtpObj.sendmail(sender, recivers, message.as_string())
        print('提醒邮件已发送。。。')

    def calculate_data(self,issue,money,income):
        # 初始化判断条件
        data = pd.DataFrame({
            '期数':issue,
            '投注金额':money,
            '收入':income
        }
        )
    def my_plan(self,indicator):
        prophet = random.randint(3,18)
        if prophet <= 10:
            shade = self.choose_shade(small=True)
        else:
            shade = self.choose_shade(big=True)
        my_plan_list = [1, 2, 6, 8, 10]
        money = my_plan_list[indicator]
        self.input_money(money)
        self.submit_shade()
        return money,shade

    def alarm_1(self):
        print('-----------------警报！警报！警报！----------------------\n')
        print('-----------------接下来是试图挽回成本-----------\n')
    def alarm_2(self):
        print('----------接下来是最后的防守一搏，如须干预，请立刻进入！！！！！！！！！\n\n\n----------')
    def alarm_3(self):
        self.send_email(text='你损失了大量资金。\n不要泄气，后面还有机会，加油！')
        print('保本已失效，现在准备东山再起。。。。。。。。。')
    def plan_process(self):
        # 进入房间静默等待本期结束，准备开始
        global money
        self.check_next_issue()
        # 是否中奖指针设置为未中奖
        isprize = False
        # 金额进度指针设置为0
        i =0
        # 初始化数据统计三个变量
        issue_list = []
        money_list = []
        income_list = []
        # 开始循环，推出条件为True
        while isprize == False:
            # 设置三等报警条件
            if i == 3:
                self.alarm_1()
            if i == 4:
                self.alarm_2()
            if i == 5:
                self.alarm_3()
                i = 0
            # 设置收入为0,为数据统计准备
            income = 0

            # 10-60秒，进入先投钱，然后再初始化金钱，点击，投钱,确认
            money,shade = self.my_plan(indicator=i)
            print('这是第{}次投注'.format(i+1))

            # 金钱指针前移一位
            i += 1
            # 数据统计三个列表添加数据
            issue_list.append(self.check_issue())
            money_list.append(money)
            income_list.append(0)
            # 等待本局截至,静默20秒,等待开奖
            self.check_next_issue()
            time.sleep(20)
            # 开奖,若中为True,不中为False
            isprize = self.check_num(shade)

        # 中奖后跳出循环,开始统计本剧收益

        statements = money *1.93#单局中赔率为1.93
        # 统计每局收入状况
        for j in range(len(money_list)):
            income_list[j] = 0 - money_list[j]
        income_list[-1] = statements - money_list[-1]
        # 构建pandas数据体
        data = pd.DataFrame({
            '期数' : issue_list,
            '金额' : money_list,
            '收益' : income_list,
        },columns=['期数','金额','收益']
        )
        time.sleep(5)
        return data

    def main(self):
        try:
            self.goto_room()
            finally_data = pd.DataFrame(columns=['期数', '金额', '收益'])
            for i in range(20):
                print(finally_data)
                print('-----------------------------------------round:{}---------------------------------------'.format(
                    i + 1))
                self.send_email(
                    text='''
                    上一轮收益为：{}\n
                    即将进行的是round:{}\n
                    '''.format(finally_data['收益'].sum(),i + 1))
                data = self.plan_process()
                finally_data = finally_data.append(data)

            print(finally_data)

        except TimeoutException:
            print('TimeoutException错误，修正后再出发。。。')
            self.send_email(text='TimeoutException错误，修正后再出发。。')
        except WebDriverException :
            print('WebDriverException错误，修正后再出发。。。')
            self.send_email(text='WebDriverException错误，修正后再出发。。')
        finally:
            print('矿机已停止运转，欢迎下次使用。。。')

if __name__ == '__main__':
    # for i in range(5):
    my_miner = MY_Miner()
    my_miner.main()

