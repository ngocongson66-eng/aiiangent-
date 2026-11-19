import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler

# Đảm bảo thư mục gốc dự án nằm trong sys.path để import server và src
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from server import RequestHandler

class handler(RequestHandler):
    """
    Entrypoint Serverless Function chuẩn mực dành riêng cho Vercel (@vercel/python).
    Kế thừa RequestHandler của server.py và hỗ trợ rewrite URL thông minh.
    """
    def get_real_path(self):
        # Vercel truyền URL gốc của người dùng qua các header x-forwarded-uri hoặc x-matched-path
        real = (
            self.headers.get("x-forwarded-uri")
            or self.headers.get("x-matched-path")
            or self.headers.get("x-vercel-matched-path")
            or self.path
        )
        return real

    def do_GET(self):
        real_path = self.get_real_path()
        if real_path and real_path not in ["/api/index.py", "/api/index", "/api"]:
            self.path = real_path
        elif self.path in ["/api/index.py", "/api/index", "/api"]:
            self.path = "/"
        return super().do_GET()

    def do_POST(self):
        real_path = self.get_real_path()
        if real_path and real_path not in ["/api/index.py", "/api/index", "/api"]:
            self.path = real_path
        return super().do_POST()

    def do_OPTIONS(self):
        return super().do_OPTIONS()

    def do_HEAD(self):
        real_path = self.get_real_path()
        if real_path and real_path not in ["/api/index.py", "/api/index", "/api"]:
            self.path = real_path
        elif self.path in ["/api/index.py", "/api/index", "/api"]:
            self.path = "/"
        return super().do_HEAD()

# Export alias tương thích cả hai kiểu nhận diện của Vercel
app = handler
