import pandas as pd
import time
import os

dosya_adi = 'ai4i2020.csv'

def canli_akıs_sistemi():
    try:
        df = pd.read_csv(dosya_adi)
        veriler = df.tail(30)

        # Sayaçlar (İstatistik tutmak için)
        toplam_ariza = 0
        kritik_sicaklik_sayisi = 0

        print("--- SİSTEM BAŞLATILIYOR ---")
        time.sleep(1)

        for i in range(len(veriler)):
            os.system('cls' if os.name == 'nt' else 'clear')
            satir = veriler.iloc[i]
            
            # Değerleri alalım
            sicaklik = satir['Air temperature [K]']
            ariza = satir['Machine failure']
            
            # Sayaçları güncelleyelim
            if ariza == 1: toplam_ariza += 1
            if sicaklik > 301: kritik_sicaklik_sayisi += 1

            print("******************************************")
            print("       MES ANLIK ÜRETİM TAKİP HATTI       ")
            print("******************************************")
            print(f"SIRA NO    : {i+1}/30")
            print(f"ÜRÜN KODU  : {satir['Product ID']}")
            print(f"SICAKLIK   : {sicaklik} K")
            print(f"TORK       : {satir['Torque [Nm]']} Nm")
            
            if ariza == 1:
                print("\n[!!! ALARM: ARIZA !!!]")
            elif sicaklik > 301:
                print("\n[UYARI: YÜKSEK ISI]")
            else:
                print("\n[DURUM: STABİL]")
            
            print("******************************************")
            time.sleep(0.5) # Hızlıca aksın diye süreyi kısalttım

        # --- SİMÜLASYON BİTTİĞİNDE ÇALIŞACAK KISIM ---
        print("\n\n" + "="*40)
        print("      VARDİYA SONU ÖZET RAPORU        ")
        print("="*40)
        print(f"İncelenen Toplam Parça : 30")
        print(f"Tespit Edilen Arıza    : {toplam_ariza}")
        print(f"Kritik Isınma Vakası   : {kritik_sicaklik_sayisi}")
        print(f"Verimlilik Puanı       : %{((30-toplam_ariza)/30)*100:.1f}")
        print("="*40)

    except Exception as e:
        print(f"Hata oluştu: {e}")

canli_akıs_sistemi()