#%%
from bs4 import BeautifulSoup
from loguru import logger
import requests
import urllib
import pandas as pd
#%%
cookies = {
    'dtCookie': 'v_4_srv_32_sn_C625B7E7FDAF6F0FC3E43EE36EF629DE_perc_100000_ol_0_mul_1_app-3Ae63eebabdf39f376_1_rcs-3Acss_1',
    'erplmeplxroute': 'node2',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # 'cookie': 'dtCookie=v_4_srv_32_sn_C625B7E7FDAF6F0FC3E43EE36EF629DE_perc_100000_ol_0_mul_1_app-3Ae63eebabdf39f376_1_rcs-3Acss_1; erplmeplxroute=node2',
    'dnt': '1',
    'priority': 'u=1, i',
    'referer': 'https://www.europarl.europa.eu/meps/en/256864/ANDRAS+TIVADAR_KULJA/meetings/past',
    'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'meetingType': 'PAST',
    'memberId': '256864',
    'termId': '10',
    'page': '14',
    'pageSize': '10',
}

response = requests.get(
    'https://www.europarl.europa.eu/meps/en/loadmore-meetings',
    params=params,
    cookies=cookies,
    headers=headers,
)
# %%
len(response.content.strip())
# %%
page= 10
member_id = 256864
params = {
            "meetingType": "PAST",
            "memberId": member_id,
            "termId": "10",
            "page": str(page),
            "pageSize": "10",
        }
base_url = "https://www.europarl.europa.eu/meps/en/loadmore-meetings"
request_url = f"{base_url}?{urllib.parse.urlencode(params)}"
print(request_url)

response = requests.get(f"{base_url}?{urllib.parse.urlencode(params)}")

response.content
# %%
response.status_code
# %%
soup = BeautifulSoup(response.content, 'html.parser')
# %%
soup
# %%
print(f"{base_url}?{urllib.parse.urlencode(params)}")
# %%
records_dict = {
    "Title": [],
    "Date":[],
    "Place": [],
    "Capacity": [],
    "Code of associated committee or delegation": [],
    "Meeting with": [],
    "page_number": [],
}

headers = soup.select(".erpl_document-header")
for header in headers:
    try:
        title = header.select_one(".t-item").get_text()
    except Exception as e:
        logger.warning(f"Failed to retrieve title: {e}")
        title = None

    try:
        date = header.select_one("time").get("datetime")
    except Exception as e:
        logger.warning(f"Failed to retrieve date: {e}")
        date = None

    try:
        place = header.select_one(".erpl_document-subtitle-location").get_text()
    except Exception as e:
        logger.warning(f"Failed to retrieve place: {e}")
        place = None

    try:
        capacity = header.select_one(".mt-25:nth-child(3) .d-inline").get_text().strip().replace("\n", " - ")
    except Exception as e:
        logger.warning(f"Failed to retrieve capacity: {e}")
        capacity = None

    try:
        code = header.select_one(".mt-25:nth-child(4) .d-inline").get_text().strip().replace("\n", " - ")
    except Exception as e:
        logger.warning(f"Failed to retrieve code: {e}")
        code = None

    try:
        meeting = header.select_one(".mt-25:nth-child(5) .d-inline").get_text().strip().replace("\n", " - ")
    except Exception as e:
        logger.warning(f"Failed to retrieve meeting: {e}")
        meeting = None

    records_dict["Title"].append(title)
    records_dict["Date"].append(date)
    records_dict["Place"].append(place)
    records_dict["Capacity"].append(capacity)
    records_dict["Code of associated committee or delegation"].append(code)
    records_dict["Meeting with"].append(meeting)
    records_dict["page_number"].append(page)
# %%
pd.DataFrame(records_dict)
# %%
records_dict
# %%
