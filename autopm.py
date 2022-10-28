import math
import os
import subprocess
import warnings
import requests
import datetime
from time import sleep
import google_play_scraper
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class COLORS:
    BGREEN = '\x1b[1;32;40m'
    RWHITE = '\x1b[1;37;41m'
    BBLUE = '\x1b[1;36;40m'
    BPINK = '\x1b[1;35;40m'
    BRED = '\x1b[1;31;40m'
    BYELLOW = '\x1b[1;33;40m'
    GGREEN = '\x1b[7;37;42m'
    GBLUE = '\x1b[7;37;46m'
    BMAGENTA = '\x1b[1;37;46m'
    END = '\x1b[0m'

class CONSTANTS:
    STAR = f'{COLORS.BGREEN} * {COLORS.END}'
    INFO = f'{COLORS.BYELLOW} i {COLORS.END}'
    RATE = f'{COLORS.BBLUE} @ {COLORS.END}'
    ASK = f'{COLORS.BPINK} ? {COLORS.END}'
    ERROR = f'{COLORS.BRED} ! {COLORS.END}'
    AINFO = f'{COLORS.BMAGENTA} > {COLORS.END}'

def initializeProgram():
    global VERSION, CURRENTDIR, SETTINGSDIR, CHROMEDRIVER, BINARYLOCATION, SHAREDMODTEMPLATE, APPMODTEMPLATE
    VERSION = "1.0"
    CURRENTDIR = os.path.realpath(os.path.dirname(__file__))
    SETTINGSDIR = os.path.join(os.path.join(CURRENTDIR, "settings"))
    CHROMEDRIVER = os.path.join(SETTINGSDIR, "chromedriver.exe")
    APPMODTEMPLATE = """
    [IMG]{}[/IMG]

Playstore Link:
{}

[COLOR=rgb(255, 77, 77)][B][SIZE=14px]Mod APK Features:[/SIZE][/B][/COLOR]
[LIST]
{}
[/LIST]
[COLOR=rgb(0, 255, 0)][SIZE=14px][B]APK Details:[/B][/SIZE][/COLOR]
[LIST]
[*][COLOR=rgb(255, 153, 153)]Version              [/COLOR]: [B]{}[/B]
[*][COLOR=rgb(255, 166, 77)]Genre[/COLOR]                : {}
[*][COLOR=rgb(255, 255, 77)]Rating               [/COLOR]: [B]{}/5[/B]
[*][COLOR=rgb(0, 255, 128)]Developer[/COLOR]         : [B]{}[/B]
[*][COLOR=rgb(0, 128, 255)]Total Installs[/COLOR]      : [B]{}[/B]
[*][COLOR=rgb(128, 0, 255)]Updated On[/COLOR]      : [B]{}[/B]
[*][COLOR=rgb(255, 77, 166)]Content Rating [/COLOR]: [B]{}[/B]
[/LIST]

[COLOR=rgb(255, 0, 128)][SIZE=14px][B]Playstore Description:[/B][/SIZE][/COLOR]
    {}

{}

[COLOR=rgb(0, 255, 0)][B][SIZE=15px]Free Download Links:[/SIZE][/B][/COLOR]

[HIDE]
[COLOR=rgb(255, 166, 77)][B]Download Link[/B]  [/COLOR]         : {}

[COLOR=rgb(77, 255, 255)][B]Mirror Download Link[/B][/COLOR]: {}
[/HIDE]
    """

    warnings.filterwarnings('ignore')

    banner("setup")
    sleep(1)

    if not os.path.exists(SETTINGSDIR):
        print(f"{CONSTANTS.AINFO}{COLORS.BYELLOW} First run detected. {COLORS.END}\n")
        sleep(1)
        print(f"{CONSTANTS.RATE}{COLORS.BYELLOW} Initializing settings. Please wait. {COLORS.END}\n")
        sleep(1)
        os.mkdir(SETTINGSDIR)
        print(f"{CONSTANTS.RATE}{COLORS.BYELLOW} Downloading chromedriver.exe. Please wait. {COLORS.END}\n")

        open(CHROMEDRIVER, "wb").write(requests.get("https://github.com/erucix/chromedriver/raw/main/chromedriver.exe").content)
        chrome = subprocess.getoutput("cd / & dir /s /b chrome.exe")
        brave = subprocess.getoutput("cd / & dir /s /b brave.exe")
        if brave != "File Not Found":
            BINARYLOCATION = brave
        elif chrome != "File Not Found":
            BINARYLOCATION = chrome
        else:
            print(f"{CONSTANTS.ERROR}{COLORS.BYELLOW} Fuck, no binary detected. Exitting...{COLORS.END}\n")
            sleep(2)
            quit()
        binaryLocationFile = open(os.path.join(SETTINGSDIR, "binary.txt"), "w")
        binaryLocationFile.write(BINARYLOCATION)
        binaryLocationFile.close()
        print(f"{CONSTANTS.AINFO}{COLORS.BYELLOW} Binary detect at: {BINARYLOCATION} {COLORS.END}\n")
        print(f"{CONSTANTS.RATE}{COLORS.BYELLOW} Writing some program info. PLease wait. {COLORS.END}\n")
        sleep(1)
        print(f"{CONSTANTS.AINFO}{COLORS.BYELLOW} Moving to main-menu.{COLORS.END}{COLORS.BBLUE} Press ENTER {COLORS.END}\n")
        sleep(5)
    BINARYLOCATION = open(os.path.join(SETTINGSDIR, "binary.txt"), "r").read()
    home()

def banner(position):
    position = position.upper()
    os.system("cls")
    print(f"               __                      ")
    print(f"  ____  __  __/ /_____  ____  ____ ___  {CONSTANTS.RATE}{COLORS.RWHITE} From erucix {COLORS.END}")
    print(f" / __ `/ / / / __/ __ \/ __ \/ __ \"__ \\")
    print(f"/ /_/ / /_/ / /_/ /_/ / /_/ / / / / / /")
    print(f"\__,_/\____/\__/\____/ .___/_/ /_/ /_/  {CONSTANTS.STAR}{COLORS.RWHITE} Version {VERSION} {COLORS.END}")
    print(f"                    /_/                \n")
    print(f"{CONSTANTS.STAR}{COLORS.RWHITE} {position} {COLORS.END}{CONSTANTS.STAR}".center(90))
    print("")

def postMod(value, url):
    banner("post-mod")
    packageName = input(f"{CONSTANTS.AINFO}{COLORS.BBLUE} Enter package name: {COLORS.END} ")
    banner("google play")
    print(f"{CONSTANTS.RATE}{COLORS.BYELLOW} Scraping Google Play Store. Please wait... {COLORS.END}")
    try:
        appDetails = google_play_scraper.app(packageName)
        appTitle = appDetails.get("title")
        appIcon = appDetails.get("icon") + "=s280" #G-Bo told me :)
        appLink = appDetails.get("url")
        appVersion = appDetails.get("version")
        appRating = math.floor(appDetails.get("score"))
        appUpdated = str(datetime.datetime.fromtimestamp(int(str(appDetails.get("updated")) + "000")/1000, tz=datetime.timezone.utc)) + "UTC"
        appDescription = appDetails.get("description")[0:300] + "....."
        appGenre = appDetails.get("genre")
        appContentRating = appDetails.get("contentRating")
        appDeveloper = appDetails.get("developer")
        appInstalls = appDetails.get("realInstalls")

        print(f"\n{CONSTANTS.INFO}{COLORS.BBLUE} App Name       : {COLORS.END} {appTitle}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} App Icon URL   : {COLORS.END} {appIcon}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} Playstore Link : {COLORS.END} {appLink}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} Version        : {COLORS.END} {appVersion}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} Genre          : {COLORS.END} {appGenre}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} Ratings        : {COLORS.END} {appRating}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} Content Rating : {COLORS.END} {appContentRating}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} Developer      : {COLORS.END} {appDeveloper}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} Total Installs : {COLORS.END} {appInstalls}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} Updated On     : {COLORS.END} {appUpdated}")
        print(f"{CONSTANTS.INFO}{COLORS.BBLUE} Description    : {COLORS.END} {appDescription[0:100]}..")        
    except:
        print(f"\n{CONSTANTS.ERROR}{COLORS.RWHITE} Critical error occured. {COLORS.END}")
        sleep(3)
        home()
        return
    else:
        specialFeatureTitle = input(f"\n{CONSTANTS.ASK}{COLORS.BYELLOW} Features for title       : {COLORS.END} ")
        specialFeatures = input(f"{CONSTANTS.ASK}{COLORS.BYELLOW} Features (seperated by ;): {COLORS.END} ").replace("; ", ";").split(";")
        features = ""
        for feature in specialFeatures:
            features = features + "[*][COLOR=rgb(255, 255, 0)]" + feature +"[/COLOR]\n"
        specialFeatures = features
        notes = input(f"{CONSTANTS.ASK}{COLORS.BYELLOW} Any Notes? [Enter=Empty] : {COLORS.END} ").strip()
        if notes != "":
            notes = "[B][COLOR=rgb(255, 255, 0)]NOTE[/COLOR]:[/B] [COLOR=rgb(77, 166, 255)]" + notes +"[/COLOR]"
        downloadLink1 = input(f"\n{CONSTANTS.ASK}{COLORS.BYELLOW} Download Link            : {COLORS.END} ")
        downloadLink2 = input(f"{CONSTANTS.ASK}{COLORS.BYELLOW} Mirror Download Link     : {COLORS.END} ")
        


    print(f"\n{CONSTANTS.RATE}{COLORS.BYELLOW} Initializing browser. Please close all open tabs... {COLORS.END}\n")
    sleep(2)

    options = webdriver.ChromeOptions()
    options.binary_location = BINARYLOCATION
    options.add_argument(r"--user-data-dir=C:\Users\eruci\AppData\Local\BraveSoftware\Brave-Browser\User Data")
    options.add_argument(r'--profile-directory=Default')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER, options=options)
    browser.get(url)
    browser.find_element(By.ID, "xfBbCode-1").click()
    innerValue = APPMODTEMPLATE.format(appIcon, appLink, specialFeatures, appVersion, appGenre, appRating, appDeveloper, appInstalls, appUpdated, appContentRating, appDescription, notes, downloadLink1, downloadLink2)
    browser.find_element(By.CLASS_NAME, "input--title").clear()
    browser.find_element(By.CLASS_NAME, "input--title").send_keys(appTitle + " v" + appVersion + " [ " + specialFeatureTitle +" Mod Apk ]")
    sleep(3)
    browser.execute_script(f"document.querySelector('textarea').value = `" + innerValue + "`")
    print(f"\n{CONSTANTS.AINFO}{COLORS.BYELLOW} Browser has been started. [Ctrl + C] to stop {COLORS.END}\n")

    while True:
        pass

def getStaffs():
    banner("active-staff-list")
    print(f"{CONSTANTS.RATE}{COLORS.BYELLOW} Searching active staffs. Please wait... {COLORS.END}")
    staffList = BeautifulSoup(requests.get("https://platinmods.com").content, "html.parser").select("div[data-widget-section='staffMembers']")[0].find_all(class_="username--staff")
    for username in staffList:
        print(f"{CONSTANTS.STAR}{COLORS.RWHITE} {username.string} {COLORS.END}")
    print("")
    os.system("pause")
    home()

def home():
    banner("main-menu")
    print(f"{COLORS.BBLUE} 1 {COLORS.END} Post shared game mod")
    print(f"{COLORS.BBLUE} 2 {COLORS.END} Get active staffs")
    print(f"{COLORS.BBLUE} 3 {COLORS.END} Reset Program Data")
    print(f"{COLORS.RWHITE} 4 {COLORS.END} Exit\n")

    option = input(f"{CONSTANTS.AINFO} ")

    if option == "1":
        postMod(APPMODTEMPLATE, "https://platinmods.com/forums/untested-android-apps.155/post-thread")
    elif option == "2":
        getStaffs()
    elif option == "3":
        print(f"{CONSTANTS.AINFO}{COLORS.BYELLOW} Clearing & Exitting...{COLORS.END}")
        os.rmdir(SETTINGSDIR)
        sleep(2)
        quit()
    elif option == "4":
        exit()
        quit()
    else:
        home()
    

initializeProgram()