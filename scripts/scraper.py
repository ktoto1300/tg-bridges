import requests
import json
import socket
import time
import os
import re
import html

# Конфигурация
TIMEOUT = 5
OUTPUT_FILE = "bridges.json"
VERSION_FILE = "version.json"

# Каналы для поиска прокси (MTProto/Socks5)
# Теперь мы ищем не Tor-мосты, а прокси
TG_CHANNELS = [
    "https://t.me/s/ProxyMTProto",
    "https://t.me/s/Mypublic_proxy",
    "https://t.me/s/TelMTProto"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_proxies():
    """
    Парсинг MTProto прокси из публичных Telegram-каналов.
    """
    print("Поиск прокси в Telegram-каналах...")
    found_proxies = set()
    
    # Регулярка для MTProto ссылок
    proxy_pattern = re.compile(r'https?:\/\/t\.me\/proxy\?server=[^&\s]+&port=[0-9]+&secret=[^&\s]+')

    for url in TG_CHANNELS:
        try:
            print(f"Парсинг {url}...")
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                matches = proxy_pattern.findall(response.text)
                for match in matches:
                    found_proxies.add(html.unescape(match.strip()))
                    
            print(f"Найдено прокси на {url}: {len(found_proxies)}")
        except Exception as e:
            print(f"Ошибка при парсинге {url}: {e}")
            
    return list(found_proxies)

def main():
    print("Запуск Proxy Scraper v1.0...")
    
    raw_proxies = fetch_proxies()
    
    # Сохраняем в bridges.json (оставляем имя файла для совместимости с модом)
    # Но внутри теперь лежат MTProto ссылки
    bridges_data = {
        "updated_at": int(time.time()),
        "count": len(raw_proxies),
        "bridges": raw_proxies
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(bridges_data, f, indent=4)
        
    print(f"Итог: Сохранено {len(raw_proxies)} прокси в {OUTPUT_FILE}.")

    # Создаем/Обновляем version.json
    version_data = {
        "latest_version": "1.0.0",
        "update_url": "https://ktoto1300.github.io/ProxyGram/",
        "changelog": "Переход на ProxyGram: автоматические быстрые прокси!",
        "force_update": False,
        "update_message": "Нажмите здесь, чтобы скачать новую версию ProxyGram.",
        "support_url": "https://t.me/proxys1488",
        "support_interval_hours": 24,
        "support_message": "Здравствуйте, будем рады если вступите ко мне в телеграмм канал для поддержки приложения!"
    }
    with open(VERSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=4)

if __name__ == "__main__":
    main()
