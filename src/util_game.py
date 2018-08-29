from .custom_driver import client
from .utils import log
from enum import Enum


def close_modal(browser: client) -> None:
    el = browser.find("//div[@class='modalContent']")
    el = el.find_element_by_xpath(".//a[@class='closeWindow clickable']")
    browser.click(el)


def close_welcome_screen(browser: client) -> None:
    wc = browser.find("//div[contains(@class, 'welcomeScreen')]")
    log("closing welcome-screen")
    el = wc.find_element_by_xpath(
        ".//a[@class='closeWindow clickable']")
    browser.click(el)


def check_resources(browser: client) -> dict:
    resources_list = ["wood", "clay", "iron", "crop"]
    resources = {}
    for res in resources_list:
        find_resources = browser.find(
            "//div[@class='stockContainer {0}']".format(res))
        find_resources = find_resources.find_element_by_xpath(
            ".//div[contains(@class, 'progressbar')]")
        value = int(find_resources.get_attribute("value"))
        resources[res] = value
    return resources


class shortcut(Enum):
    marketplace = 0
    barrack = 1
    stable = 2
    workshop = 3


def open_shortcut(browser: client, sc: shortcut) -> None:
    shortcut_link = browser.find("//div[@id='quickLinks']")
    shortcut_link = shortcut_link.find_element_by_xpath(
        ".//div[contains(@class, 'slotWrapper')]")
    link = shortcut_link.find_elements_by_xpath(
        ".//div[contains(@class, 'slotContainer')]")
    browser.click(link[sc.value], 1)


def stationed_troops(browser: client) -> dict:
    troops_dict = {}
    foo = 0
    troops_stationed = browser.find("//div[@id='troopsStationed']/ul/ul")
    lis = troops_stationed.find_elements_by_xpath(".//li")
    tribe = lis[0].get_attribute("tooltip-translate")
    troop_name = troops_name(browser, tribe)
    for listed in lis[2:]:
        div = listed.find_element_by_xpath(".//div")
        troop_amount = div.get_attribute("innerHTML")
        if len(troop_amount) == 0:
            troops_dict[troop_name[foo]] = 0
            foo += 1
        else:
            troops_dict[troop_name[foo]] = int(troop_amount)
            foo += 1
    return troops_dict


def troops_name(browser: client, tribe: str) -> list:
    troops_dict = {"tribe_1":
        ["legionnaire","praetorian","imperian","equites_legati","equites_imperatoris","equites_caesaris","battering_ram","fire_catapult","senator","settler","hero"],
        "tribe_3":
        ["phalanx","swordsman","pathfinder","theutates_thunder","druidrider","haeduan","ram","trebuchet","chieftain","settler","hero"],
        "tribe_2":
        ["clubswinger","spearfighter","axefighter","scout","paladin","teutonic_knight","ram","catapult","chief","settler","hero"]}
    return troops_dict[tribe.lower()]

