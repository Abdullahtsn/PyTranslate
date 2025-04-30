
import os
import sys
import pyautogui

from screen_scale import ScreenSize     #kullanıcının ekranına göre ölçekleme yapmak için kullanıcağım sabit class
from PyQt5 import QtWidgets, QtCore, QtGui
#from PyQt5.QtWidgets import QMessageBox
#from design import Ui_MainWindow   #tasarımı designerde yapmadığım için böyle


if getattr(sys,'frozen', False):        
    os.chdir(sys._MEIPASS)
else:                       
    os.chdir('.')


    


class TranslateApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(TranslateApp,self).__init__()
        self.screen_w, self.screen_h, self.screen_scale = ScreenSize()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.toolbutton_size = (20*self.screen_scale, 20*self.screen_scale)
        self.language = ['tr','en','we','hh','yt','fg','f','sd','er']        #dilleri iki harf kısaltmalı olarak ver. daha fazlası diğer yerleşimleri ve düzenleri bozabilir.
        self.style_sheet_string = (f'''
                            QMainWindow {{
                        background-color: rgb(0,0,0) ;margin: 0px; padding: 0px; border:none; 
                        }}
                            QToolBar {{ 
                         background-color: transparent; margin: 0px; padding: 0px; spacing: 0px; border:none; 
                        }}  
                            QToolButton {{
                           text-align: center; padding: 0px; margin: 0px; spacing: 0px;
                        }}
                            QToolButton:checked {{       /* bu yöntemle sadece butonun basılı tutulma halini kontrol ediyorum ve diğer hiç bi varsayılan ayarı değiştirmiyoruz. özellikle pinned butonu için çok faydalı oldu. */
                        background-color: rgb(57, 12, 55)
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
                        }} 
                            QToolButton:hover {{
                        background-color:rgb(255, 254, 219);
                        }}
                            QToolButton:pressed {{
                        border-color: rgb(168, 186, 253); background-color:rgb(207, 230, 7); color:  rgb(201, 243, 201);
                        }} */
                            QComboBox {{
                        text-align: center;
                        padding: {4*self.screen_scale}px;
                        font: bold {8*self.screen_scale}px;
                        max-width: {18*self.screen_scale}px;
                        border: none solid white;
                        color: rgb(96, 139, 76);
                        background-color: black;
                        }}
                            QComboBox::hover {{
                        background-color: white
                        }}
                            QComboBox QAbstractItemView {{
                        text-align: center;
                        border: none;
                        background-color: white;
                        color: rgb(96, 139, 76);
                        }}
                            QComboBox::drop-down {{
                        width: 0px;
                        border: none;
                        }}
                            
                            QComboBox:!editable {{
                        text-align: center; 
                        }}
                            QComboBox:editable {{
                        text-align: center;    
                        }}
                            QComboBox::down-arrow {{         /* ok kısmının olduğu yer */
                        image: none;
                        width: 0px;
                        height: 0px;
                        }}
                                                ''')    #normalde toolbarın üst kısmında bi çizgi vardı boydan boya beyaz. borderi none yaparak bundan kurtulduk.
        
        self.setStyleSheet(self.style_sheet_string)
        self.widgets_load()
        self.resize(QtCore.QSize(self.toolbar.sizeHint()))      #başlangıçta sadece toolbarı göstercek şekilde açılması için.
        self.move_button_clicked()      #move butonuna tıklanınca pencerenin hareket etmesi için. bunu özel tanımlıyoruz çünkü pyqtnin hazır fonksiyonlarını override ediyoruz.
        self.animations_create()

        
    def animations_create(self):    
        self.window_animation_shrink = QtCore.QPropertyAnimation(self, b'size') 
        self.window_animation_shrink.setEasingCurve(QtCore.QEasingCurve.Type.OutBounce)    
        self.window_animation_shrink.setDuration(1500)
        self.window_animation_enlarge = QtCore.QPropertyAnimation(self, b'size') 
        self.window_animation_enlarge.setEasingCurve(QtCore.QEasingCurve.Type.OutBounce)    
        self.window_animation_enlarge.setDuration(1500)

        #aşağıdaki finished connectleri  replace butonunda değilde burda yapmamız sebebi sadece bir defa bağlanması için. butona bağladığımda sürekli sürekli sinyal bağlanarak yığılma yapıyor.
        self.window_animation_shrink.finished.connect(self.change_toolbar_orientation)      #ilk animasyon bitiminde toolbar yönünü değiştirme fonksiyonu.
        self.window_animation_shrink.finished.connect(self.window_enlarge)
        #self.window_animation_enlarge.finished.connect(lambda: self.setEnabled(True))       #animasyonların bitiminde kitli olan pencereyi kullanıcıyla etkileşime girebilsin diye açıyoruz.
                                                                                            #lambda ile kullanmamızın sebebi setenablede parametre veriyoruz (True) diye. yani kullanılan fonksiyon parametre istiyorsa lambda  ile başlatıyoruz onu.
                                                                                            #parametre istemiyorsa lambda kullanmadan direk fonksiyonu yazabiliyoruz.
        self.window_animation_enlarge.finished.connect(self.move_button_mouse_release_event)        #genişleme animasyonu bitince eğer pencere ekran dışına çıkmışsa tekrar içerde konumlandırması için sinyal gönderiyoruz.
                                                                                                    #(move butonunun fare tıklama bırakma fonksiyonunda bunu tanımadığımız için direk o fonksiyona gönderiyoruz sinyalle)


    def widgets_load(self):
        self.toolbar = QtWidgets.QToolBar('ToolBar', self)
        self.toolbar.setIconSize(QtCore.QSize(self.toolbutton_size[0], self.toolbutton_size[1]))
        layout = self.toolbar.layout()
        layout.setSpacing(0)     #bu ve alttaki satır hiç bir tarafından boşluk kalmaması için
        layout.setContentsMargins(0,0,0,0)
        self.toolbar.setMovable(False)       #kullanıcı hareket ettiremesin diye
        self.toolbar.setMinimumSize(1,1)        #bunun amacı toolbar animasyon ile küçültülürken son öğe küçültülmüyordu ve çıkan genişletme okun alanı düzensiz bir görünüm veriyordu. genişletme okununda alanını ölçüye dahil edebilmek için genel ölçünün en küçüğünü ayarladık.minimumsizesi yüksek olunca animasyon küçültme yapmıyor.
        self.toolbar.setFloatable(False)    #pencere dışına bırakıldığında otomatik pencereye dönmesi için.
        
        self.addToolBar(self.toolbar)  #direk en üste eklemesi için. çünkü mainwindowu buna göre ayarlıyoruz.
       
        toolbutton_str = [
            ('open','Open', 'action'),
            ('picture','Picture','action'),
            ('speech','Speech','action'),
            ('source_combobox','Source','combobox'),
            ('change','Change','action'),
            ('target_combobox','Target','combobox'),
            ('trash','Trash','action'),
            ('transparent','Transparent','action'),
            ('pinned','Pinned','action'),        #bunu basılı tutan şekilde ayarla
            ('replace','Replace','action'),
            ('move','Move','toolbutton'),       #move butonuna basılı tutulunca hareket etmesini override etmek için toolbutton sınıfını oluşturmamız lazım. çünkü action sınıfı sadece tıklamaları falan sinayle bağlıyor. onun move,press gibi yöntemleri olmadığı için override edemiyoruz. o yüzden sadece move butonu için action değilde toolbutton oluşturuyoz.
            ('close','Close','action')
        ]

        self.toolbar_widget_dict = {}       #bunu liste olarakta yapabilirdik ama o zaman butonlara teker teker ulaşamıyoruz o yüzden bunu dict olarak tanımlıyoruz. eğer tekil olarak ulaşmak istersek ulaşabiliyoruz.        
        
        for png_path, text, widgettype in toolbutton_str:
            if widgettype == 'combobox':      #burda change butonundan önce ve sonra comboboxları ekliyceğimiz için toolbutton_str listesine ekliyceğimiz comboboxları koyduk.
                combobox = QtWidgets.QComboBox()                                #aşağıdaki yorum eski çünkü widget tiplerine göre işlem yapmak için stryi genişlettim. ve kontrolü tiplere göre yapıyom. continueye gerek kalmadı. ama lazım olursa diye bu satırı bıraktım not olarak.
                                                                                #eski olan açıklama -->  ve eğer bu comboboxlar gelirse döngüde bunlar için buton değil combobox oluşturduk. ve aşağıda buton oluşturmasın diye döngüde sonraki iterasyona geçsin diye continue kullandık.contunie ile döngüde sonraki adıma geçmesini sağladık. böylece sözlüğe sıralı bir şekilde qactionları ve qcomboboxları yerleştirmiş olduk.
                self.toolbar_widget_dict[png_path] = {'widget':combobox, 'widgettype': widgettype}      
                
            elif widgettype == 'action':
                png = QtGui.QIcon(os.path.join('icon',f'{png_path}.png'))
                button = QtWidgets.QAction(png, text, self)
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
                png = QtGui.QIcon(os.path.join('icon',f'{png_path}.png'))
                button = QtWidgets.QToolButton()
                button.setIcon(png)
                button.setToolTip(text)
                self.toolbar_widget_dict[png_path] = {'widget':button, 'widgettype':widgettype}
                
        self.toolbar_widget_dict['source_combobox']['widget'].setToolTip('Source Language')    #q acitonda oluşturduğumuz ikinci parametreler zaten tooltip gibi göründüğü için onlara yapmaya gerek yok ama qcomboboxlarınki fareyle üzerine gelince görünmüyor. bu ikisinielle ayarladık.
        self.toolbar_widget_dict['target_combobox']['widget'].setToolTip('Target Language')
        self.toolbar_widget_dict['pinned']['widget'].setCheckable(True)   #bu  pinned butonunu basılı tutulabilen hale getiriyor.
        self.toolbar_widget_dict['transparent']['widget'].setCheckable(True)    #basılı tutulabilir.
        
        language = []
        for i in self.language:
            language.append(i.upper())
        for key, value in self.toolbar_widget_dict.items():
            if value['widgettype'] == 'combobox':         #comboboxa uzun bişey eklersen tool button dikeyde sola yaslı kalıyor. zaten dil kodları kısa olduğu için burda bişey farketmiycek ama sonrası için uzun bişeyler eklersen değiştirmek gerekebilir.
                value['widget'].addItems(language)        #comboboxdaki dillerin otomatik olarak ikisinede eklenmesi için. eğer bi comboboxda olup ötekinde olmazsa change ile olmayan değişmiyor. o yüzden ikisininde aynı olması lazım. (ekleme yoluyla yine yapılabilir ama böylesi daha iyi)
                self.toolbar.addWidget(value['widget'])
            elif value['widgettype'] == 'toolbutton':           
                self.toolbar.addWidget(value['widget'])
            else:
                self.toolbar.addAction(value['widget'])
        #self.toolbar.addActions(self.toolbar_widget_dict.values())      #addactionsa butonların asıl hallerini değerler olarak kaydettiğimiz için buraya o şekilde giriyoruz.

        '''self.setCentralWidget(self.toolbar)
        for button in self.findChildren(QtWidgets.QToolButton):     #extension butonuna yani pyqtnin toolbar için otomatik oluşturduğu genişletme butonuna erişim için gerekli olan döngü
            if button.objectName() == "qt_toolbar_ext_button":      #butona bu şekilde ulaşabiliyoruz ama değiştiremiyoruz özelliklerini pyqt izin vermiyor. lazım olursa diye not için yorum yaptım.
                button.setEnabled(False)'''
        
        '''for i in self.findChildren(QtWidgets.QWidget):           #hem bizim hem pyqtnin oluşturduğu widgetleri  görmek için.
            print(i, i.objectName()  '''   
        
        
    

    def open_button_clicked(self):
        pass

    def picture_button_clicked(self):
        pass

    def speech_button_clicked(self):
        pass

    def change_button_clicked(self):
        source_combobox = self.toolbar_widget_dict['source_combobox']['widget'].currentText()
        target_combobox = self.toolbar_widget_dict['target_combobox']['widget'].currentText()
        self.toolbar_widget_dict['source_combobox']['widget'].setCurrentText(target_combobox)
        self.toolbar_widget_dict['target_combobox']['widget'].setCurrentText(source_combobox)
        

    def trash_button_clicked(self):
        pass


    def transparent_button_clicked(self):
        if self.toolbar_widget_dict['transparent']['widget'].isChecked():
            self.setWindowOpacity(0.60)
        else:
            self.setWindowOpacity(1)


    def pinned_button_clicked(self):
        if self.toolbar_widget_dict['pinned']['widget'].isChecked():
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint) 
             
        else:
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint) 
        self.showNormal()       #pencere bayrak ayarlarını değiştirdiğimiz için pencereyi başta oluşturuyor.o yüzden bunu tekrar göstermesi için shownormal yada direk showda yapabiliriz farketmez.
                   
    
    def replace_button_clicked(self):
        #self.setEnabled(False)      #kullanıcı animasyon sırasında pencereyle etkileşime giremesin diye kitliyoruz. zaten animasyon kısa olduğu için bunu açmaya gerek duymadım. bunu etkinleştirmek gerekirse animastionları tanımadığım yerde bunu açıcak sinyali açmayı unutma onuda yorum yaptım.
        self.window_shrink()
        self.window_animation_shrink.start()
        

    def window_shrink(self):
        sizehint = self.toolbar.sizeHint()
        w, h =  sizehint.width(), sizehint.height()
        self.window_animation_shrink.setStartValue(QtCore.QSize(w, h))
        if self.toolbar.orientation() == 1:         #anlamı; eğer toolbar yataysa demek
            self.window_animation_shrink.setEndValue(QtCore.QSize(self.toolbutton_size[0], h))                     
        else:
            self.window_animation_shrink.setEndValue(QtCore.QSize(w, self.toolbutton_size[1]))


    def window_enlarge(self):
        current_size_h = self.toolbar.size().height()
        sizehint = self.toolbar.sizeHint()
        sizehint_w, sizehint_h =  sizehint.width(), sizehint.height()
        self.window_animation_enlarge.setStartValue(QtCore.QSize(current_size_h, current_size_h ))          #genişlemeye başlamadan önce sadece yükseklik ölçüsünü veriyoruz hem genişliğe hem yüksekliğe. öteki türlü ufak taşmalar oluyor genişlme okunun çıkmasından dolayı.
        self.window_animation_enlarge.setEndValue(QtCore.QSize(sizehint_w, sizehint_h))
        self.window_animation_enlarge.start()

        
    def change_toolbar_orientation(self):
        if self.toolbar.orientation() == 1:     #orientationun döndürdüğü yatay ise 1, dikey ise 2
            self.toolbar.setOrientation(QtCore.Qt.Vertical)
        elif self.toolbar.orientation() == 2:
            self.toolbar.setOrientation(QtCore.Qt.Horizontal) 
        
    
    def close_button_clicked(self):
        self.close()

        
    def DENEMELER(self):        #YUKARIDA BUTONLARI DİNAMİK OLUŞTURDUĞUM İÇİN TAMAMLAMA ÇIKMIYOR. ÖZELLİKLERE BAKMAK İSTERSEN BURDA DENE.
        action = QtWidgets.QAction()
        button = QtWidgets.QToolButton()
        combobox = QtWidgets.QComboBox()

        
        
    def move_button_clicked(self):
        self.toolbar_widget_dict['move']['widget'].mousePressEvent = self.move_button_mouse_pressed_event
        self.toolbar_widget_dict['move']['widget'].mouseMoveEvent = self.move_button_mouse_move_event
        self.toolbar_widget_dict['move']['widget'].mouseReleaseEvent = self.move_button_mouse_release_event
    

    def move_button_mouse_pressed_event(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.initial_pos = event.pos()
        #super(QtWidgets.QToolButton, self.toolbar_widget_dict['move']['widget']).mousePressEvent(event)    #burda sınıfın kendi içinde olmadığımız için super mantıksız kalıyor olabilir o yüzden bu satır aşağıdaki şekilde güncellendi.
        QtWidgets.QToolButton.mousePressEvent(self.toolbar_widget_dict['move']['widget'], event)    #yukardaki satırı bu şekle dönüştürdük. supere gerek yok. direktoolbuttonun tıklamaısnı alıyoz.
                                                                                                    #Bu, 'widget’a ait olan Qt'nin orijinal mousePressEvent metodunu elle çağır' demek. kısaca ;
                                                                                                    #super(...).method()	Sadece bir sınıfın içinden, self o sınıfken mantıklı,
                                                                                                    #QtWidgets.QToolButton.method(widget, event)	Eğer QToolButton nesnesinin içinden değilsen, bu şekilde çağırmak gerekiyor
        event.accept()
        
    def move_button_mouse_move_event(self,event):
        self.setCursor(QtCore.Qt.BlankCursor)       #move tuşuna basılıyken farenin görünmez olmasını sağlıyor.
        if self.initial_pos is not None:
            delta = event.pos() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        #super(QtWidgets.QToolButton, self.toolbar_widget_dict['move']['widget']).mouseMoveEvent(event)
        QtWidgets.QToolButton.mouseMoveEvent(self.toolbar_widget_dict['move']['widget'], event)
        event.accept()

    def move_button_mouse_release_event(self, event = None):    #burda eventi varsayılan olarak none ayarlamamızın sebebi;
                                                                #bu fareyi bırakma yanibu fonksiyonun asıl amacı pencerenin dışarı taşırabilirliğini engellemek.
                                                                #o yüzden sadece move butonuyla değil pencereye döndürme butonuylada pencere ekran dışına taşırılabiliyor. 
                                                                #o yüzden pencereyi döndürme fonksiyonunuda burdaki hesaplamaya yönlendirip ekran içinde tutulmasını sağlıyoruz. 
                                                                #eventi none yapmazsak ordan event göndermediğimiz için hata veriyor.
                                                                #o yüzden bu fonksiyona istediğimiz heryerden sorunsuzca ulaşmak için none yaptık, ve gerçek event gelirse diye mesela move butonu gibi, onuda aşağıdaki if bloğunda kodladık.
                                                                #sahte eventte oluşturabiliyormuşuz ama ona gerek duyulmadı bu işimizi görür.
        #ekran dışına çıkarsa tekrar ekran sınırlarına geri getirilmesi için. bunu mouse move kısmında değilde fareyi bırakma kısmında yapmamın sebebi;
        #sürüklenirken sürekli gereksiz hesaplama yapmaması için, sadece bırakma anında bir kere hesaplayıp sınırlar içine yerleştirmesi daha az kaynak tüketir ve daha optimize olur.
        geometry = self.geometry()
        x, y, width, height = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if x < 0 :
            x = 0
        elif x + width > self.screen_w :
            x = self.screen_w - width
        if y < 0 :
            y = 0
        elif y + height > self.screen_h :
            y = self.screen_h - height
        self.setGeometry(x, y, width, height)

        if event is not None:
            self.unsetCursor()          #farenin tuşu bırakılınca cursor ayarını kaldırıp eski haline getiriyor.
            self.initial_pos = None 
            #super(QtWidgets.QToolButton, self.toolbar_widget_dict['move']['widget']).mouseReleaseEvent(event)
            QtWidgets.QToolButton.mouseReleaseEvent(self.toolbar_widget_dict['move']['widget'], event)
            event.accept()


            
    
        
        
    #pyqt nin sabit fonksiyonları;
    '''def mousePressEvent(self, event):   #farenin basma olayları
        pass
        
    def mouseMoveEvent(self, event):     #farenin basılı tutarkenki hareket olayları
        pass
    
    def mouseReleaseEvent(self, event):    #farenin basılmasını bırakma olayları
        pass'''


    def closeEvent(self, event):       
        print('çıkıldı')
            
        

    
    
    



def app():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')          #genel pencere tasarımını değiştiriyor .en moderdi bu. diğer seçenekler arasında windowsvista ve Windows var. onlar çok eski ve kötü gözüküyor.
    win = TranslateApp()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app()
    


