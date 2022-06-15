import httpx
from bs4 import BeautifulSoup
from urllib import parse

def search(query):
    search_page = httpx.get("https://noonnu.cc/font_page?search=" + parse.quote(query)).text
    search_soup = BeautifulSoup(search_page, "html.parser")

    a_elements = search_soup.find_all("a")
    font_data = []
    for e in a_elements:
        img_element = e.find("img", class_="font-image-preview")
        if img_element:
            font_data.append({"name": img_element.get("alt"), "page": int(e.get("href").split("/")[2])})

    return font_data

def get_license(page):
    font_page = httpx.get("https://noonnu.cc/font_page/" + str(page)).text
    font_soup = BeautifulSoup(font_page, "html.parser")

    tr_elements = font_soup.find_all("tr")
    tr_elements.pop(0)
    license_data = {}
    license_names = ["print", "website", "video", "bi&ci", "embed", "package", "ofl"]
    for i in range(len(tr_elements)):
        license_data.update({license_names[i]: tr_elements[i].find_all("td")[2].get_text().strip() == "O"})

    return license_data

print(get_license(search("고딕")[0].get("page")))
