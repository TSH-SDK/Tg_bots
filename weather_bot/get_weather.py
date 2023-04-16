import httpx
from bs4 import BeautifulSoup

headers = {
    "accept-language": "ru-RU, ru; q=0.9, en;q=0.8, de;q=0.7, *;q=0.5",
    "user-agent": "Mozilla/5.0 (Windows NT 10; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}

async def get_response(link: str):
    async with httpx.AsyncClient(headers=headers) as asyclient:
        result = await asyclient.get(link)
        if result.status_code != 200:
            return await get_response(link=link)
        else:
            return await result.aread()

async def get_weather_text(city: str):
    link = f"https://www.gismeteo.ru/weather-{city}/now/"
    result_resp = await get_response(link=link)
    soup = BeautifulSoup(markup=result_resp, features='lxml')
    place = soup.find("div", class_="breadcrumbs-links")
    date = soup.find("div", class_="now-localdate")
    temp = soup.find("span", class_="unit unit_temperature_c" )
    wind = soup.find("div", class_="unit unit_wind_m_s" )
    pressure = soup.find("div", class_="unit unit_pressure_mm_hg_atm")
    return f"{place.text} \n"\
           f"<i>{date.text}</i> \n" \
           f"<b>Температура</b>: {temp.text}\n" \
           f"<b>Ветер</b>: {wind.text}\n" \
           f"<b>Давление: {pressure.text}</b>"
