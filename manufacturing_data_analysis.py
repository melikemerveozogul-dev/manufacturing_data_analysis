import pandas as pd
import matplotlib.pyplot as plt

try:
    # Veriyi oku
    df = pd.read_csv('ai4i2020.csv')
    df.to_excel('uretim_analiz_sonuc.xlsx', index=False)
    
    # Hata analizleri
    hata_sutunlari = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']
    hata_toplamlari = df[hata_sutunlari].sum().sort_values(ascending=False)
    
    print("\n--- GÜNLÜK ÜRETİM HATA RAPORU ---")
    print(hata_toplamlari)
    
    # Metrik hesaplamaları
    toplam_uretim = len(df)
    toplam_hata = hata_toplamlari.sum()
    basarili_uretim = toplam_uretim - toplam_hata
    verimlilik_orani = (basarili_uretim / toplam_uretim) * 100
    hata_yuzdesi = (toplam_hata / toplam_uretim) * 100
    
    print(f"\nToplam Üretim: {toplam_uretim} Adet")
    print(f"Hatalı Parça: {toplam_hata} Adet")
    print(f"Genel Verimlilik: %{verimlilik_orani:.2f}")
    print(f"Hata Oranı: %{hata_yuzdesi:.2f}")
    print("-" * 30)
    
    # Grafik oluşturma
    plt.figure(figsize=(10, 6))
    hata_toplamlari.plot(kind='bar', color='red', edgecolor='black')
    
    # Barların üzerine sayıları ekleme (Hata veren kısım burasıydı, hizalamaya dikkat)
    for i, v in enumerate(hata_toplamlari):
        plt.text(i, v + 0.5, str(int(v)), ha='center', fontweight='bold')
        
    plt.title('Hata Tiplerine Göre Duruş Sayıları')
    plt.xlabel('Hata Kategorisi')
    plt.ylabel('Adet')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Kaydet ve Göster
    plt.savefig('uretim_grafigi.png')
    print("\n✅ Grafik 'uretim_grafigi.png' olarak kaydedildi.")
    plt.show()

except Exception as e:
    print(f"Hata oluştu: {e}")