from bs4 import BeautifulSoup
import re
import requests
from pymongo import MongoClient

url = "https://crautos.com/autosusados/zonaverde/"
CONNECTION_STRING = "mongodb+srv://root:rootroot@webscraperdata.x6mux.mongodb.net/WebScraperData?retryWrites=true&w=majority"


def removeSideTags(string):
    firstIndexOfTag = string.index(">") + 1
    lastIndexOfTag = len(string) - 1 - string[::-1].index("<")
    string = string[firstIndexOfTag:lastIndexOfTag]
    return string


def removeSideSpaces(string):
    newString = re.sub("[\r\n\t]", "", string)
    newString = newString.lstrip(" ").rstrip(" ")
    return newString


def removeInsideTags(string):
    newString = ""
    while "<" in string and ">" in string:
        openTagIndex = string.index("<")
        closeTagIndex = string.index(">") + 1
        if closeTagIndex < openTagIndex:
            newString = re.sub(">", "", string, 1)
            closeTagIndex = string.index(">")
        else:
            newString = string
        tag = newString[openTagIndex:closeTagIndex]
        newString = newString.replace(tag, " ")
        string = newString
    if newString == "":
        return string
    return newString


def cleanString(string):
    string = removeInsideTags(string)
    string = removeSideSpaces(string)
    return string


def scrapeData(url):
    carList = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    inventory = soup.find_all("a", class_="inventory dealerhlcar")
    results = []
    for item in inventory:
        if re.search('cardetail.cfm', item.get("href")):
            results.append(url + item.get("href"))

    for carUrl in results:
        car = {}
        car["url"] = carUrl

        carPage = requests.get(carUrl)
        soup = BeautifulSoup(carPage.content, 'html.parser')

        carModel = str(soup.find("h2"))
        carModel = removeSideTags(carModel)

        carName = carModel[:carModel.index("<")]
        carYear = carModel[carModel.index(">") + 1:]
        car["nombre"] = carName
        car["anno"] = carYear

        carInfo = soup.find(id="geninfo")
        carAttributes = carInfo.find_all("tr")
        for carAttributePair in carAttributes:
            attributePair = carAttributePair.find_all("td")

            if len(attributePair) == 2:
                key = removeSideTags(str(attributePair[0]))
                value = removeSideTags(str(attributePair[1]))
            else:
                key = "nota"
                value = removeSideTags(str(attributePair[0]))

            dbKey = removeSideSpaces(key).replace(" ", "_").lower()
            dbValue = cleanString(value)
            dbValue = removeSideSpaces(dbValue)

            car[dbKey] = dbValue
        # print(car)
        carList.append(car)
    return carList


client = MongoClient(CONNECTION_STRING)
db = client['WebScraperData']
collection = db['carros']

scrapedCarData = scrapeData(url)
collection.insert_many(scrapedCarData)
