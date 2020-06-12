from bs4 import BeautifulSoup
import requests
import re
import json

html_content = requests.get('https://dot.ca.gov/contact-us').text
soup = BeautifulSoup(html_content, "lxml")

organizations_table = soup.find("table")
organizations_table_data = organizations_table.tbody.find_all("tr")

returnList = list()

for tr in organizations_table_data:

    response = {}
    tds = tr.find_all("td")

    # Organization name
    organization = tds[0].text.replace('\n', ' ').strip()
    response["office_name"] = organization

    # Address of the organization's office
    street_address = tds[1].text.strip().split('\n')
    response["office_address"] = street_address[0]

    office_city = street_address[1].strip().split(' ')[:-2]
    if len(office_city)==1:
        response["office_city"] = office_city[0].strip(", ")
    else:
        city_name = ""
        for city in office_city:
            city_name+=city
            city_name+=" "
        response["office_city"] = city_name.strip(", ")

    offic_state = street_address[1].strip().split(' ')[-2:][0]
    response["office_state"] = offic_state
    office_zip = street_address[1].strip().split(' ')[-2:][1]
    response["office_zip"] = office_zip

    # Phone Number
    phone_data = tds[3].text.strip()
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    results = r.findall(phone_data)
    response["office_phone"] = results[0]

    # Mailing Address
    mailing_address = tds[2].text.strip().split('\n')
    mailing_address1 = mailing_address[0]
    if mailing_address1[:4]=="P.O.":
        response["mail_address"] = None
        response["mail_pobox"] = mailing_address1
    else:
        response["mail_address"] = mailing_address1
        response["mail_pobox"] = None

    mailing_address2 = mailing_address[-1].strip("").split()
    mail_city = mailing_address2[:-2]
    if len(mail_city)==1:
        response["mail_city"] = mail_city[0].strip(", ")
    else:
        city_name = ""
        for city in mail_city:
            city_name+=city
            city_name+=" "
        response["mail_city"] = city_name.strip(", ")

    mail_state, mail_zip = mailing_address2[-2], mailing_address2[-1]
    response["mail_state"] = mail_state
    response["mail_zip"] = mail_zip

    response["mail_phone"] = None

    returnList.append(response)

result = json.dumps(returnList)
print(result)



