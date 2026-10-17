from datetime import datetime, timezone, timedelta
from threading import Lock
from time import monotonic

import requests
from flask import Flask, render_template, jsonify, send_from_directory

from get_news import lay_bai_moi


app = Flask(__name__)

cac_bai = []
cap_nhat_luc = None
lan_tai_cuoi = 0
khoa = Lock()


# Trả giao diện ngay, không đợi tải tin
@app.get("/")
def trang_chu():
    return render_template("index.html")


# Điện thoại gọi địa chỉ này để lấy dữ liệu
@app.get("/api/tin")
def api_tin():
    global cac_bai, cap_nhat_luc, lan_tai_cuoi

    with khoa:
        # Dùng lại dữ liệu trong 5 phút để hạn chế tải nguồn liên tục
        can_tai = not cac_bai or monotonic() - lan_tai_cuoi >= 300

        if can_tai:
            try:
                bai_moi = lay_bai_moi()

                cac_bai = bai_moi
                gio_vn = timezone(timedelta(hours=7))
                cap_nhat_luc = datetime.now(gio_vn).isoformat()
                lan_tai_cuoi = monotonic()

            except (requests.RequestException, ValueError):
                return jsonify({
                    "bai_viet": cac_bai,
                    "cap_nhat_luc": cap_nhat_luc,
                    "loi": "Chưa lấy được tin mới. Bạn thử lại sau nhé."
                }), 503

        return jsonify({
            "bai_viet": cac_bai,
            "cap_nhat_luc": cap_nhat_luc,
            "loi": None
        })


@app.get("/health")
def health():
    return "OK", 200

@app.get("/sw.js")
def service_worker():
    response = send_from_directory(
        app.static_folder,
        "sw.js",
        mimetype="application/javascript"
    )

    response.headers["Cache-Control"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)