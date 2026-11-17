
import requests

url = "http://127.0.0.1:5000/process"

number = int(input("Введите число: "))

response = requests.post(
    url,
    json={"number": number}
)

print("HTTP status:", response.status_code)
print("Ответ:", response.json())
