import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup

# Modüllerimizi içeri aktarıyoruz
import scraper_comments
import scraper_qna

# 20 Ürünlük URL Listesi
urls = [
    "https://www.hepsiburada.com/3000-serisi-airfryer-large-rapid-air-teknolojisi-4-1-lt-kapasite-7-ayarli-dokunmatik-ekran-sicak-tutma-ozelligi-hd9243-90-pm-HBC00004OVGX1",
    "https://www.hepsiburada.com/xiaomi-mi-air-fryer-6l-fritoz-siyah-sicak-hava-fritozu-pisirme-buz-cozme-fermantasyon-dokunmatik-pm-HBC00007R1ARZ",
    "https://www.hepsiburada.com/neutron-smart-air-fryer-pro-7-3-l-tek-hazneli-yagsiz-fritoz-cikarilabilir-kapakli-enerji-tasarruflu-ve-kolay-temizlenir-p-HBCV000049EHA2?magaza=Whirtz%20T%C3%BCrkiye",
    "https://www.hepsiburada.com/yui-m45-8-litre-4-4-seramik-cift-hazneli-smart-airfryer-fritoz-siyah-p-HBCV00004MJGY6?magaza=MarkaDepo",
    "https://www.hepsiburada.com/3000-serisi-airfryer-cift-hazneli-rapid-air-plus-teknolojisi-8-ayarli-dijital-ekran-homeid-uygulamasi-na350-00-pm-HBC000062ZPFZ",
    "https://www.hepsiburada.com/xiaomi-mi-smart-airfryer-3-5-l-pm-HBC00000PVC2V",
    "https://www.hepsiburada.com/wiami-12l-yagsiz-hava-fritozu-tek-hazneli-led-ekranli-mekanik-kontrollu-saglikli-ve-pratik-pisirme-cihazi-p-HBCV00003MS94G?magaza=MarkaDepo",
    "https://www.hepsiburada.com/robwell-as28-airfryer-halojen-isi-sistemli-sesli-uyari-xl-yagsiz-hava-fritozu-robx-turkiye-garantili-pm-HBC00005BTNPV",
    "https://www.hepsiburada.com/philips-avance-collection-hd9650-90-xxl-airfryer-7-3-lt-tek-hazneli-yagsiz-pisirme-ve-otomatik-kapanma-ozellikli-fritoz-pm-HB00000DGBRG",
    "https://www.hepsiburada.com/xiaomi-akilli-yagsiz-fritoz-6-5-litre-tek-hazne-enerji-tasarruflu-hizli-isinma-ve-cikarilabilir-hazne-pm-HBC0000546FWY",
    "https://www.hepsiburada.com/rossclean-cook-fresh-5-5-lt-dijital-airfryer-fritoz-p-HBCV00003VZHCK?magaza=RossClean%20T%C3%BCrkiye",
    "https://www.hepsiburada.com/tefal-easy-fry-xl-surface-4-litre-2200-watt-super-kompakt-boyutlu-genis-air-fryer-fritoz-pm-HBC00009HL9FH",
    "https://www.hepsiburada.com/rossclean-cook-active-5-5l-dijital-airfryer-fritoz-p-HBCV00003VZI5H?magaza=RossClean%20T%C3%BCrkiye",
    "https://www.hepsiburada.com/xiaomi-air-fryer-4-litre-beyaz-pro-akilli-fritoz-pm-HBC00005CPWOD",
    "https://www.hepsiburada.com/philips-hd9285-96-5000-serisi-airfryer-xxl-connected-7-2-l-1-4-kg-rapid-air-teknolojisi-pisirme-ve-izgara-aksesuarlari-pm-HBC000040CBJY",
    "https://www.hepsiburada.com/altus-ecofryer-xl-al-2983-af-airfryer-pm-HBC00004U8VSF",
    "https://www.hepsiburada.com/onvo-ovfry13-8l-alt-ust-cift-rezistansli-seramik-kaplama-desenli-airfryer-pm-HBC00007IL0ME",
    "https://www.hepsiburada.com/kumtel-digital-fastfryer-haf-02-yagsiz-fritoz-airfryer-pm-HBC00002OX66W",
    "https://www.hepsiburada.com/luxell-5-5-lt-yagsiz-sicak-hava-fritozu-tek-hazneli-sokulebilir-ust-kapak-enerji-tasarruflu-ve-kolay-temizlik-pm-HBC00002TGQ5G",
    "https://www.hepsiburada.com/karaca-9-litre-ekstra-buyuk-hacimli-airfryer-8-kisilik-kapasite-aile-ve-kalabalik-sofralar-icin-ideal-pm-HBC00007P2WU4"
]

# Çıktı klasörünü ayarla
if not os.path.exists('data'):
    os.makedirs('data')

# Tarayıcıyı Hazırla
options = webdriver.FirefoxOptions()
# options.add_argument("--headless") 
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0")

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
driver.maximize_window()

try:
    for index, url in enumerate(urls, 1):
        try:
            print(f"\n[{index}/{len(urls)}] İşlem Başlıyor...")
            driver.get(url)
            time.sleep(5)

            # 1. Ürün Başlığı ve ID Yakalama
            soup_main = BeautifulSoup(driver.page_source, "html.parser")
            title_tag = soup_main.find("h1", attrs={"data-test-id": "title"})
            product_title = title_tag.get_text(strip=True) if title_tag else "Başlık Bulunamadı"

            # Ürün ID'sini temizleme (URL karmaşasından kurtarma)
            product_id = url.split("-pm-")[-1].split("?")[0] if "-pm-" in url else "Bilinmiyor"

            print(f"ÜRÜN: {product_title[:50]}...")
            print(f"ID: {product_id}")

            # 2. Yorumları Çek ve Anlık Kaydet
            print("Yorumlar toplanıyor (Max 30 Sayfa)...")
            reviews = scraper_comments.get_product_reviews(driver, url, max_pages=40)
            if reviews:
                for r in reviews:
                    r['product_id'] = product_id
                    r['product_name'] = product_title
                    r['source_url'] = url

                df_temp_rev = pd.DataFrame(reviews)
                file_exists = os.path.isfile('data/tum_yorumlar.csv')
                # Append modunda kaydet (mode='a'), UTF-16 Excel uyumu içindir
                df_temp_rev.to_csv('data/tum_yorumlar.csv', mode='a', index=False, header=not file_exists, encoding="utf-16")
                print(f"BAŞARILI: {len(reviews)} yorum dosyaya eklendi.")
            else:
                print("Hata: Hiç yorum çekilemedi.")

            # 3. Soru-Cevapları Çek ve Anlık Kaydet
            print("Soru-Cevaplar toplanıyor...")
            qnas = scraper_qna.get_product_qna(driver, url)
            if qnas:
                for q in qnas:
                    q['product_id'] = product_id
                    q['product_name'] = product_title
                    q['source_url'] = url

                df_temp_qna = pd.DataFrame(qnas)
                file_exists_qna = os.path.isfile('data/tum_soru_cevaplar.csv')
                df_temp_qna.to_csv('data/tum_soru_cevaplar.csv', mode='a', index=False, header=not file_exists_qna, encoding="utf-16")
                print(f"BAŞARILI: {len(qnas)} soru-cevap dosyaya eklendi.")
            else:
                print("Bilgi: Bu ürün için soru-cevap bulunamadı.")

        except Exception as inner_e:
            print(f"!!! {url} işlenirken bir sorun çıktı, sonraki ürüne geçiliyor: {inner_e}")
            continue

    print(f"\n{'='*50}\nTÜM PROSES TAMAMLANDI! Dosyalar 'data/' klasöründe.")

finally:
    driver.quit()
