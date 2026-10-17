from pathlib import Path
from PIL import Image, ImageDraw

thu_muc = Path(__file__).parent / "static"
thu_muc.mkdir(exist_ok=True)

for kich_thuoc in [192, 512]:
    anh = Image.new("RGB", (kich_thuoc, kich_thuoc), "#812b34")
    ve = ImageDraw.Draw(anh)

    # Vẽ hình quyển sách bằng tọa độ tương đối
    def diem(x, y):
        return (round(x * kich_thuoc), round(y * kich_thuoc))

    ve.polygon(
        [
            diem(0.22, 0.29),
            diem(0.48, 0.34),
            diem(0.48, 0.73),
            diem(0.22, 0.68),
        ],
        fill="#fff6e7"
    )

    ve.polygon(
        [
            diem(0.52, 0.34),
            diem(0.78, 0.29),
            diem(0.78, 0.68),
            diem(0.52, 0.73),
        ],
        fill="#fff6e7"
    )

    for y in [0.42, 0.51, 0.60]:
        ve.line(
            [diem(0.29, y), diem(0.41, y + 0.025)],
            fill="#c4a68c",
            width=max(2, kich_thuoc // 100)
        )

        ve.line(
            [diem(0.59, y + 0.025), diem(0.71, y)],
            fill="#c4a68c",
            width=max(2, kich_thuoc // 100)
        )

    duong_dan = thu_muc / f"icon-{kich_thuoc}.png"
    anh.save(duong_dan)
    print("Đã tạo:", duong_dan)