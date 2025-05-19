import os

from design import Ui_Form
from languages_code import tool_and_translate_matching
from msgbox_widget import MsgBox
from move_class import MoveClass

from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QApplication, QListView, QShortcut, QStyledItemDelegate
from PyQt5.QtCore import pyqtSignal, Qt, QSize, QEvent
from PyQt5.QtGui import QIcon, QFontMetrics, QKeySequence

import language_tool_python
from deep_translator import GoogleTranslator
import requests



class SpeechWidget(QWidget):
    close_signal = pyqtSignal()
    def __init__(self, screen_w, screen_h, screen_scale):
        super().__init__()
        self.screen_w, self.screen_h, self.screen_scale = screen_w, screen_h, screen_scale
        self.ui = Ui_Form()
        self.ui.setupUi(self)       #Arayüzü bu pencere (widget) üzerine kuruyosun.
        self.msg_box = MsgBox(self.screen_w, self.screen_h, self.screen_scale)
        self.combobox_dict = tool_and_translate_matching
        #self.pano = QApplication.clipboard()     #nadiren kullanılcağı için bu şekilde bellekte tutmak gereksizmiş. kopyala yapıştır butonlarında çağırmak en mantıklısı sürekli kullanmıycağımız için.
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(540*self.screen_scale, 390*self.screen_scale)
        self.button_icon_size = (20*self.screen_scale, 20*self.screen_scale)
        self.style_sheet_string = f'''
                            #Form{{         /* kullandığımız ana pencere Qwidget olduğu için buraya qwidget yazarsam tüm butonları falan buraya göre düzeltiyor çünkü hepsi qwidget kategorisinde
                                            o yüzden başına '#' bu işareti koyarak obje adını verdiğimizde sadece bu objeye tasarımı uyguluyor. obje adını şu şekilde öğrendim. print(self.objectName()).*/
                        background-color: rgb(36, 40, 48);
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
                            QComboBox {{
                        combobox-popup:0;   /*qcomboboxın açılır menüsü ekrenın en üstünden en altına kadaruzanıp bide alta ve üste buton ekliyordu. bunu bu şekilde çözdüm ne anlama geldiğini bilmiyorum internette yazılan tek çözüm. bunu 1 yapınca o boydan boya açılır pencere geliyor.
                                            0 yapınca normal combobox gibi oluyor hatta item sayısını da 0 yapınca ayarlayabiliyoruz maxvisibleitem fonksiyonuyla. ötekinde oda ayarlanmıyordu. tek sorun bunu böyle yapınca comboboxun
                                            açılır menüsü qlistviewe dönüşüyor galiba yani stil tanımlamalarına qlistviewide eklemememiz gerekiyor*/
                        background-color: rgb(30, 30, 30);          
                        color: rgb(220, 220, 220); 
                        border: {2*self.screen_scale}px solid rgb(100, 100, 100);
                        border-radius: {6*self.screen_scale}px;
                        padding: {4*self.screen_scale}px;
                        margin: {2*self.screen_scale}px;
                        font: bold {8*self.screen_scale}px;
                        }}
                            QComboBox::hover {{
                        background-color: rgb(220, 220, 220);
                        color: rgb(30, 30, 30);
                        }}
                            QComboBox QAbstractItemView {{              /* comboboxa tıklanıldıktan sonra açılan listenin tasarımı */
                        border: {2*self.screen_scale}px solid rgb(100, 100, 100);
                        border-radius: {6*self.screen_scale}px;
                        background-color: rgb(100, 100, 100);
                        padding: 0px;
                        margin: 0px;
                        }}
                            QComboBox QAbstractItemView::item {{        /*burası combobox açıldıktan sonra ki o listedeki itemleri kontrol ediyor padding margin burda uygulanınca oluyor. ama font burda uyarlanmıyor.*/
                        background-color: rgb(30, 30, 30);          
                        color: rgb(220, 220, 220); 
                        padding: {6*self.screen_scale}px;
                        margin: {2*self.screen_scale}px;
                        border-radius: {2*self.screen_scale}px;
                        border: none;
                        /*selection-background-color: rgb(0, 0, 0);*/       /* fareyle seçtiğimiz yazının arka planı */
                        selection-color: rgb(90, 191, 81);
                        }}
                            QListView{{                                 /*açılan listedekiyazıların font kısmınıda burda uyguluyoruz. marginle padding deburda uygulanmıyor.*/
                        font: bold {8*self.screen_scale}px;
                        text-align: center; 
                        }}
                            QComboBox::drop-down {{
                        width: 0px;
                        border: none;
                        }}
                            QComboBox:!editable {{ 
                        }}
                            QComboBox:editable {{   
                        }}
                            QComboBox::down-arrow {{         /* ok kısmının olduğu yer */
                        image: none;
                        width: 0px;
                        height: 0px;
                        }}
                            QTextEdit {{
                        background-color: rgb(30, 30, 30);          
                        color: rgb(220, 220, 220); 
                        selection-background-color: rgb(180,180,228);       /* fareyle seçtiğimiz yazının arka planı */
                        selection-color: rgb(38, 79, 195);
                        border: {2*self.screen_scale}px solid rgb(60, 60, 60);
                        padding: {6*self.screen_scale}px;
                        font:  {10*self.screen_scale}px;
                        }}
                            QScrollBar:vertical, QScrollBar:horizontal  {{
                        background: rgb(30, 30, 30);
                        width: {6*self.screen_scale}px;
                        border-radius: {2*self.screen_scale}px;
                        margin: 0px;
                        }}
                            QScrollBar::handle:vertical, QScrollBar::handle:horizontal{{
                        background: rgb(200, 200, 200);
                        min-height: {10*self.screen_scale}px;
                        border-radius: {2*self.screen_scale}px;
                        }}
                            QScrollBar::handle:vertical:pressed, QScrollBar::handle:horizontal:pressed {{  /* scrollbar tutma yeri için hover olayıda var lazım olursa kullan */
                        background: rgb(90, 170, 81);
                        }}
                            QScrollBar::add-line:vertical,
                            QScrollBar::sub-line:vertical,
                            QScrollBar::add-line:horizontal,
                            QScrollBar::sub-line:horizontal {{
                        height: 0px;
                        }}
                            QScrollBar::corner {{       /* Köşe birleşimi */
                        background: rgb(30, 30, 30);
                        }}

                                            '''
        self.setStyleSheet(self.style_sheet_string)
        self.install_icons()
        self.button_clicks()        #tüm pushbuttonları 'pushButton_' böyle başlat. 
        self.install_combobox_items()
        self.combobox_source_text = self.ui.comboBox_source.currentText()
        self.combobox_target_text = self.ui.comboBox_target.currentText()
        self.layout_settings()
        self.move_button_click()    #movebutonunun override edilcek mouse eventlerini tanımlıyoruz. butonun tıklanma fonksiyonunu döngüde kaldırdık.
        
        self.ui.textEdit_source.installEventFilter(self)    #textedit source için oraya odaklıyken ki tuş basımlarını yakalayıp sistemin kendi ctrl + v kombosunu ezip kendi yöntemimizi ekliyoruz.çünkü;
                                                            #bunu yapmazsak vscoddan yada internetten bişey kopyalanınca oranın stilini ve yazı tipini falan alıyor öyle kopyalıyor.font ayarlarıyla beraber kopyalıyor yani.html içerinin hepsini alıyor.
                                                            #bizde bunu istemediğimiz için event filtrelemeye gönderip sadece texti alıp bunu yapıştırmasını söyledik ve sistemin ctrl + v fonksiyonunu override ettik.      


    def install_icons(self):
        self.ui.pushButton_change_language.setIcon(QIcon(os.path.join('icon','lang_change.png')))
        self.ui.pushButton_close.setIcon(QIcon(os.path.join('icon','close.png')))
        self.ui.pushButton_move.setIcon(QIcon(os.path.join('icon','move.png')))
        self.ui.pushButton_minimize.setIcon(QIcon(os.path.join('icon','minimize.png')))
        self.ui.pushButton_info.setIcon(QIcon(os.path.join('icon','info.png')))
        self.ui.pushButton_change_text.setIcon(QIcon(os.path.join('icon','text_change.png')))
        self.ui.pushButton_correct_text.setIcon(QIcon(os.path.join('icon','correct_text.png')))
        self.ui.pushButton_translate.setIcon(QIcon(os.path.join('icon','translation.png')))
        self.ui.pushButton_copy_s.setIcon(QIcon(os.path.join('icon','copy.png')))
        self.ui.pushButton_paste_s.setIcon(QIcon(os.path.join('icon','paste.png')))
        self.ui.pushButton_clear_s.setIcon(QIcon(os.path.join('icon','clear.png')))
        self.ui.pushButton_copy_t.setIcon(QIcon(os.path.join('icon','copy.png')))
        self.ui.pushButton_paste_t.setIcon(QIcon(os.path.join('icon','paste.png')))
        self.ui.pushButton_clear_t.setIcon(QIcon(os.path.join('icon','clear.png')))
        

        for button in self.findChildren(QPushButton): #tüm butonların boyutunu döngüyle daha kısa halde değiştiriyoruz.
            '''print(button.objectName())'''    #tüm pushbuttonların ismini alma.
            button.setIconSize(QSize(self.button_icon_size[0], self.button_icon_size[1]))

    def button_clicks(self):        
        for button in self.findChildren(QPushButton):     #tüm pushbuttonlara isim verirken hepsini 'pushButton_' bu şekilde başlatmıştım. 
                                                                    #o yüzden aşağıda o fonksiyonlara yönlendirirken hepsini tek tek yazmak yerine döngüde str olarak o fonksiyonların isimlerini veriyorum. 
                                                                    #ve hepsi aynı şekilde başladığı için replace methodu ile başlarındaki 'pushButton_' kelimesini kaldırıyorum.
            button_name = f'{button.objectName().replace('pushButton_','')}_button_click'
            if button_name == 'move_button_click':  #move butonu için mouse olaylarnı overide edeceğimiz için bu butonun fonksiyon bağlamasını kaldırıyoruz döngüde.
                continue                            #bunu yukarda girişte override edilcek fonksiyonları tanımlamak için kullanıcaz
            if hasattr(self, button_name):      #hasattr nin kullanımı; ikinci verilen parametrede o isimde bir fonksiyon olup olmadığını döndürüyor. yani bu satırda bu isimde  bir fonksiyon varmı diye kontrol edip varsa aşağıdaki şekilde o fonksiyona yönlendiriyoruz.
                                                #sadece getattr ile kullanınca o isimde fonksiyon yoksa hata veriyor. ama böyle kullanırsak o isimde varsa ynlendirmeyi yapmış oluyoruz. hasattr ve getattr ikisi güzel uyumlu oluyor
                button.clicked.connect(getattr(self, button_name))  #bu satırın anlamı;
                                                                    #tüm pushbutonların başındaki 'pushButton_' kelimesini atıp sonuna _button_click ekleyerek o fonksiyona yönlendirmek demek.
                                                                    #fonksiyonları str olarak veriyoruz yani. daha sistematik. ama tüm butonları 'pushButton_' böyle başlattığına emin ol. yoksa çalışmaz burası.
        self.ui.textEdit_target.setReadOnly(True)       #qplaintextte sadece kopyalama seçme gibi işlemlere zin veriyor. kullanıcı burdaki metne ekleme ve çıkarma yapamasın diye.(çeviri sonucu olcağı için böyle ayarlandı.)
        self.ui.pushButton_info.setCheckable(True)
        

    def install_combobox_items(self):
        for combobox in [self.ui.comboBox_source, self.ui.comboBox_target]:
            for item in self.combobox_dict:
                combobox.addItem(item)
            combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  #comboboxun içine scrollbar eklemek için. (comboboxa eklenen itemler fazla olunca scrolbar yerine aşağıda ve yukarda buton çıkıyor.)
            combobox.setMaxVisibleItems(10)  #comboboxda aynı anda gösterilcek item sayısı sınırlama
            combobox.view().setViewportMargins(0,0,4*self.screen_scale,0) 
            combobox.setView(QListView())
            
            #combobox.currentTextChanged.connect(lambda text, cb = combobox: self.current_text_changed(cb))    #lambdanın yanındaki alt çizginin anlamı: normalde bu current changed sinyali bir str gönderiyor hazırda. ama biz hangi comboboxtan geldiğini hesaba katıyoruz. yani bu str yi göndersen bile kullanmıycaz demek oluyor _ işareti.
                                                                                                                    #o _işareti aslında sinyalin gönderdiği stryi ifade ediyormuş ve lambdada bunu kullanmasak bile belirtmediğimizde hata veriyor. o yüzden bi yer tutucu gibi bişeymiş sabit bi fonksiyon yada simge değil. onu silip text yazdım zaten str göndercekti bu fonksiyon. yada direk aşağıdaki şekle dönüştürebiliriz.
            combobox.currentTextChanged.connect(lambda text, cb = combobox: self.current_text_changed(text, cb)) 
            
        auto = self.ui.comboBox_target.findText('Auto')     #textin indexini döndürüyor
        self.ui.comboBox_target.removeItem(auto)            #indexi siliyor.
        self.ui.comboBox_source.setCurrentText('Auto')
        self.ui.comboBox_target.setCurrentText('Turkish')
        #print(self.ui.comboBox_source.view()) comboboxun açılır menüsünün widget türünü öğrenme
        
    def current_text_changed(self, text, cb):
        if cb == self.ui.comboBox_source:
            self.combobox_source_text = text
        else:
            self.combobox_target_text = text
            
        
        


    def layout_settings(self):
        m_s_r = 6*self.screen_scale   #m_s_r ---> margin_spacer_ratio anlamında kısalttım
        self.setContentsMargins(m_s_r, 0, m_s_r, 0)     #burası text editlerin ana pencere kenarlarında sıfır olarak durmasını engellemek için yazıldı. yani hafif bi kenarlıkmış gibi görünmesi için
        self.ui.layout_toolbar.setContentsMargins(m_s_r, m_s_r, m_s_r, m_s_r)
        self.ui.layout_source_button.setContentsMargins(m_s_r, m_s_r, m_s_r, m_s_r)
        self.ui.layout_target_button.setContentsMargins(m_s_r, m_s_r, m_s_r, m_s_r)
        self.ui.layout_combobox.setContentsMargins(m_s_r, m_s_r, m_s_r, m_s_r)
        self.ui.layout_toolbar.setSpacing(m_s_r)
        self.ui.layout_source_button.setSpacing(m_s_r)
        self.ui.layout_target_button.setSpacing(m_s_r)
        self.ui.layout_combobox.setSpacing(m_s_r)

        self.ui.textEdit_source.setViewportMargins(0,0,4*self.screen_scale,0)   #texteditin içinde metin scroolbara fazla yakın oluyordu ve paddingle marginle ayarlanmıyordu. bizde metni scrollbardan bu şekilde uzaklaştırıyoruz.
        self.ui.textEdit_source.setViewportMargins(0,0,4*self.screen_scale,0)   #Soldan 0 px, Yukarıdan 0 px, Sağdan 20 px (yani metin scrollbar’dan 8 px uzağa çekilir) , Alttan 0 px
        
        


    def change_language_button_click(self):
        source_combobox = self.ui.comboBox_source.currentText()
        target_combobox = self.ui.comboBox_target.currentText()
        self.ui.comboBox_source.setCurrentText(target_combobox)
        self.ui.comboBox_target.setCurrentText(source_combobox)

    def close_button_click(self):
        self.close()
    
    def minimize_button_click(self):
        self.showMinimized()

    def move_button_click(self):    #burası init kısmında sadece bir defa çalıştırılcak şekilde ayarlandı. movebutonu için olan mouse eventlerini override ettiğimiz yer. tüm move işlemleri için moveclası hazırladık , değişkenleri oraya gönderiyoruz ve her  pencere widgeti için tek tek eklemek zorunda kalmıyoruz.
        self.move_class = MoveClass(self.ui.pushButton_move, self.screen_w, self.screen_h)
        self.ui.pushButton_move.mousePressEvent = self.move_class.move_button_mouse_press_event
        self.ui.pushButton_move.mouseMoveEvent = self.move_class.move_button_mouse_move_event
        self.ui.pushButton_move.mouseReleaseEvent = self.move_class.move_button_mouse_release_event

    

    def info_button_click(self):                #!!!!!!!buraya sonra açılır bi iletişim penceresi eklencek unutma
        if self.ui.pushButton_info.isChecked():
            self.ui.pushButton_change_language.setToolTip('Change Languages')
            self.ui.pushButton_close.setToolTip('Close')
            self.ui.pushButton_move.setToolTip('Move')
            self.ui.pushButton_minimize.setToolTip('Minimize')
            self.ui.pushButton_info.setToolTip('Info')
            self.ui.pushButton_change_text.setToolTip('Change Texts')
            self.ui.pushButton_correct_text.setToolTip('Correct Text')
            self.ui.pushButton_translate.setToolTip('Translate')
            self.ui.pushButton_copy_s.setToolTip('Copy')
            self.ui.pushButton_paste_s.setToolTip('Paste')
            self.ui.pushButton_clear_s.setToolTip('Clear')
            self.ui.pushButton_copy_t.setToolTip('Copy')
            self.ui.pushButton_paste_t.setToolTip('Paste')
            self.ui.pushButton_clear_t.setToolTip('Clear')
            self.ui.comboBox_source.setToolTip('Source Language')
            self.ui.comboBox_target.setToolTip('Target Language')
        else:
            for button in self.findChildren(QPushButton):
                button.setToolTip(None)     #settooltipleri sıfırlama, varsayılanı bu zaten
            for combobox in self.findChildren(QComboBox):
                combobox.setToolTip(None)     #settooltipleri sıfırlama, varsayılanı bu zaten

    def change_text_button_click(self):
        source_textedit = self.ui.textEdit_source.toPlainText()
        target_textedit = self.ui.textEdit_target.toPlainText()
        self.ui.textEdit_source.setPlainText(target_textedit)
        self.ui.textEdit_target.setPlainText(source_textedit)
    
    def correct_text_button_click(self):
        #tool_and_translate_matching['Slovenian (Generic)']['language_tool']
        #tool_and_translate_matching['Slovenian (Generic)']['deep_translator']
        tool = None     #local değişlende bunu burda tanımlamazsak eğer tryda hata verirse finally bloğunda toolu görmüyor ve hata veriyor. o yüzden burda none ile tanımlayıp finalliyde ona göre işlem yapıyoruz.
        if self.combobox_source_text == 'Turkish':  #kelime ve gramer düzeltme türkçeyi desteklemiyor o yüzden dil türkçeyse düzeltme uygulamıyoruz.
            return
        
        else:
            try:
                tool = language_tool_python.LanguageToolPublicAPI(self.combobox_dict[self.combobox_source_text]['language_tool'])
                text = self.ui.textEdit_source.toPlainText()
                correct = tool.correct(text)
                self.ui.textEdit_source.setPlainText(correct)
            except language_tool_python.utils.RateLimitError:
                self.msg_box.edit("You've reached the maximum number of requests for now. Please wait a little while.The correction feature will be available again shortly !")
            except language_tool_python.utils.LanguageToolError:
                self.msg_box.edit('Internet Connection Lost !')
            finally:
                if tool is not None:
                    tool.close()   #kaynak güvenilği açısından en temizi her düzeltme sonrası bağlantıyı kapatmak olduğu için her buton tıklaması sonrası kapatıyoz bunu. hem ratelimitede daha geç dolduruyor böylece.

            
        

    def translate_button_click(self):
        #print(self.translate.get_supported_languages(as_dict=True))        #desteklenen dilleri görmek için(sadece uzun hallerini görmek istersen parantez içini sil)
        text = self.ui.textEdit_source.toPlainText()
        if text.strip() == '':      #eğer kullanıcı hiç bişey yazmamışsa yada sadece boşluk koymuşsa çeviri yapmaması için
            self.msg_box.edit('No text found to translate !')
            return      #fonksiyonun bitmesi için. yani bu if bloğu çalışırsa alt kısım çalışmıycak o kısma geçmiycek demek.
        try:
            translate = GoogleTranslator(source = self.combobox_dict[self.combobox_source_text]['deep_translator'], target = self.combobox_dict[self.combobox_target_text]['deep_translator']).translate(text=text)
            self.ui.textEdit_target.setPlainText(translate)
        except requests.exceptions.ConnectionError:
            self.msg_box.edit('Internet Connection Lost !')
        
    def copy_s_button_click(self):
        if self.ui.textEdit_source.textCursor().selectedText() != '':   #eğer kullanıcı imleçle herhangi bişey seçmişse, o seçili alanı panoya kopyalıycak
            QApplication.clipboard().setText(self.ui.textEdit_source.textCursor().selectedText())
        else:                                                           #eğer hiç bişey seçili değilse textin tamamını kopyalıycak
            QApplication.clipboard().setText(self.ui.textEdit_source.toPlainText())

    def paste_s_button_click(self):
        self.ui.textEdit_source.textCursor().insertText(QApplication.clipboard().text())      #yapıştırma butonu comple silmek yerine imlecin konumunu alıp, oraya ekliyor kopyalanan kısmı.(zaten silme butonu var eğer silip yapıştırılmasını isterse diye o seçenekte açık.)

    def clear_s_button_click(self):
        self.ui.textEdit_source.clear()

    def copy_t_button_click(self):
        if self.ui.textEdit_target.textCursor().selectedText() != '':
            QApplication.clipboard().setText(self.ui.textEdit_target.textCursor().selectedText())
        else:
            QApplication.clipboard().setText(self.ui.textEdit_target.toPlainText())

    def paste_t_button_click(self):
        self.ui.textEdit_target.textCursor().insertText(QApplication.clipboard().text())

    def clear_t_button_click(self):
        self.ui.textEdit_target.clear()

        
    def eventFilter(self, obj, event):
        if obj == self.ui.textEdit_source and event.type() == QEvent.KeyPress and event.modifiers() == Qt.ControlModifier:
            if  event.key() == Qt.Key_V:
                self.ui.pushButton_paste_s.click()
                return True  # sinyali biz hallettik diyoz qtye
        return super().eventFilter(obj, event)  # Diğer her şeyi normal devam etsin


    def closeEvent(self,event):
        self.close_signal.emit()
        print('Speech kapatıldı')
        super().closeEvent(event)
      
'''    ----------------------
  
        self.github = self.ui.label_github.text()
        self.gmail = self.ui.label_gmail.text()
        self.pano = QApplication.clipboard()      #kullanıcının  panoya ulaşması oraya bişeyler kopyalayıp yada panodaki kopyalı olanı yapıştırabilmesi için pyqtnin kendi fonksiyonu.

        self.ui.pushButton_close.clicked.connect(self.window().close)
        self.ui.pushButton_github.clicked.connect(self.button_github)
        self.ui.pushButton_gmail.clicked.connect(self.button_gmail)
        self.load_icon()

    def load_icon(self):
        icon_size_button = 40,40
        self.ui.pushButton_close.setIcon(QIcon(os.path.join('icon','close.png'))) 
        self.ui.pushButton_github.setIcon(QIcon(os.path.join('icon','copy.png'))) 
        self.ui.pushButton_gmail.setIcon(QIcon(os.path.join('icon','copy.png'))) 
        
        self.ui.pushButton_close.setIconSize(QSize(icon_size_button[0],icon_size_button[1]))
        self.ui.pushButton_github.setIconSize(QSize(icon_size_button[0],icon_size_button[1]))
        self.ui.pushButton_gmail.setIconSize(QSize(icon_size_button[0],icon_size_button[1]))


    def button_github(self):
        self.pano.setText(self.github)      #butona tıklanınca panoya kopyalaması için

    def button_gmail(self):
        self.pano.setText(self.gmail)       #butona tıklanınca panoya kopyalaması için'''