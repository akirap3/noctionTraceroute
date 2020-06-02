#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, os, shutil, re
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import pandas as pd


# In[ ]:


def create_instance(target_url):
    options = Options()
    options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    # ChromeDriver 83.0.4103.14
    webdriver_path = os.getcwd()+"\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    driver.get(target_url)
    driver.maximize_window()
    return driver


# In[ ]:


# create tab and open by finding link text
def open_tab(driver, tab_number, url):
    time.sleep(1)
    driver.execute_script("window.open('about:blank', '"+tab_number+"');")
    time.sleep(1)
    driver.switch_to.window(tab_number)
    time.sleep(1)
    driver.get(url)


# In[ ]:


# open noction webpage, but will direct to unsafe page
def directToMainPage(driver):
    driver.find_element_by_id("details-button").click()
    driver.find_element_by_id("proceed-link").click()


# In[ ]:


def NoctionLogin(driver,username, password):
    # elment ids of username, password and subcimt
    elm_username_id = "username"
    elm_password_id =  "password"
    elm_submit_id = "_submit"
    #to login
    driver.find_element_by_id(elm_username_id).send_keys(username)
    driver.find_element_by_id(elm_password_id).send_keys(password)
    driver.find_element_by_id(elm_submit_id).click()


# In[ ]:


def getDstIPListAndTabList():
    # read destination IP list
    with open(os.getcwd()+"\\DstIPList.txt",'r+') as f:
        dstIPList = f.readlines()
        dstIPList = [x.strip() for x in dstIPList]
    # create a list for storing tabs
    index = 0
    tabList = list(range(0, len(dstIPList)))
    for tab in tabList:
        tabList[index] = 'tab' + str(tab)
        index +=1
    return [dstIPList,tabList]


# In[ ]:


# to get the traceroute table and convert to a csv file
def getTrCsvFile(index,driver,fileName):
    flag = True
    count = 0
    while(flag):
        try:
            driver.find_element_by_link_text("Exploring details").click()
            break
        except:
            time.sleep(10)
            count += 1
            if count == 30:
                flag = False
            continue
    table_element = driver.find_element_by_xpath("//*[@id=\"tabs-2\"]/div/table")
    table_html = table_element.get_attribute('outerHTML')
    html_str = table_html.strip().replace('\n', '')
    # read html and transfer to a list
    dfs = pd.read_html(html_str, header=None, index_col=0, keep_default_na=False)
    result = pd.DataFrame(dfs[0])
    # convert dataframe to a csv file
    if re.search('^\d$', str(index)):
        result.to_csv(os.getcwd()+ "\\CSVFILE\\" + '0' + str(index) + '_' + fileName + '.csv',index=False, header=False)
    else:
        result.to_csv(os.getcwd()+ "\\CSVFILE\\" + str(index) + '_' + fileName + '.csv',index=False, header=False)


# In[ ]:


def switchToSpecificTab(driver,tab):
    # switch to specific window tab
    driver.switch_to.window(tab)


# In[ ]:


def getUsernaeAndPassword():
    # login 
    # enter username and password
    IP = tk.Tk()
    IP.withdraw()
    #username
    username = simpledialog.askstring(title="Username", prompt="Please enter username")
    messagebox.showinfo(title="Username",message="Username: " + username)
    #password
    password = simpledialog.askstring(title="Password", prompt="Please enter password")
    messagebox.showinfo(title="Password",message="Password : " + password)
    return [username, password]


# In[ ]:


def combineAllCSVtoOneXLSX():
    # get path where csv files locate
    newdir = os.getcwd()+"\\CSVFILE" 
    # list csv file names and put into a list
    names = os.listdir(newdir)
    writer = pd.ExcelWriter('TraceRouteCombined.xlsx')
    for name in names:
        path = os.path.join(newdir, name)
        data = pd.read_csv(path, encoding="utf8", index_col=0)
        data.to_excel(writer, sheet_name=name)
    writer.save()


# In[ ]:


# define urls, get username, password, ip list, and tab list
noctionUrl ="https://xxxxxxxxxxxx.noction.net/login"
traceroute_url = "https://xxxxxxxxxxxxxx.noction.net/troubleshooting/traceroute"
usernameAndPassword = getUsernaeAndPassword()
ipListAndTabList = getDstIPListAndTabList()

# remove CSVFILR document
try:
    shutil.rmtree(os.getcwd()+"\\CSVFILE")
except os.error:
    pass

# create a CSVFILR document
try:
    os.mkdir(os.getcwd()+"\\CSVFILE")
except os.error:
    pass

# create the webdriver, direct to Noction web page, and log in
driver = create_instance(noctionUrl)
directToMainPage(driver)
NoctionLogin(driver,usernameAndPassword[0], usernameAndPassword[1])


# In[ ]:


index = 0
for tabName in ipListAndTabList[1]: 
    open_tab(driver, tabName, traceroute_url)
    time.sleep(2)
    # send destination IP 
    driver.find_element_by_name("trace").send_keys(ipListAndTabList[0][index])
    time.sleep(5)
    #click "Trace" button
    driver.find_element_by_css_selector("input[class='btn-new btn-ok submit-traceroute btn-popup']").click()
    time.sleep(20)
    index += 1


# In[ ]:


index = 0
for tabName in ipListAndTabList[1]: 
    switchToSpecificTab(driver,tabName)
    getTrCsvFile(index, driver,ipListAndTabList[0][index])
    index += 1


# In[ ]:


combineAllCSVtoOneXLSX()


# In[ ]:


## for test
# from IPython.display import display_html
# display_html(html_str, raw=True)

