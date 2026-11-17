import requests

url = "http://127.0.0.1:5000/process"

response = requests.post(
    url,
    json={"number": 10}
)

print("Статус:", response.status_code)
print("Ответ:", response.text)