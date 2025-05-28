
import os
import sys

from screen_scale import ScreenSize         #kullanıcının ekranına göre ölçekleme yapmak için kullanıcağım sabit class
from speech_widget import SpeechWidget      #speech butonuna tıklanınca açılcak özel oluşturulan çeviri widgeti
from image_widget import ImageWidget        #ekrandaki metni tanımlama için oluşturulcak widget
from move_class import MoveClass            #widgetlerin move tuşuna bağlanması
from msgbox_widget import MsgBox            #messagebox widgeti
from style_sheet import ThemaClass, ThemaDict     #bunları uygulamanın daha oluşturulma aşamasında kullanacağımız için direk genel değişken olarak alıyoruz. def initte tanımlarsak win oluşmadan bunlara ulaşamıyoruz.
from exe_script_path_class import ExeScriptPath     #çalışma yeri exemi sciprtmi diye kontrol edip buna göre yol belirlediğimiz singleton desenle oluşturulmuş class

from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QToolButton, QAction, QMenu
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QPixmap



class TranslateApp(QMainWindow):
    def __init__(self):
        super(TranslateApp,self).__init__()
        
        self.screen_w, self.screen_h, self.screen_scale = ScreenSize().values()
        self.path_temp, self.path_exe = ExeScriptPath().paths()         #exenin içine gömülceklerin yolunu tempe ver. installer paketlencek eze ile aynı dizinde olan büyük bağımlılıklara exeyi ver.
        self.speech_widget = SpeechWidget(self)     #burda main windowu parent olarak göndermemin sebebi msgbox widgetini ana widgete taşıycam çünkü bu widgeti sadece speechwidget kullanmıycak.
                                                    #her kullanan widget içinde msgbox widgeti oluşturup bellekte tutmak istemiyorum. o yüzden mainwindowu gönderip, msgbox widgetini burda oluşturup,
                                                    #diğer widgetlerden burdaki msgbox widgetine erişip edit fonksiyonunu çalıştırabiliriz. hatta tüm fonksiyonlara erişmek için bile mantıklı.
                                                    #mainwindowu göndermek ayrıca bellekte yer tutmadığı için çok iyi bi yöntem. SpeechWidget içinde self.main_window = main_window dediğinde,
                                                    #bu sadece MainWindow objesinin adresini tutar, yeni bir pencere veya veri oluşturmaz
        self.speech_widget.close_signal.connect(self.speech_widget_close_signal)    #speechWidgetten çıkılırsa toolbardaki text butonunun bırakılması için gelen sinyalin fonksiyonu.
        
        self.msg_box = MsgBox()         
        self.setWindowTitle('PyTranslate')
        self.setWindowIcon(QIcon(QPixmap(os.path.join(self.path_temp, 'icon','icon.ico'))))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)       #mainwindow için arka planı görünmez yapıyor sadece widgetler görünüyor.(frameleswindowhint ile birlikte kullanılıyor.)
        self.toolbutton_size = (20*self.screen_scale, 20*self.screen_scale)
        
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
            ('pinned','Pinned','action'),        
            ('rotation','Rotation','action'),
            ('thema','Thema','toolbutton'),
            ('expand','Expand','action'),
            ('move','Move','toolbutton'),       #move butonuna basılı tutulunca hareket etmesini override etmek için toolbutton sınıfını oluşturmamız lazım. çünkü action sınıfı sadece tıklamaları falan sinayle bağlıyor. onun move,press gibi yöntemleri olmadığı için override edemiyoruz. o yüzden sadece move butonu için action değilde toolbutton oluşturuyoz.
            ('minimize','Minimize','action'),
            ('close','Close','action')
        ]

        self.toolbar_widget_dict = {}       #bunu liste olarakta yapabilirdik ama o zaman butonlara teker teker ulaşamıyoruz o yüzden bunu dict olarak tanımlıyoruz. eğer tekil olarak ulaşmak istersek ulaşabiliyoruz.        
        
        for png_path, text, widgettype in toolbutton_str:
            '''if widgettype == 'combobox':      #burda change butonundan önce ve sonra comboboxları ekliyceğimiz için toolbutton_str listesine ekliyceğimiz comboboxları koyduk.
                combobox = QComboBox()                                #aşağıdaki yorum eski çünkü widget tiplerine göre işlem yapmak için stryi genişlettim. ve kontrolü tiplere göre yapıyom. continueye gerek kalmadı. ama lazım olursa diye bu satırı bıraktım not olarak.
                                                                                #eski olan açıklama -->  ve eğer bu comboboxlar gelirse döngüde bunlar için buton değil combobox oluşturduk. ve aşağıda buton oluşturmasın diye döngüde sonraki iterasyona geçsin diye continue kullandık.contunie ile döngüde sonraki adıma geçmesini sağladık. böylece sözlüğe sıralı bir şekilde qactionları ve qcomboboxları yerleştirmiş olduk.
                self.toolbar_widget_dict[png_path] = {'widget':combobox, 'widgettype': widgettype}    '''  #combobox toolbardan kaldırıldı buraya ihtiyaç kalmadı. eğer eklersen yorumu aç.
                
            if widgettype == 'action':
                png = QIcon(os.path.join(self.path_temp, 'icon',f'{png_path}.png'))
                button = QAction(png, text, self)
                button.setObjectName(text)
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
                                                    #sonradan dahil ettiğim bi thema butonu var belki başka butonlarda dahil ederim diye burayada bi toolbutton fonksiyonu tanımlaması yaptık. 
                png = QIcon(os.path.join(self.path_temp, 'icon',f'{png_path}.png'))
                button = QToolButton(self)
                button.setObjectName(text)
                button.setIcon(png)
                button.setToolTip(text)
                '''if png_path != 'move' and png_path != 'thema':      #tek bir toolbuttonda tıklamaya göre fonksiyona göndermiycez oda move.
                    button.clicked.connect(getattr(self, f'{png_path}_button_clicked'))'''      #thema butonu için bireysel bi tanımlama yapmaktan vazgeçtik içindeki tıklanan menü butonlarını yönlendiricez o fonksiyona. o yüzden yorum satırına dönüştürüldü burası. eğer ilerde başka toolbutton eklersen ona göre kaldır yorumu..
                self.toolbar_widget_dict[png_path] = {'widget':button, 'widgettype':widgettype}

                
        '''self.toolbar_widget_dict['source_combobox']['widget'].setToolTip('Source Language')    #q acitonda oluşturduğumuz ikinci parametreler zaten tooltip gibi göründüğü için onlara yapmaya gerek yok ama qcomboboxlarınki fareyle üzerine gelince görünmüyor. bu ikisinielle ayarladık.
        self.toolbar_widget_dict['target_combobox']['widget'].setToolTip('Target Language')'''
        self.toolbar_widget_dict['pinned']['widget'].setCheckable(True)   #bu  pinned butonunu basılı tutulabilen hale getiriyor.
        self.toolbar_widget_dict['transparent']['widget'].setCheckable(True)    #basılı tutulabilir.
        self.toolbar_widget_dict['text']['widget'].setCheckable(True)    #basılı tutulabilir.
        self.toolbar_widget_dict['expand']['widget'].setCheckable(True) 
        self.toolbar_widget_dict['expand']['widget'].setChecked(True)       #uygulama açılırken basılı halde başlaması için. (genişlemiş halde başlıyodu zaten normalde. biz sadece bunu basılı olduğunu gösteriyoz böyle.)

        for key, value in self.toolbar_widget_dict.items():
            '''if value['widgettype'] == 'combobox':         #comboboxa uzun bişey eklersen tool button dikeyde sola yaslı kalıyor. zaten dil kodları kısa olduğu için burda bişey farketmiycek ama sonrası için uzun bişeyler eklersen değiştirmek gerekebilir.
                value['widget'].addItems(language)        #comboboxdaki dillerin otomatik olarak ikisinede eklenmesi için. eğer bi comboboxda olup ötekinde olmazsa change ile olmayan değişmiyor. o yüzden ikisininde aynı olması lazım. (ekleme yoluyla yine yapılabilir ama böylesi daha iyi)
                self.toolbar.addWidget(value['widget'])'''      #comboboxlar normalde main windowdaydı bu şekilde dilleri eklemiştim. ama speexhwidgete taşındı(çeviri yapıcağım widget). o yüzden kaldırıldı burası.
            if value['widgettype'] == 'toolbutton':           
                self.toolbar.addWidget(value['widget'])
            else:
                self.toolbar.addAction(value['widget'])
        #self.toolbar.addActions(self.toolbar_widget_dict.values())      #addactionsa butonların asıl hallerini değerler olarak kaydettiğimiz için buraya o şekilde giriyoruz.
        
        self.thema_menu = QMenu(self)
        for key in ThemaDict.keys():        #yazım yanlışlığı olmasın diye hem dicte hemde buraya ayrı ayrı yazmak yerine sadece dictteki genel tema isimlerini menüye ekliyoruz.
            self.thema_menu.addAction(QAction(key, self))
        

        self.toolbar_widget_dict['thema']['widget'].setMenu(self.thema_menu)
        self.toolbar_widget_dict['thema']['widget'].setPopupMode(QToolButton.InstantPopup)      #normalde bu menüyü oluşturunca bu menüyü açan tuşa normal basınca menü açılmıyor. bayağı baslı tutmak gerekiyor. ama;
                                                                                                #bu satırı ekleyince basar basmaz direk menü açılıyor.
        self.thema_menu.triggered.connect(lambda action: self.thema_menu_button_clicked(action.text()))


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
        self.image = ImageWidget(self)
        self.image.signal.connect(self.image_widget_signal)     #widget kapatılmadan önce ordaki resmin metnini sinyalle buraya gönderiyoruz. zaten orda sinyali str ile tanımladığımız için burda parametre olarak vermiyoruz, yönlendirdiğimiz fonksiyona hazır olarak gidiyor o.
        self.image.show()
        #self.image.showFullScreen() #direk tam ekran gibi gösteriyor
        

    def image_widget_signal(self,text):
        if text != '':      #boş metin yoksa işlemler yapılcak.
            self.speech_widget.ui.textEdit_source.setPlainText(text)
            if not self.toolbar_widget_dict['text']['widget'].isChecked():
                self.toolbar_widget_dict['text']['widget'].trigger()
        else:
            pass


    '''def change_button_clicked(self):     #burası comboboxlarla ilgiliydi ama speechwidgete taşındı o yüzden gerek kalmadı. sonrası için combobox eklersem diye yorum bıraktım.
        source_combobox = self.toolbar_widget_dict['source_combobox']['widget'].currentText()
        target_combobox = self.toolbar_widget_dict['target_combobox']['widget'].currentText()
        self.toolbar_widget_dict['source_combobox']['widget'].setCurrentText(target_combobox)
        self.toolbar_widget_dict['target_combobox']['widget'].setCurrentText(source_combobox)'''
        

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
                   

    def thema_menu_button_clicked(self, action):
        ThemaClass.update(ThemaDict[action])
        '''for i  in [self, self.speech_widget, self.msg_box]:      #stili olan ve mainwindowdan ayrı olarak açılan pencerelerede stili uygulamak için.
            i.setStyleSheet(ThemaClass.update_style_sheet())'''     #böyle döngü ile her penceresi olan widget yerine qapplicationu instance methodu ile bulup ona style uygularsak burdaki aynı işlemi yapmış oluyoruz.
        app = QApplication.instance()    #bu app kısmı asaşğıdaki uygulama oluştururken ki kısımda tanımlanıyor. ama instance ile ordaki örneğe erişip bunu istediğimiz yerden stilini değiştirmek için kullanabiliyoruz
        app.setStyleSheet(ThemaClass.update_style_sheet())

            
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
        

    def expand_button_clicked(self):
        if self.toolbar_widget_dict['expand']['widget'].isChecked():
            for i in self.toolbar_widget_dict.keys():
                self.toolbar_widget_dict[i]['widget'].setVisible(True)
        else:
            for i in self.toolbar_widget_dict.keys():
                if i in ['text', 'image_text', 'thema', 'expand', 'move']:
                    pass
                else:
                    self.toolbar_widget_dict[i]['widget'].setVisible(False)
        

        self.resize(self.sizeHint())        #bunu yapmadığımızda simgeler küçülmüşken bile ilk hali ölçülü kaldığı için move tuşuna tıklayınca ordaki haline göre konumlama yapıyordu.
                                            #yani kısa hali görünürken yatay haldeyken sağ kenara yaklaştırınca sanki uzun haldeymiş gibi boyutu alıp ona göre taşmaması için yeniden konumlandırıyordu. bu küçük hale geçincede büyük hale geçincede idaeal boyutlara göre konumlandırmayı yapıyor. 
        self.move_class.move_button_mouse_release_event()   #küçültme ve büyültme sonrasında durum değişmelerinden sonra ekran kenarlarına taşarsa tekrar ekran içinde konumlandırması için move tuşunun mouse bırakma sinyalini tetikliyoruz.
                    

    def minimize_button_clicked(self):
        self.showMinimized()

    def close_button_clicked(self):
        self.close()

    def move_button_clicked(self):  #bu buton veya herhangi bir widgetin taşınma olaylarını ayrı bir pyde tanımladık. hem tüm taşıma butonları için kod tekrarını azalttık hemde script daha düzenli oldu.
        self.move_class = MoveClass(self.toolbar_widget_dict['move']['widget'])
        self.toolbar_widget_dict['move']['widget'].mousePressEvent = self.move_class.move_button_mouse_press_event
        self.toolbar_widget_dict['move']['widget'].mouseMoveEvent = self.move_class.move_button_mouse_move_event
        self.toolbar_widget_dict['move']['widget'].mouseReleaseEvent = self.move_class.move_button_mouse_release_event
        
    def closeEvent(self, event): 
        self.speech_widget_close_signal()   #eğer speechwidget açıksa toolbardan çıkılırken onunda kapatılması için.
        super().closeEvent(event)
            
       
def app():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')          #genel pencere tasarımını değiştiriyor .en moderdi bu. diğer seçenekler arasında windowsvista ve Windows var. onlar çok eski ve kötü gözüküyor.
    ThemaClass.update(ThemaDict['Dark Mocha'])              #uygulama ilk başlarken ki uygulanacak olan tema.   
    app.setStyleSheet(ThemaClass.update_style_sheet())      #update fonksiyonu ile renkleri değiştirdikten sonra update fonksiyonunu tekrar hazırlayıp return ile bunu döndürüyoruz.  
                                                            #uygulamayı böyle başlatınca tüm oluşturduğum ayrı penceredeki widgetlere tek tek stylesheet yapmak zorunda kalmıyom. burdan uygulayınca direk mainwindowa bağlı tüm widgetlere uygulanıyor. penceresi olan widgetler için tek tek 200 satırlık stylesheet import edip bide tüm o içindeki widgetlere uygulamam gerekmiyor.
                                                            
    win = TranslateApp()                                    #eğer win oluşturulduktan sonra app.setstylesheet yaparsan uygulama oluşturulduğu için kesik kesik görünüyor boyutlandırmalar değiştiği için. o yüzden win oluşturulmadan önce yapmayı unutma app.setstylesheeti
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app()
    


