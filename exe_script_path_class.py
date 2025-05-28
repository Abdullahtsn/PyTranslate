import os
import sys

class ExeScriptPath:               
    _instance = None            
                                
    def __new__(cls):          
                                
        if cls._instance is None:
            cls._instance = super(ExeScriptPath, cls).__new__(cls)          
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  #sys._meipas sadece pyintallerde var . onun çıkardığı geçici klasörün yolu bu.
                                                                            #eğer nuitkada yaparsan exeyi orda yol alma farklı çalışıyor direk geçici klasör yolu alma yok orda.
                                                                            #eğer exenin içindeki belgelere ulaşmak istersen Nuitkanın pkgutil.get_data() modülüne bak . bu ömülü dosyaları okumak için kullanılır.yada pythonun kendi modülü olan importlib.resources kullanman gerekir.
                cls._instance.path_temp = sys._MEIPASS                      #pyinstaller için exenin içinin çıkarıldığı geçici klasör
                cls._instance.path_exe = os.path.dirname(sys.executable)    #exenin o an bulunduğu çalıştırıldığı konum
            else:
                cls._instance.path_temp = os.path.dirname(os.path.abspath(__file__))       #eğer exe değilde py scripti çalıştırılıyorsa konumu o py scriptiin bulunmasına göre ayarlıyor
                cls._instance.path_exe = os.path.dirname(os.path.abspath(__file__))
        return cls._instance
    
    
    def paths(self):   #bu sınıfı oluşturcağımız yerde direk bunu çağırıyoruz. değerleri döndürüyor. oluşturduğumuz yerde hepsini tek tek vermekle uğraşmıyoruz.
        return self.path_temp, self.path_exe
