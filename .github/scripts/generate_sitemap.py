#!/usr/bin/env python3
import os
import json
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

BASE_URL = "https://tugledaydinlatma.github.io/led-bant-armatur-rehberi"
ARSIV_DIR = "Arsiv"
ARTICLES_FILE = "articles.json"

def generate_sitemap():
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
    
    # Ana sayfa
    add_url(urlset, BASE_URL + "/", "1.0", "daily")
    
    # Arsiv sayfaları
    if os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        for article in articles:
            file_path = article.get('file', '')
            date = article.get('date', datetime.now().strftime('%Y-%m-%d'))
            if file_path:
                url = BASE_URL + "/" + file_path.replace('\\', '/')
                add_url(urlset, url, "0.8", "weekly", date)
    
    # XML'i güzelleştir
    rough_string = tostring(urlset, 'utf-8')
    reparsed = parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8")
    
    # Dosyaya yaz
    with open('sitemap.xml', 'wb') as f:
        f.write(pretty_xml)
    
    print(f"✅ sitemap.xml oluşturuldu! Toplam {len(urlset)} URL.")

def add_url(urlset, loc, priority, changefreq, lastmod=None):
    url = SubElement(urlset, 'url')
    loc_elem = SubElement(url, 'loc')
    loc_elem.text = loc
    
    if lastmod:
        lastmod_elem = SubElement(url, 'lastmod')
        lastmod_elem.text = lastmod
    
    changefreq_elem = SubElement(url, 'changefreq')
    changefreq_elem.text = changefreq
    
    priority_elem = SubElement(url, 'priority')
    priority_elem.text = priority

if __name__ == "__main__":
    generate_sitemap()
