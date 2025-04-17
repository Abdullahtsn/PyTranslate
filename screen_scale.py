import pyautogui


class ScreenSize:       #genel özet ; sadece bir kere hesaplanıcak değer olursa bunu new fonksiyonuyla classlar oluşmadan önce hesaplıyoruz ve kaydediyoruz. cls new fonksiyonunda kullanılıyor. tıpkı initte self kullanılması gibi. ve new fonksiyonu initten önce çalıştırılıyor ve başarılı olursa ondan sonra init fonksiyonu çalıştırılıyor. tek bir nesne kaydediceksek pythonda genel kabul görmüş değişken ismi _instanceye atıyoruz bunu. kural değil ama genel kullanım böyle. 
    _instance = None    #bu kural değil ama python için genel kabul görmüş bişey. Tüm sınıfın tek örneğini sakladığımız yer. yani bu sınıftan bir sürü oluştursakta sadece ilk ölçü alınırken hesaplama yapılcak,
                        #sonrakiler bu ilk ölçümü kullanıcak. bu yönteme singleton deniyor. bişeyi sınıf düzeyinde tanımlayıp hep onu kullanıyoruz ve sadece bir kere tanımlama yapılıyor. diğer classlarda bu ilk tanımlanıp kaydedileni kullanıyor.
    def __new__(cls):      #bu new methodu classların sabit fonksiyonlarından biri pythonda. bu cls kısmı new fonksiyonuna özel. def initteki self gibi düşün.
                        #def init gibi. ama initten bile önce çalışıyor. def init fonksiyonu eğer bu new fonksiyonu başarılı olursa çalışır.
        if cls._instance is None:
            cls._instance = super(ScreenSize, cls).__new__(cls)     #Bu, Singleton deseninde sadece bir tane nesne yaratılmasını garanti eder. Eğer _instance zaten oluşturulmuşsa, tekrar bir nesne yaratılmayacak. eğer mantığını unutursan initteki super gibi. self yerlerine cls, init yerlerine new yazılıyor.
            w, h = pyautogui.size()         #genişlik, yükseklik

            if (w,h) in [(1280, 720) ,(1366, 768), (1280, 1024), (1600, 1200)]:
                cls._instance = 1
            elif (w,h) in [(1920, 1080), (1920, 1200)]:
                cls._instance = 1.5
            elif (w, h) in [(2560, 1440), (2560, 1600), (3440, 1440)]:
                cls._instance = 2
            elif (w, h) == (3840, 2160):
                cls._instance = 3
            elif (w, h) == (5120, 2880):
                cls._instance = 4
            elif (w, h) == (7680, 4320):
                cls._instance = 6
            else:
                cls._instance = 2
            return w, h, cls._instance
        