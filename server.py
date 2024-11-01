import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # 添加 CORS 头，允许跨域访问
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        """处理 GET 请求，添加正确的编码设置"""
        # 设置响应头
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 读取并发送文件内容
            try:
                with open(os.path.join(DIRECTORY, self.path.lstrip('/')), 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_error(404, str(e))
        else:
            # 对于其他类型的文件，使用默认处理
            super().do_GET()

def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"服务器运行在 http://localhost:{PORT}")
        print(f"可以通过局域网 IP 访问：http://[你的IP地址]:{PORT}")
        print("按 Ctrl+C 停止服务器")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()