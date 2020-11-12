import sqlite3
import time
import datetime

class URUN():

    def __init__ (self,mal_ad,mal_kod,mal_fiyat,mal_son_kullanma_tarih):

        self.mal_ad=mal_ad
        self.mal_kod=mal_kod
        self.mal_fiyat=mal_fiyat
        self.mal_son_kullanma_tarih=mal_son_kullanma_tarih

    def __str__ (self):

        return("Ürünün Adı: {}\nÜrünün Kodu: {}\nÜrünün Fiyatı: {}\nÜrünün Son Kullanma Tarihi: {}\n".format(self.mal_ad,self.mal_kod,self.mal_fiyat,self.mal_son_kullanma_tarih))

class MARKET():

    def __init__ (self):

        self.baglanti_olustur()
    
    def baglanti_olustur(self):

        self.baglanti=sqlite3.connect("Market.db")
        self.cursor=self.baglanti.cursor()
        sorgu="Create Table if Not Exists Urunler(Ad TEXT,Kod INT,Fiyat INT,Kullanma INT)"
        self.cursor.execute(sorgu)
        self.baglanti.commit()
    
    def baglanti_kes(self):

        self.baglanti.close()
    
    def urunleri_goster(self):

        sorgu="Select *From Urunler"
        self.cursor.execute(sorgu)
        list=self.cursor.fetchall()
        if len(list)==0:
            print("Ürün Bulunmamaktadır")
        else:
            for i in list:
                urun=URUN(i[0],i[1],i[2],i[3])
                print("\n")
                print(urun)
    
    def urun_sorgula(self):

        mal_ad=input("Hangi Ürünü Sorgulamak İstiyorsunuz?:")
        print("Sorgulanıyor...")
        time.sleep(2)
        sorgu="Select *From Urunler where Ad=?"
        self.cursor.execute(sorgu,(mal_ad,))
        list=self.cursor.fetchall()
        if len(list)==0:
            print("Bu Ürün Bulunmamaktadır")
        else:
            for i in list:
                urun=URUN(list[0][0],list[0][1],list[0][2],list[0][3])
                print("\n")
                print(urun)
    
    def urun_ekle(self,urun):

        sorgu="Insert Into Urunler values(?,?,?,?)"
        self.cursor.execute(sorgu,(urun.mal_ad,urun.mal_kod,urun.mal_fiyat,urun.mal_son_kullanma_tarih))
        self.baglanti.commit()
    
    def urun_sil(self):

        mal_ad=input("Hangi Ürünü Silmek İstiyorsunuz?:")
        sorgu="Select *From Urunler where Ad=?"
        self.cursor.execute(sorgu,(mal_ad,))
        list=self.cursor.fetchall()
        if(len(list)==0):
            print("Böyle Bir Ürün Bulunmadığından Silemezsiniz")
        else:
            sorgu2="Delete From Urunler where Ad=?"
            self.cursor.execute(sorgu2,(mal_ad,))
            print("Siliniyor")
            i=0
            while(i<5):
                print(" ",end=".",flush=True)
                time.sleep(0.5)
                i+=1
            print("\n")
            print("Silindi")
            self.baglanti.commit()

    def zam_yap(self):

        mal_ad=input("Hangi Ürüne Zam Yapmak İstiyorsunuz?:")
        sorgu="Select *From Urunler where Ad=?"
        self.cursor.execute(sorgu,(mal_ad,))
        list=self.cursor.fetchall()
        if(len(list))==0:
            print("Bu Ürün Bulunmamaktadır")
        else:
            for i in list:
                zam_miktarı=float(input("Zam Yapılacak Miktarı Giriniz:"))
                mal_fiyat=list[0][2]
                mal_fiyat+=zam_miktarı
                sorgu2="Update Urunler set Fiyat=? where Ad=?"
                self.cursor.execute(sorgu2,(mal_fiyat,mal_ad))
                print("Zam Yapılıyor...")
                time.sleep(2)
                print("{} Ürününün Yeni Fiyatı: {} TL".format(mal_ad,mal_fiyat))
                self.baglanti.commit()
    
    def fiyat_dusur(self):

        mal_ad=input("Hangi Ürünün Fiyatını Düşürmek İstiyorsunuz?:")
        print("Sistem Kontrol Ediliyor...")
        time.sleep(2)
        sorgu="Select *From Urunler where Ad=?"
        self.cursor.execute(sorgu,(mal_ad,))
        list=self.cursor.fetchall()
        if(len(list)==0):
            print("Bu Ürün Mevcut Değil")
        else:
            for i in list:
                indirim=float(input("Düşürülecek Miktar:"))
                print("Hesaplanıyor...")
                time.sleep(2) 
                mal_fiyat=list[0][2]
                mal_fiyat-=indirim
                sorgu2="Update Urunler set Fiyat=? where Ad=?"
                self.cursor.execute(sorgu2,(mal_fiyat,mal_ad))
                self.baglanti.commit()
                print("Ürünün Yeni Fiyatı: {}".format(mal_fiyat))
                print("Fiyat Güncellendi.")
    
    def son_kullanma_tarihi_guncelle(self):

        mal_ad=input("Hangi Ürünün Kullanma Tarihini Güncellemek İstiyorsunuz?:")
        sorgu="Select *From Urunler where Ad=?"
        self.cursor.execute(sorgu,(mal_ad,))
        list=self.cursor.fetchall()
        if(len(list))==0:
            print("Bu Ürün Mevcut Değil")
        else:
            mal_son_kullanma_tarih=list[0][3]
            tarih=input("Yeni Tarih:")
            print("Güncelleniyor...")
            time.sleep(2)
            mal_son_kullanma_tarih=tarih
            sorgu2="Update Urunler set Kullanma=? where Ad=?"
            self.cursor.execute(sorgu2,(mal_son_kullanma_tarih,mal_ad))
            print("{} Ürünün Güncel Tarihi:{}".format(mal_ad,tarih))
            self.baglanti.commit()
    
    def kodunu_degistir(self):

        mal_ad=input("Hangi Ürünün Kodunu Değiştirmek İstiyorsunuz?:")
        sorgu="Select *From Urunler where Ad=?"
        self.cursor.execute(sorgu,(mal_ad,))
        list=self.cursor.fetchall()
        if len(list)==0:
            print("Ürün Mevcut Değil")
        else:
            mal_kod=list[0][1]
            kod=int(input("Ürünün Kodu:"))
            print("Kodu Güncelleniyor...")
            time.sleep(2)
            sorgu2="Update Urunler set Kod=? where Ad=?"
            self.cursor.execute(sorgu2,(kod,mal_ad))
            print("{} Ürünün Yeni Kodu:{}".format(mal_ad,kod))
            self.baglanti.commit()

print(""" 
           ----MARKET----

1.)Ürün Göster
2.)Ürün Sorgula
3.)Ürün Ekle
4.)Ürün Sil
5.)Ürünün Fiyatına Zam Yap
6.)Ürünün Fiyatını Düşür
7.)Ürünün Son Kullanma Tarihini Güncelle
8.)Ürünün Kodunu Değiştir

(Çıkış='q')

""")

market=MARKET()

while True:

    işlem=input("İşlem Seçiniz:")

    if(işlem=="1"):  
        market.urunleri_goster()
    
    elif(işlem=="2"):
        market.urun_sorgula()
    
    elif(işlem=="3"):
        mal_ad=input("Ürün İsmi:")
        mal_kod=int(input("Ürün Kodu:"))
        mal_fiyat=float(input("Ürün Fiyatı:"))
        
        print("Son Kullanma Tarihini Girin")
        yıl= int(input('Enter a year:'))
        ay= int(input('Enter a month:'))
        gün= int(input('Enter a day:'))
        tarih = datetime.date(yıl,ay,gün)
        mal_son_kullanma_tarih=tarih
       
        yeni_urun=URUN(mal_ad,mal_kod,mal_fiyat,mal_son_kullanma_tarih)
        print("Ekleniyor...")
        time.sleep(2)
        print("Eklendi")
        market.urun_ekle(yeni_urun)
    
    elif(işlem=="4"):
        market.urun_sil()
    
    elif(işlem=="5"):
        market.zam_yap()
    
    elif(işlem=="6"):
        market.fiyat_dusur()
    
    elif(işlem=="7"):
        market.son_kullanma_tarihi_guncelle()
    
    elif(işlem=="8"):
        market.kodunu_degistir()
    
    elif(işlem=="q"):
        print("Çıkış Yapılıyor...")
        time.sleep(2)
        break
    
    else:
       print("Yanlış Tuşlama Yaptınız") 