#!/usr/bin/env python3
import urllib.request
import sys

SITEMAP_URL = "https://tugledaydinlatma.github.io/led-bant-armatur-rehberi/sitemap.xml"

def ping_google():
    try:
        url = f"http://www.google.com/ping?sitemap={SITEMAP_URL}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            print(f"✅ Google ping gönderildi! Status: {response.status}")
            return True
    except Exception as e:
        print(f"⚠️ Google ping hatası: {e}")
        return False

def ping_bing():
    try:
        url = f"http://www.bing.com/ping?sitemap={SITEMAP_URL}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            print(f"✅ Bing ping gönderildi! Status: {response.status}")
            return True
    except Exception as e:
        print(f"⚠️ Bing ping hatası: {e}")
        return False

if __name__ == "__main__":
    ping_google()
    ping_bing()
