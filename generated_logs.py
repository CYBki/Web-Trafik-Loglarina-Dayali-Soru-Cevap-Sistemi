import random
from datetime import datetime, timedelta


def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"


def generate_timestamp():
    start_date = datetime(2023, 8, 15, 8, 0, 0)
    random_seconds = random.randint(0, 86400)
    return (start_date + timedelta(seconds=random_seconds)).strftime("[%d/%b/%Y:%H:%M:%S +0300]")


def generate_method():
    return random.choice(["GET", "POST", "PUT", "DELETE"])


def generate_path():
    paths = ["/index.html", "/login", "/images/logo.png", "/api/users", "/products", "/favicon.ico", "/api/comments",
             "/css/main.css", "/blog", "/nonexistent-page", "/about", "/contact", "/api/products/1234"]
    return random.choice(paths)


def generate_status_code():
    return random.choice([200, 201, 204, 301, 302, 304, 400, 401, 403, 404, 500])


def generate_size():
    return random.randint(100, 10000)


def generate_referer():
    referers = ["https://www.google.com", "http://example.com", "https://www.bing.com", "http://example.com/login",
                "http://example.com/blog/post-1", "-"]
    return random.choice(referers)


def generate_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
    ]
    return random.choice(user_agents)


def generate_log_entry():
    ip = generate_ip()
    timestamp = generate_timestamp()
    method = generate_method()
    path = generate_path()
    protocol = "HTTP/1.1"
    status = generate_status_code()
    size = generate_size()
    referer = generate_referer()
    user_agent = generate_user_agent()

    return f'{ip} - - {timestamp} "{method} {path} {protocol}" {status} {size} "{referer}" "{user_agent}"'

file_path = r"log_path"

with open(file_path, "w") as f:
    for _ in range(1200):
        log_entry = generate_log_entry()
        f.write(log_entry + "\n")

print("1200 adet log girişi oluşturuldu ve 'access.log' dosyasına kaydedildi.")
