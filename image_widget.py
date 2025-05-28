import os
import io

from languages_code import tesseract_dict
from screen_scale import ScreenSize
from exe_script_path_class import ExeScriptPath

from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QApplication, QRubberBand, QListView
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QBuffer, QIODevice
from PyQt5.QtGui import  QMouseEvent, QPalette, QColor, QCursor, QPixmap, QIcon

from PIL import Image as pil_Image

import pytesseract



path_temp, path_exe = ExeScriptPath().paths()   #burda classın içinde selfle belirtmememin sebebi uygulama başlamadan önce pytesseractın yolunu veriyoruz. paketleme yaparken exenin yanında olacak dil paketleri o yüzden konumu burda alıyoruz.. yine initte tanımlamasını yapıyoruz.

pytesseract.pytesseract.tesseract_cmd = os.path.join(path_exe, 'Tesseract-OCR','tesseract.exe')


class SRubberBand(QRubberBand):
    def __init__(self,*arg,**kwargs):
        super().__init__(*arg,**kwargs)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 80, 0))    #highlight = seçim alanı için çıkan o kutu kısmı. burda onun rengini ayarlıyoruz.
        self.setPalette(palette)


class ImageWidget(QWidget):
    signal = pyqtSignal(str)
    def __init__(self, parent):
        super().__init__()
        self.main_window = parent
        self.setObjectName('i_widget')      #stylesheetde bu idyi vererek arka plan ayarlaması yapıcam  genel styleshettee.
        self.screen_w, self.screen_h, self.screen_scale = ScreenSize().values()
        self.path_temp, self.path_exe = path_temp, path_exe
        self.initial_pos = None
        self.setWindowTitle('PyTranslate Image')
        self.setWindowIcon(QIcon(QPixmap(os.path.join(self.path_temp, 'icon','icon.ico'))))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)  #bu widgeti sadece mainwindowda resim butonuna tıklanınca oluştursun, resim seçilince otomatik widgette bellekten kaldırılsın. 
                                                                #normalde mainwindowun initinde bu widgeti yapınca silinmiyor. sadece görünmez olup arka planda çalışmaya devam edip bellekte yer tutuyordu. bu bayrak sayesinde self.close() fonksiyonu her tetiklediğinde widgeti siliyor.
                                                                #yani widget işiniy aptıktan sonra tamamen siliniyor. kaynak yönetimi için çok iyi bi bayrak. sürekli kullanılmıycak widgetlere ekle bunu.
                                                                #her butona tıklanınca bu widgeti yeniden oluşturduğunu anlamanın yolu buranın initineşunu yazmak ; #print('image widget oluşturuluyor') .
                                                                
        self.setGeometry(0, 0, self.screen_w, self.screen_h)
        #self.setWindowOpacity(0.85)
        self.setContentsMargins(0,0,0,0)
        self.rubber_band = SRubberBand(QRubberBand.Shape.Rectangle, self)
        pixmap = QPixmap(os.path.join(self.path_temp, 'icon','cursor.png')).scaled(30*self.screen_scale,30*self.screen_scale, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap_hot_x = round(pixmap.width()/2)
        pixmap_hot_y = round((pixmap.height()/2) - 8*self.screen_scale)
        self.special_cursor = QCursor(pixmap, hotX = pixmap_hot_x, hotY = pixmap_hot_y)     #burdaki hotx ve hoty farenin ana tıklama noktasını belirtiyor piksel olarak. resmin hangi bölgesinin tıklama noktası olacağı kısaca.
                                                                                            #eğer hotx ve hotyyi vermezsek sol üst köşeyi tıklama noktası alıyor verdiğimiz resimin yani (0,0). bizim fare işaretçimizin okunun ucu sol üstten değil ortadan başladığı için o konumu ona veriyoruz.
        #self.setCursor(Qt.CursorShape.CrossCursor)      #kırpma işaretine çevirme
        self.setCursor(self.special_cursor)
        self.install_label()
        self.install_combobox()
        self.screen_shot()

    def install_label(self):   
        self.label = QLabel(self)
        self.label.setGeometry(self.geometry())
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def install_combobox(self):
        view = QListView() 
        view.setCursor(self.special_cursor)     #normalde bu widgetin hepsine uyguluyor cursoru ama listviewi burda oluşturduğumuz için comboboxu açınca burda fare normal varsayılanına dönüyordu listedeyken. o yüzden buna da ayrıca uyguluyoruz.
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)    #comboboxun içine scrollbar eklemek için. (comboboxa eklenen itemler fazla olunca scrolbar yerine aşağıda ve yukarda buton çıkıyor.)
        view.setViewportMargins(0,0,4*self.screen_scale,0) 
        self.combobox = QComboBox(self)
        self.combobox.setMaxVisibleItems(10)  #self.comboboxda aynı anda gösterilcek item sayısı sınırlama
        self.combobox.setView(view)
        self.combobox.setSizeAdjustPolicy(self.combobox.SizeAdjustPolicy.AdjustToContents)   
        '''self.combobox_first_item = 'Select Language'
        self.combobox.addItem(self.combobox_first_item)'''
        self.combobox.addItems(tesseract_dict.keys())
        '''self.combobox.setCurrentText(self.combobox_first_item)'''
        self.combobox.setCurrentText('English')
        self.combobox.move(round((self.screen_w/2)-(self.combobox.size().width()/2)),round((14*self.screen_scale)))                                                                
        #self.combobox.currentTextChanged.connect(self.combobox_change_language)        #burası normalde uygulama açılırken select language diye açılıyordu. bu değiştikten sonra comboboxu  gizliyorduk. ama her defasında tekrar tekrar dil seçimi yapmak yerine varsayılan olarak ingilizce kullanılıp comboboxun kaybolmasını iptal etmek  daha mantıklı geldi.
        
    def combobox_change_language(self):     #combobox değiştikten sonraki gerçekleşicek işlemler. ama şuan çalışmıyor yukarısı yorum satırı haline getirildi.
        '''remove_item = self.combobox.findText(self.combobox_first_item)   
        self.combobox.removeItem(remove_item)'''
        self.combobox.hide()      #normalde select language yazısını çıkarıyoduk başka bi seçim yapıldıktan sonra ama seçim yapıldıktan sonra comboboxu gizliyceğimiz için çıkarmaya gerek kalmadı.
        
    def screen_shot(self):
        self.main_window.hide()
        self.screen_image = QApplication.primaryScreen().grabWindow(0)
        self.label.setPixmap(self.screen_image.scaled(self.screen_w, self.screen_h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))    #setpixmap ile normalde sadece pixmap nesneleri koyabiliyoz bu fonksiyona. ama grabwindow fonksiyonu zaten qpixmap nesnesi döndürdüğü için direk verebiliyoz bunu
        self.main_window.show()

    def image_to_text(self, image):
        text = pytesseract.image_to_string(image, tesseract_dict[self.combobox.currentText()])
        self.signal.emit(text)

    def mousePressEvent(self, event  = QMouseEvent):
        '''if self.combobox.isHidden():'''
        if event.button() == Qt.MouseButton.LeftButton: 
            
            self.initial_pos = event.pos()
            self.rubber_band.setGeometry(QRect(self.initial_pos, event.pos()).normalized())     #bu fare ile seçilen recti sol üstten(initialpos) ve eventpos(sağ alttan) verir. 2 noktası belli rect oluşturuyor yani sadece sol üst ve sağ alt
                                                                                                #eğer başlangıç noktası sağ alttan yada bitiş noktası sol üstten olursa bu koordinatlar negatif olabilir. Eğer başlangıç noktası bitiş noktasının sağında ya da altında kalırsa, Qt negatif genişlik/yükseklik verir.
                                                                                                #normalized fonksiyonu bu durumu düzeltiyor. daima sol üstten sağ alta düzgün bi dikdörtgen verir
            self.rubber_band.show()
        else:
            self.main_window.msg_box.edit('Click with the left mouse button to make a selection.')
        '''else:
            self.main_window.msg_box.edit('Please select your language first.')  ''' 
        QWidget.mouseMoveEvent(self, event) 

    def mouseMoveEvent(self, event = QMouseEvent):
        if self.initial_pos is not None:
            self.rubber_band.setGeometry(QRect(self.initial_pos, event.pos()).normalized()) 
        QWidget.mouseMoveEvent(self, event) 

    def mouseReleaseEvent(self, event = QMouseEvent):
        if self.initial_pos is not None: 
            if event.button() == Qt.MouseButton.LeftButton:
                self.initial_pos = None
                #self.unsetCursor()      #fareyi eski haline getirme (buna gerek yok widget zaten kapatılınca burdaki cursor ayarı geçersiz oluyor ama yinede burda bunu tanımlıyoruz.)
                self.rubber_band.hide()
                rubber_rect = self.rubber_band.geometry()

                #### bu blok Qpixmap veya Qimage nesnesini Pil image nesnesine dönüştürmek için yazıldı. pil image direk açamıyor pyqtnin resmini. 
                #### ya bilgisayara kaydetmemiz gerekiyor, ki bu her ekrandan yazı tarıycağımızda sürekli resim kaydetmek demek, sonrasında silsek sürekli resim kaydedip silmek gereksiz bi kaynak tüketimi oluşturabilir diye düşündük.
                #### o yüzden qbuffer kullanıp bi tampon oluşturduk (dosyayı bilgisayara kaydetmek gibi düşün bunu. hayali bi yere kaydediyoz. belleğe yazmak gibi bişeydi kısaca dosyayı).
                #### sonra qiodevice ile pyqtnin resmini byte döndürüp buraya yazıyoz. sonra pil image ile sanki bilgisayardaki bi reesmi açar gibi bu tampondan byteleri alıyoz. bu bufferi kapatıyoz en sonundada.
                image_crop = self.screen_image.copy(rubber_rect)        
                buffer = QBuffer()
                buffer.open(QIODevice.OpenModeFlag.ReadWrite)
                image_crop.save(buffer, 'PNG')
                image = pil_Image.open(io.BytesIO(buffer.data()))
                buffer.close()
                
                self.image_to_text(image)
                self.close()
            else:   #buranın mantığı kullanıcı seçim için karar değiştirirse farenin sol tuşu hariç başka bir tuşa basarsa widget kapanmasın diye.
                self.initial_pos = None   #bunu böyle yapmamın sebebi yukarıdaki işlemleri durdurması için. fare basılıyken sol tuş değildebaşka tuş bırakılırsa yukarısı çalışmasın diye eklendi. kullanıcı seçimi yanlış yapıp tekrar seçim yapmak isterse diye eklendi.
                self.rubber_band.hide()
                #uyarı mesajı yazdır sol tuş bırakılırsa seçim gerçekleşmez diye
                self.main_window.msg_box.edit('If you press another key while holding down the left mouse button, the selection will be canceled.')   
        QWidget.mouseMoveEvent(self, event) 
        
    def closeEvent(self, event): 
        super().closeEvent(event)