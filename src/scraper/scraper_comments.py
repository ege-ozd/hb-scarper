import time
from bs4 import BeautifulSoup


def get_product_reviews(driver, base_url, max_pages=30):
    all_reviews = []

    # 1. URL Temizleme ve Hazırlama
    clean_url = base_url.split('?')[0]
    if not clean_url.endswith("-yorumlari"):
        clean_url = clean_url + "-yorumlari"

    for page_num in range(1, max_pages + 1):
        
        page_url = f"{clean_url}?sayfa={page_num}"
        print(f"Yorumlar: Sayfa {page_num} deneniyor -> {page_url}")

        driver.get(page_url)
        time.sleep(5)  # Sayfanın render edilmesi için süre

        # Sayfayı kaydırarak içeriği tetikle
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Yorum kartlarını bul
        cards = soup.find_all("div", class_=lambda x: x and x.startswith("hermes-ReviewCard-module-"))

        if not cards:
            print(f"Sayfa {page_num} boş çıktı, yorumlar bitmiş olabilir.")
            break

        page_count = 0
        for card in cards:
            # --- YILDIZ (PUAN) HESAPLAMA ---
            rating = 0
            
            # class ismi 'hermes-RatingPointer-module-' ile başlayan div'i arıyoruz
            rating_container = card.find("div", class_=lambda x: x and x.startswith("hermes-RatingPointer-module-"))

            if rating_container:
                # İçindeki 'star' sınıfına sahip div'leri sayıyoruz
                full_stars = rating_container.find_all("div", class_="star")
                rating = len(full_stars)
            else:
                rating = "N/A"  # Eğer yıldız div'i yoksa

            # --- YORUM METNİ ---
            span_text = card.find("span", style=lambda s: s and "text-align:start" in s)

            if span_text:
                comment = span_text.get_text(strip=True)
                if len(comment) > 10:
                    # Mükerrer kontrolü
                    if not any(r['yorum'] == comment for r in all_reviews):
                        all_reviews.append({
                            "yorum": comment,
                            "puan": rating  # Puanı buraya ekledik
                        })
                        page_count += 1

        print(f"Sayfa {page_num} bitti. {page_count} yeni yorum eklendi.")

        if page_count == 0 and page_num > 1:
            print("Sürekli aynı sayfa geliyor veya yeni yorum yok. Durduruldu.")
            break

    return all_reviews
