from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import os

def load_proxy(proxy_path: str) -> str:
    if os.path.exists(proxy_path):
        with open(proxy_path, 'r') as file:
            proxy_url = file.readline().rstrip()
            return proxy_url

    return None

def save_proxy(proxy_path: str, proxy_url: str):
    if "http" in proxy_url:
        split = proxy_url.split("://")
        proxy_url = split[1]

    ensure_valid_proxy(proxy_url)
    with open(proxy_path, 'w') as file:
        file.write(proxy_url)

def setup_driver_with_proxy(service: Service, proxy_url: str, options: Options, session_path: str):
    """
        proxy_url: str in the following format: <USERNAME>:<PASSWORD>@<IP>:<PORT>
    """

    ensure_valid_proxy(proxy_url)

    seleniumwire_options = {
        "proxy": {
            "http": f"http://{proxy_url}",
            "https": f"http://{proxy_url}"
        },
    }

    driver = webdriver.Chrome(
        service=service,
        seleniumwire_options=seleniumwire_options,
        options=options
    )

    save_proxy(proxy_path=session_path, proxy_url=proxy_url)

    return driver


def ensure_valid_proxy(s):
    try:
        # Split by '@' to separate the credentials from the IP:PORT
        credentials, ip_port = s.split('@')
        
        # Split credentials into USERNAME and PASSWORD
        username, password = credentials.split(':')
        
        # Split ip_port into IP and PORT
        ip, port = ip_port.split(':')
        
        if not username or not password:
            raise ValueError("Invalid format: Username or password is missing.")
        
        ip_parts = ip.split('.')
        if len(ip_parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_parts):
            raise ValueError("Invalid format: IP address is invalid.")        

        if not port.isdigit() or not 1 <= int(port) <= 65535:
            raise ValueError("Invalid format: Port number is invalid.")
        
        # If all validations pass
        return True
    except ValueError as e:
        raise ValueError(f"Invalid string format: {str(e)}")