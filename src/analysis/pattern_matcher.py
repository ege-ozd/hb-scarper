import re


class AirfryerPatternMatcher:
    def __init__(self):
        # Analitik değeri düşük gürültü bigramlar
        self.stop_bigrams = ["cok guzel", "tavsiye ederim", "gayet guzel", "cok iyi", "tesekkur ederim"]

    def cluster_by_pattern(self, text, puan):
        if not isinstance(text, str): return "Tanımsız"
        text = text.lower()
        tags = []

        # --- PUAN BAZLI GENEL DUYGU ---
        is_negative = puan <= 3
        is_positive = puan >= 4

        # 1. LOJİSTİK ANALİZİ
        if any(w in text for w in ["hizli geldi", "hızlı geldi", "kargo hizli", "kısa sürede", "elime ulasti"]):
            if is_negative:
                tags.append("Lojistik Şikayeti") # 1-3 puan verip hızı övmez, sorun vardır.
            else:
                tags.append("Lojistik Memnuniyeti")

        # 2. "DAHA ÖNCE" (Keşke/Pişmanlık)
        if "daha önce" in text or "daha once" in text:
            if any(w in text for w in ["keşke", "keske", "pişman", "pisman"]):
                if is_positive:
                    tags.append("Pozitif: Geç Kalınmış Memnuniyet")
                else:
                    tags.append("Negatif: Gerçek Müşteri Pişmanlığı")

        # 3. "GEREK YOK" ANALİZİ
        if "gerek yok" in text:
            # 1-2-3 puan ise her zaman "Ürün Gereksiz/Kötü"
            if is_negative:
                tags.append("Negatif: Ürün Gereksizliği")
            # 4-5 puan ise "Fiyat/Performans veya Tasarruf"
            elif any(w in text for w in ["para", "yağ", "yag", "ekstra", "fırın", "firin", "başka"]):
                tags.append("Pozitif: Verimlilik/Tasarruf")
            else:
                tags.append("Pozitif: Tavsiye")

        # 4. "DAHA İYİ" (Kıyaslama)
        if "daha iyi" in text:
            if is_negative:
                tags.append("Negatif: Performans Yetersizliği")
            elif "göre daha iyi" in text or "gore daha iyi" in text:
                tags.append("Pozitif: Rakip Üstünlüğü")
            else:
                tags.append("Pozitif: Beklenti Üstü Performans")

        # 5. "ÜRÜN ÇOK" ANALİZİ
        if "ürün çok" in text or "urun cok" in text:
            if is_negative:
                tags.append("Negatif: Ürün Şikayeti")
            else:
                tags.append("Pozitif: Genel Memnuniyet")

        # 6. HİZMET / SATICI / HEDİYE
        if any(w in text for w in ["hediye", "ince dusunceniz", "satıcı", "satici", "paketleme"]):
            if is_positive:
                tags.append("Hizmet/Satıcı Memnuniyeti")
            else:
                tags.append("Hizmet/Paketleme Şikayeti")

        # --- 7. DOĞRUDAN MEMNUNİYETSİZLİK VE İADE (YENİ) ---
        # Bu kelimeler geçiyorsa puan ne olursa olsun bir "sorun" vardır.
        direct_negative_keywords = [
            "begenmedim", "beğenmedim", "begenmedik", "beğenmedik",
            "iade ettim", "iade edecegim", "iade edeceğim", "iade ederdim",
            "sikayet ettim", "şikayet ettim", "sikayetciyim", "şikayetçiyim",
            "pismandim", "pişmanım", "pismanim", "tavsiye etmiyorum", "etmem"
        ]

        if any(w in text for w in direct_negative_keywords):
            tags.append("Doğrudan Memnuniyetsizlik / İade")

        return " | ".join(tags) if tags else "Genel Deneyim / Diğer"

    def get_context(self, text, target="gerek yok", window=5):
        # Bu fonksiyon aynı kalıyor...
        if not isinstance(text, str) or target not in text:
            return None
        words = text.split()
        target_words = target.split()
        for i in range(len(words) - len(target_words) + 1):
            if words[i:i + len(target_words)] == target_words:
                start = max(0, i - window)
                end = min(len(words), i + len(target_words) + window)
                return " ".join(words[start:end])
        return None