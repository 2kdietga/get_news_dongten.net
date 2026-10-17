import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def lay_bai_moi():
    url = "https://dongten.net/"

    # Tải phiên bản hiện tại của trang chủ
    print("Đang tải trang dongten.net, bạn chờ một chút...")
    response = requests.get(url, timeout=(15, 90))
    response.raise_for_status()

    # Phân tích HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Chỉ tìm trong khu vực "Bài Mới"
    khu_vuc = soup.select_one(".newest")

    if khu_vuc is None:
        raise ValueError("Không tìm thấy mục Bài Mới. Cấu trúc trang có thể đã đổi.")

    danh_sach = []
    link_da_lay = set()

    # Mỗi tiêu đề bài nằm trong thẻ h3
    for tieu_de in khu_vuc.select("h3"):
        the_link = tieu_de.find_parent("a")

        if the_link is None or not the_link.get("href"):
            continue

        ten_bai = tieu_de.get_text(" ", strip=True)
        link = urljoin(url, the_link["href"])

        # Bỏ qua bài trùng
        if link in link_da_lay:
            continue

        link_da_lay.add(link)

        danh_sach.append({
            "tieu_de": ten_bai,
            "link": link
        })

    if not danh_sach:
        raise ValueError("Tìm thấy mục Bài Mới nhưng chưa lấy được bài nào.")

    return danh_sach


if __name__ == "__main__":
    try:
        cac_bai = lay_bai_moi()

        print(f"Lấy được {len(cac_bai)} bài:\n")

        for so, bai in enumerate(cac_bai, start=1):
            print(f"{so}. {bai['tieu_de']}")
            print(bai["link"])
            print()

    except (requests.RequestException, ValueError) as error:
        print("Không lấy được tin:", error)