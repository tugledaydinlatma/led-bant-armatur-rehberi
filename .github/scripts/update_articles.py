#!/usr/bin/env python3
import os
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

ARSIV_DIR = "Arsiv"
OUTPUT_FILE = "articles.json"

def extract_meta_from_html(filepath):
    """HTML dosyasından meta verileri çek"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else os.path.basename(filepath)
        
        # Meta description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        description = desc_tag.get('content', '') if desc_tag else ''
        
        # Meta date
        date_tag = soup.find('meta', attrs={'name': 'date'})
        date = date_tag.get('content', datetime.now().strftime('%Y-%m-%d')) if date_tag else datetime.now().strftime('%Y-%m-%d')
        
        # Meta category
        cat_tag = soup.find('meta', attrs={'name': 'category'})
        category = cat_tag.get('content', 'Genel') if cat_tag else 'Genel'
        
        # H1 başlığı varsa onu kullan
        h1_tag = soup.find('h1')
        if h1_tag:
            title = h1_tag.get_text().strip()
        
        return {
            "title": title,
            "description": description,
            "date": date,
            "category": category,
            "file": filepath.replace("\\", "/")
        }
    except Exception as e:
        print(f"Hata: {filepath} - {e}")
        return None

def main():
    articles = []
    
    if not os.path.exists(ARSIV_DIR):
        print(f"{ARSIV_DIR} klasörü bulunamadı!")
        return
    
    # Arsiv klasöründeki tüm HTML dosyalarını tara
    for filename in sorted(os.listdir(ARSIV_DIR)):
        if filename.endswith('.html'):
            filepath = os.path.join(ARSIV_DIR, filename)
            article = extract_meta_from_html(filepath)
            if article:
                articles.append(article)
                print(f"✅ Eklendi: {article['title']}")
    
    # Tarihe göre sırala (en yeni en üstte)
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # JSON'u yaz
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 {OUTPUT_FILE} güncellendi! Toplam {len(articles)} yazı.")

if __name__ == "__main__":
    main()
