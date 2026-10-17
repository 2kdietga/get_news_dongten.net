import requests

url = "https://dongten.net/"

try:
    response = requests.get(url, timeout=30)

    print("Mã phản hồi:", response.status_code)
    print("Địa chỉ nhận được:", response.url)

    response.raise_for_status()

    with open("dongten.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    print("Đã lưu nội dung vào dongten.html")

except requests.RequestException as error:
    print("Không lấy được trang:", error)