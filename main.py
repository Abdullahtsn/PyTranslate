
import os
import sys

from screen_scale import ScreenSize         #kullanıcının ekranına göre ölçekleme yapmak için kullanıcağım sabit class
from speech_widget import SpeechWidget      #speech butonuna tıklanınca açılcak özel oluşturulan çeviri widgeti
from move_class import MoveClass

from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QToolButton, QComboBox, QAction
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QIcon

#from PyQt5.QtWidgets import QMessageBox
#from design import Ui_MainWindow   #tasarımı designerde yapmadığım için böyle



if getattr(sys,'frozen', False):        
    os.chdir(sys._MEIPASS)
else:                       
    os.chdir('.')







class TranslateApp(QMainWindow):
    def __init__(self):
        super(TranslateApp,self).__init__()
        self.screen_w, self.screen_h, self.screen_scale = ScreenSize()
        self.speech_widget = SpeechWidget(self.screen_w, self.screen_h, self.screen_scale)
        self.speech_widget.close_signal.connect(self.speech_widget_close_signal)    #speechWidgetten çıkılırsa toolbardaki text butonunun bırakılması için gelen sinyalin fonksiyonu.
        
        
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)       #mainwindow için arka planı görünmez yapıyor sadece widgetler görünüyor.(frameleswindowhint ile birlikte kullanılıyor.)
        self.toolbutton_size = (20*self.screen_scale, 20*self.screen_scale)
        self.style_sheet_string = (f'''
                            QMainWindow {{
                        background-color: rgb(255, 253, 227) ;
                        margin: 0px; 
                        padding: 0px; 
                        border:none; 
                        }}
                            QToolBar {{ 
                        background-color: transparent; 
                        padding: 0px; 
                        spacing: 0px; 
                        border:none; 
                        }}  
                            QPushButton, QToolButton {{
                        background-color: rgb(255, 253, 227) ; 
                        text-align: center; 
                        padding: {2*self.screen_scale}px; 
                        margin: 0px; 
                        spacing: 0px; 
                        border-radius:{4*self.screen_scale}px;
                        border-style: solid;
                        border-width: {2*self.screen_scale}px;
                        border-color: rgb(48, 68, 0);
                        }}
                            QPushButton:checked, QToolButton:checked {{       /* bu yöntemle sadece butonun basılı tutulma halini kontrol ediyorum ve diğer hiç bi varsayılan ayarı değiştirmiyoruz. özellikle pinned butonu için çok faydalı oldu. */
                        background-color: rgb(25, 60, 30);
                        border-color: rgb(40, 90, 40);
                        }}
                            QPushButton:hover, QToolButton:hover {{
                        background-color: rgb(11, 42, 10);
                        border-color: rgb(168, 186, 253); 
                        }}
                            QPushButton:pressed, QToolButton:pressed {{
                        border-color: rgb(168, 186, 253); 
                        background-color: rgb(0, 0, 0); 
                        color:  rgb(11, 42, 10);
                        }} 
                           QToolButton#qt_toolbar_ext_button {{
                        border: none;
                        padding: 0px;
                        margin: 0px;
                        max-width: 0px; 
                        }}

                        /*    QToolButton {{             #toolbutton ayarları ilerde lazım olursa diye yazdım ama şuan burda kullanmıycaz carsayılan ayarı fena değil.
                        text-align: center; padding: 0px; margin: 0px; border-radius: 0px; border-style: solid; 
                        color: rgb(201, 243, 201); background-color: initial; border-color: rgb(47, 172, 126);
                        }} */
                           
                                                ''')    #normalde toolbarın üst kısmında bi çizgi vardı boydan boya beyaz. borderi none yaparak bundan kurtulduk.
        
        self.setStyleSheet(self.style_sheet_string)
        self.widgets_load()
        self.resize(QSize(self.toolbar.sizeHint()))      #başlangıçta sadece toolbarı göstercek şekilde açılması için.
        self.move_button_clicked()      #move butonuna tıklanınca pencerenin hareket etmesi için. bunu özel tanımlıyoruz çünkü pyqtnin hazır fonksiyonlarını override ediyoruz.
        self.animations_create()
        
            
    def animations_create(self):    
        self.window_animation_shrink = QPropertyAnimation(self, b'size') 
        self.window_animation_shrink.setEasingCurve(QEasingCurve.Type.InOutSine)    
        self.window_animation_shrink.setDuration(1000)
        self.window_animation_enlarge = QPropertyAnimation(self, b'size') 
        self.window_animation_enlarge.setEasingCurve(QEasingCurve.Type.InOutSine)    
        self.window_animation_enlarge.setDuration(1000)

        #aşağıdaki finished connectleri  replace butonunda değilde burda yapmamız sebebi sadece bir defa bağlanması için. butona bağladığımda sürekli sürekli sinyal bağlanarak yığılma yapıyor.
        self.window_animation_shrink.finished.connect(self.change_toolbar_orientation)      #ilk animasyon bitiminde toolbar yönünü değiştirme fonksiyonu.
        self.window_animation_shrink.finished.connect(self.window_enlarge)
        #self.window_animation_enlarge.finished.connect(lambda: self.setEnabled(True))       #animasyonların bitiminde kitli olan pencereyi kullanıcıyla etkileşime girebilsin diye açıyoruz.
                                                                                            #lambda ile kullanmamızın sebebi setenablede parametre veriyoruz (True) diye. yani kullanılan fonksiyon parametre istiyorsa lambda  ile başlatıyoruz onu.
                                                                                            #parametre istemiyorsa lambda kullanmadan direk fonksiyonu yazabiliyoruz.
        self.window_animation_enlarge.finished.connect(self.move_class.move_button_mouse_release_event)        #genişleme animasyonu bitince eğer pencere ekran dışına çıkmışsa tekrar içerde konumlandırması için sinyal gönderiyoruz.
                                                                                                    #(move butonunun fare tıklama bırakma fonksiyonunda bunu tanımadığımız için direk o fonksiyona gönderiyoruz sinyalle)


    def widgets_load(self):
        self.toolbar = QToolBar('ToolBar', self)
        self.toolbar.setIconSize(QSize(self.toolbutton_size[0], self.toolbutton_size[1]))
        layout = self.toolbar.layout()
        layout.setSpacing(0)     #bu ve alttaki satır hiç bir tarafından boşluk kalmaması için
        layout.setContentsMargins(0,0,0,0)
        self.toolbar.setMovable(False)       #kullanıcı hareket ettiremesin diye
        self.toolbar.setMinimumSize(1,1)        #bunun amacı toolbar animasyon ile küçültülürken son öğe küçültülmüyordu ve çıkan genişletme okun alanı düzensiz bir görünüm veriyordu. genişletme okununda alanını ölçüye dahil edebilmek için genel ölçünün en küçüğünü ayarladık.minimumsizesi yüksek olunca animasyon küçültme yapmıyor.
        self.toolbar.setFloatable(False)    #pencere dışına bırakıldığında otomatik pencereye dönmesi için.
        
        self.addToolBar(self.toolbar)  #direk en üste eklemesi için. çünkü mainwindowu buna göre ayarlıyoruz.
       

        toolbutton_str = [
            ('text','Text', 'action'),
            ('image_text','Image Text','action'),
            ('transparent','Transparent','action'),
            ('pinned','Pinned','action'),        #bunu basılı tutan şekilde ayarla
            ('rotation','Rotation','action'),
            ('minimize','Minimize','action'),
            ('move','Move','toolbutton'),       #move butonuna basılı tutulunca hareket etmesini override etmek için toolbutton sınıfını oluşturmamız lazım. çünkü action sınıfı sadece tıklamaları falan sinayle bağlıyor. onun move,press gibi yöntemleri olmadığı için override edemiyoruz. o yüzden sadece move butonu için action değilde toolbutton oluşturuyoz.
            ('close','Close','action')
        ]

        self.toolbar_widget_dict = {}       #bunu liste olarakta yapabilirdik ama o zaman butonlara teker teker ulaşamıyoruz o yüzden bunu dict olarak tanımlıyoruz. eğer tekil olarak ulaşmak istersek ulaşabiliyoruz.        
        
        for png_path, text, widgettype in toolbutton_str:
            '''if widgettype == 'combobox':      #burda change butonundan önce ve sonra comboboxları ekliyceğimiz için toolbutton_str listesine ekliyceğimiz comboboxları koyduk.
                combobox = QComboBox()                                #aşağıdaki yorum eski çünkü widget tiplerine göre işlem yapmak için stryi genişlettim. ve kontrolü tiplere göre yapıyom. continueye gerek kalmadı. ama lazım olursa diye bu satırı bıraktım not olarak.
                                                                                #eski olan açıklama -->  ve eğer bu comboboxlar gelirse döngüde bunlar için buton değil combobox oluşturduk. ve aşağıda buton oluşturmasın diye döngüde sonraki iterasyona geçsin diye continue kullandık.contunie ile döngüde sonraki adıma geçmesini sağladık. böylece sözlüğe sıralı bir şekilde qactionları ve qcomboboxları yerleştirmiş olduk.
                self.toolbar_widget_dict[png_path] = {'widget':combobox, 'widgettype': widgettype}    '''  #combobox toolbardan kaldırıldı buraya ihtiyaç kalmadı. eğer eklersen yorumu aç.
                
            if widgettype == 'action':
                png = QIcon(os.path.join('icon',f'{png_path}.png'))
                button = QAction(png, text, self)
                button.triggered.connect(getattr(self, f'{png_path}_button_clicked'))       #getattr bir objenin içindeki bir özelliğe (ya da fonksiyona) string olarak ulaşmanı sağlar. 
                                                                                            #yukarda butonlar için oluşturduğumuz fonksiyonları burda str olarka tanımlıyorum getattr ile. bu işe yarıyor.
                #toolbutton_list.append(button)
                self.toolbar_widget_dict[png_path] = {'widget':button, 'widgettype':widgettype}     #burdaki buton isimlerini yani png deki isimleri key, butonun asıl oluşturulmuş qaction hallerini value olarak kaydettik. 
                                                                #daha sonra herhangi bir butona ulaşmak istersek self.toolbar_widget_dict['open']    yazarak o butona ulaşabiliyoruz.
                #print(self.toolbar_widget_dict['open'])        #dicte widget tiplerinide ekledim bu biraz eskide kaldı ama mantığını unutmamak için silmedim.
                #print(self.toolbar_widget_dict.keys(), self.toolbar_widget_dict.values())
        
            elif widgettype == 'toolbutton':        #move butonu için action değilde toolbutton olarak oluşturup diğer buttonlardan ayırmamızın sebebi , qaction qwidget olmadığı için 
                                                    #mousePressEvent, mouseMoveEvent gibi eventleri yakalayamıyoruz. o yüzden move butonu için toolbutton kullanıyoruz.
                                                    #bide bunu yukardaki actionda yaptığımız gibi hazır bi fonksiyona göndermiyoruz. initte move butonunun tıklama ve sürükleme olaylarını override ediceğimiz fonksiyona yönlendiriyoruz.     
                png = QIcon(os.path.join('icon',f'{png_path}.png'))
                button = QToolButton(self)
                button.setIcon(png)
                button.setToolTip(text)
                self.toolbar_widget_dict[png_path] = {'widget':button, 'widgettype':widgettype}
                
        '''self.toolbar_widget_dict['source_combobox']['widget'].setToolTip('Source Language')    #q acitonda oluşturduğumuz ikinci parametreler zaten tooltip gibi göründüğü için onlara yapmaya gerek yok ama qcomboboxlarınki fareyle üzerine gelince görünmüyor. bu ikisinielle ayarladık.
        self.toolbar_widget_dict['target_combobox']['widget'].setToolTip('Target Language')'''
        self.toolbar_widget_dict['pinned']['widget'].setCheckable(True)   #bu  pinned butonunu basılı tutulabilen hale getiriyor.
        self.toolbar_widget_dict['transparent']['widget'].setCheckable(True)    #basılı tutulabilir.
        self.toolbar_widget_dict['text']['widget'].setCheckable(True)    #basılı tutulabilir.
        
        '''language = []
        for i in self.language:
            language.append(i.upper())'''


        for key, value in self.toolbar_widget_dict.items():
            '''if value['widgettype'] == 'combobox':         #comboboxa uzun bişey eklersen tool button dikeyde sola yaslı kalıyor. zaten dil kodları kısa olduğu için burda bişey farketmiycek ama sonrası için uzun bişeyler eklersen değiştirmek gerekebilir.
                value['widget'].addItems(language)        #comboboxdaki dillerin otomatik olarak ikisinede eklenmesi için. eğer bi comboboxda olup ötekinde olmazsa change ile olmayan değişmiyor. o yüzden ikisininde aynı olması lazım. (ekleme yoluyla yine yapılabilir ama böylesi daha iyi)
                self.toolbar.addWidget(value['widget'])'''      #comboboxlar normalde main windowdaydı bu şekilde dilleri eklemiştim. ama speexhwidgete taşındı(çeviri yapıcağım widget). o yüzden kaldırıldı burası.
            if value['widgettype'] == 'toolbutton':           
                self.toolbar.addWidget(value['widget'])
            else:
                self.toolbar.addAction(value['widget'])
        #self.toolbar.addActions(self.toolbar_widget_dict.values())      #addactionsa butonların asıl hallerini değerler olarak kaydettiğimiz için buraya o şekilde giriyoruz.

        
        '''self.setCentralWidget(self.toolbar)
        for button in self.findChildren(QToolButton):     #extension butonuna yani pyqtnin toolbar için otomatik oluşturduğu genişletme butonuna erişim için gerekli olan döngü
            if button.objectName() == "qt_toolbar_ext_button":      #butona bu şekilde ulaşabiliyoruz ama değiştiremiyoruz özelliklerini pyqt izin vermiyor. lazım olursa diye not için yorum yaptım.
                button.setEnabled(False)'''
        
        '''for i in self.findChildren(QWidget):           #hem bizim hem pyqtnin oluşturduğu widgetleri  görmek için.
            print(i, i.objectName()  '''   
        
        
    
    def text_button_clicked(self):
        if self.toolbar_widget_dict['text']['widget'].isChecked():
            self.speech_widget.show()
        else:
            self.speech_widget.close()

    def speech_widget_close_signal(self):      #eğer toolbardan değilse speechwidgetten çıkılırsa burası tetiklenip toolbarın tuşunun bırakılmasını sağlıycak sinyal fonksiyonu.
        if self.toolbar_widget_dict['text']['widget'].isChecked():
            self.toolbar_widget_dict['text']['widget'].trigger()    #qactionda tıklamayı böyle yapıyoruz. scriptte tıklanmasını istersek böyle yapıyoruz. Qpushbutton ve Qtoolbuttonda ki click() fonksiyonu mantığı. 
        else:
            pass

    def image_text_button_clicked(self):
        pass

    

    '''def change_button_clicked(self):     #burası comboboxlarla ilgiliydi ama speechwidgete taşındı o yüzden gerek kalmadı. sonrası için combobox eklersem diye yorum bıraktım.
        source_combobox = self.toolbar_widget_dict['source_combobox']['widget'].currentText()
        target_combobox = self.toolbar_widget_dict['target_combobox']['widget'].currentText()
        self.toolbar_widget_dict['source_combobox']['widget'].setCurrentText(target_combobox)
        self.toolbar_widget_dict['target_combobox']['widget'].setCurrentText(source_combobox)'''
        

    def trash_button_clicked(self):
        pass


    def transparent_button_clicked(self):
        if self.toolbar_widget_dict['transparent']['widget'].isChecked():
            self.setWindowOpacity(0.60)
        else:
            self.setWindowOpacity(1)


    def pinned_button_clicked(self):
        if self.toolbar_widget_dict['pinned']['widget'].isChecked():
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint) 
             
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint) 
        self.showNormal()       #pencere bayrak ayarlarını değiştirdiğimiz için pencereyi başta oluşturuyor.o yüzden bunu tekrar göstermesi için shownormal yada direk showda yapabiliriz farketmez.
                   
    
    def rotation_button_clicked(self):
        #self.setEnabled(False)      #kullanıcı animasyon sırasında pencereyle etkileşime giremesin diye kitliyoruz. zaten animasyon kısa olduğu için bunu açmaya gerek duymadım. bunu etkinleştirmek gerekirse animastionları tanımadığım yerde bunu açıcak sinyali açmayı unutma onuda yorum yaptım.
        self.window_shrink()
        self.window_animation_shrink.start()
        

    def window_shrink(self):
        sizehint = self.toolbar.sizeHint()
        w, h =  sizehint.width(), sizehint.height()
        self.window_animation_shrink.setStartValue(QSize(w, h))
        if self.toolbar.orientation() == 1:         #anlamı; eğer toolbar yataysa demek
            self.window_animation_shrink.setEndValue(QSize(h, h))                     
        else:
            self.window_animation_shrink.setEndValue(QSize(w, w))


    def window_enlarge(self):
        current_size_h = self.toolbar.size().height()
        sizehint = self.toolbar.sizeHint()
        sizehint_w, sizehint_h =  sizehint.width(), sizehint.height()
        self.window_animation_enlarge.setStartValue(QSize(current_size_h, current_size_h ))          #genişlemeye başlamadan önce sadece yükseklik ölçüsünü veriyoruz hem genişliğe hem yüksekliğe. öteki türlü ufak taşmalar oluyor genişlme okunun çıkmasından dolayı.
        self.window_animation_enlarge.setEndValue(QSize(sizehint_w, sizehint_h))
        self.window_animation_enlarge.start()

        
    def change_toolbar_orientation(self):
        if self.toolbar.orientation() == 1:     #orientationun döndürdüğü yatay ise 1, dikey ise 2
            self.toolbar.setOrientation(Qt.Vertical)
        elif self.toolbar.orientation() == 2:
            self.toolbar.setOrientation(Qt.Horizontal) 
        
    def minimize_button_clicked(self):
        self.showMinimized()

    def close_button_clicked(self):
        self.close()

        
    def move_button_clicked(self):  #bu buton veya herhangi bir widgetin taşınma olaylarını ayrı bir pyde tanımladık. hem tüm taşıma butonları için kod tekrarını azalttık hemde script daha düzenli oldu.
        self.move_class = MoveClass(self.toolbar_widget_dict['move']['widget'], self.screen_w, self.screen_h)
        self.toolbar_widget_dict['move']['widget'].mousePressEvent = self.move_class.move_button_mouse_press_event
        self.toolbar_widget_dict['move']['widget'].mouseMoveEvent = self.move_class.move_button_mouse_move_event
        self.toolbar_widget_dict['move']['widget'].mouseReleaseEvent = self.move_class.move_button_mouse_release_event
        
    


            
    
        
        
    #pyqt nin sabit fonksiyonları;
    '''def mousePressEvent(self, event):   #farenin basma olayları
        pass
        
    def mouseMoveEvent(self, event):     #farenin basılı tutarkenki hareket olayları
        pass
    
    def mouseReleaseEvent(self, event):    #farenin basılmasını bırakma olayları
        pass'''


    def closeEvent(self, event): 
        self.speech_widget_close_signal()   #eğer speechwidget açıksa toolbardan çıkılırken onunda kapatılması için.
        print('çıkıldı')
        super().closeEvent(event)
            
        

    
    
    



def app():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')          #genel pencere tasarımını değiştiriyor .en moderdi bu. diğer seçenekler arasında windowsvista ve Windows var. onlar çok eski ve kötü gözüküyor.
    win = TranslateApp()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app()
    


