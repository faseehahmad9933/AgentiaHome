import requests

url = f"https://io.adafruit.com/api/v2/Faseeh99/feeds/light/data/last"

headers = {
"X-AIO-Key": "aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1"
}
response = requests.get(url, headers=headers)
jsonRespounse= response.json()
value = jsonRespounse.get('value')
print(value)