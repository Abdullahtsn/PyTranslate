from screen_scale import ScreenSize
from dataclasses import dataclass
import sys
import os


if getattr(sys,'frozen', False):            #burasını stylesheet içinde comboboxlara ok butonu için resim ayarlıyorum o yüzden ekledim. okun yolunu doğru bulması için yolu ona göre ayarlıyorum. 
    os.chdir(sys._MEIPASS)
else:                       
    os.chdir('.')
 
screen_w, screen_h, screen_scale = ScreenSize().values() 

@dataclass                          #python kendi fonksiyonlarından biri. normal class ile benzer gibi düşünebilirsin ama bu daha az kodla daha iyi eşleştirmeler ve bazı otomatikleştirmeler sağlıyor.
                                    #mesela normal classta her değişkene erişebilmek için tek tek inite hem gönderiyosun hemde self diyerek hepsini tek tek tanımlıyosun. dataclass ile bu yükten kurtuluyosun initi kendi otomatik yapıyor.
                                    #dataclass, yazdığın alanlardan otomatik olarak yapıcı (__init__), gösterici (__repr__), karşılaştırıcı (__eq__), sıralayıcı (__lt__, __gt__) gibi metodları kendisi üretir. dataclass üretmek için @dataclass yazdıktan sonra altında normal sınıf tanımla.
class Thema:
    mainwindow_bg : str = ''        # : -> bu tip belirtiyor. = buda normal kullandığımız değer atama için. tüm değişkenler için string boşluk atadık yani.
    toolbar_bg : str = '' 
    i_widget_bg : str = '' 
    form_bg : str = ''
    button_bg : str = '' 
    button_color : str = '' 
    button_border : str = '' 
    button_checked_bg : str = '' 
    button_checked_color : str = ''
    button_checked_border : str = ''
    button_hover_bg : str = '' 
    button_hover_color : str = ''
    button_hover_border : str = ''
    button_pressed_bg : str = '' 
    button_pressed_color : str = ''
    button_pressed_border : str = ''
    combobox_bg : str = ''
    combobox_color : str = '' 
    combobox_border : str = '' 
    combobox_hover_bg : str = ''
    combobox_hover_color : str = '' 
    combobox_hover_border : str = '' 
    combobox_abstract_bg : str = '' 
    combobox_abstract_border : str = ''
    combobox_abstractitem_bg : str = '' 
    combobox_abstractitem_color : str = '' 
    combobox_item_hover_color : str = '' 
    combobox_item_hover_bg : str = '' 
    messagebox_bg : str = '' 
    messagebox_color : str = '' 
    messagebox_label_bg : str = '' 
    messagebox_label_color : str = '' 
    messagebox_button_color : str = '' 
    messagebox_button_bg : str = '' 
    textedit_bg : str = '' 
    textedit_color : str = ''
    textedit_selectbg : str = ''
    textedit_selectcolor : str = ''
    textedit_border : str = ''
    checkbox_indicator_bg : str = '' 
    scrollbar_vrt_hrz_bg : str = ''
    scrollbar_handle_bg : str = ''
    scrollbar_pressed_bg : str = ''
    scrollbar_corner_bg : str = ''
    menu_bg : str = '' 
    menu_color : str = ''
    menu_border : str = '' 
    menu_item_bg : str = ''
    menu_item_color : str = ''
    menu_item_border : str = ''
    menu_item_selected_bg : str = ''
    menu_item_selected_color : str = ''
    menu_item_selected_border : str = ''
    

    def update(self, thema_dict):       #sadece tek bi thema clası oluşturuyoruz. tema değişimleri için sadece bunu güncelliyoruz. ayrı ayrı her tema için ayrı dataclass oluşturmaya gerek yok. değerler sözlükte saklı zaten.
        for key, value in thema_dict.items():   #sözlüğü alıp key ve valuelerini dönüyoruz. zaten sözlükten gelen keyler bu sınıftaki değişkenlerle aynı.. sonrasında dinamik olarak settattr ile değişkenleri güncelliyoruz.
            setattr(self, key, value)       #burda normalde her değişken için self.mainwindow = value falan yazcaktık ama onlarca satırı böyle uzatmanın mantığı yok.
                                            #burda kısaca setattr(self, key, value) dedik. bu self.key = value demenin dinamik hali. zaten değişkenleri aynı. aynı omadığında hata vericek. eğer farklı bişey yaparsan ve aynı olmayanları kullanıcak olursan hasattr koy
        

    def update_style_sheet(self):
        style_sheet_string = (f'''
                            QMainWindow {{
                        background-color: {self.mainwindow_bg} ;
                        margin: 0px; 
                        padding: 0px; 
                        border:none; 
                        }}
                            QToolBar {{ 
                        background-color: {self.toolbar_bg}; 
                        padding: 0px; 
                        spacing: 0px; 
                        border:none; 
                        }}  
                            QPushButton, QToolButton {{
                        background-color: {self.button_bg} ; 
                        text-align: center; 
                        padding: {1*screen_scale}px; 
                        margin: 0px; 
                        spacing: 0px; 
                        border-radius:{2*screen_scale}px;
                        border-style: solid;
                        border-width: {1*screen_scale}px;
                        border-color: {self.button_border};
                        color: {self.button_color};
                        }}
                            QPushButton:checked, QToolButton:checked {{       /* bu yöntemle sadece butonun basılı tutulma halini kontrol ediyorum ve diğer hiç bi varsayılan ayarı değiştirmiyoruz. özellikle pinned butonu için çok faydalı oldu. */
                        background-color: {self.button_checked_bg};
                        border-color: {self.button_checked_border};
                        color: {self.button_checked_color};
                        }}
                            QPushButton:hover, QToolButton:hover {{
                        background-color: {self.button_hover_bg};
                        border-color: {self.button_hover_border}; 
                        color: {self.button_hover_color};
                        }}
                            QPushButton:pressed, QToolButton:pressed {{
                        border-color: {self.button_pressed_border}; 
                        background-color: {self.button_pressed_bg}; 
                        color:  {self.button_pressed_color};
                        }} 
                           QToolButton#qt_toolbar_ext_button {{     /*toolbarda hazır gelen extansion butonunu görünmez gibi yapma*/
                        border: none;
                        padding: 0px;
                        margin: 0px;
                        max-width: 0px; 
                        }}
                            #i_widget {{
                        background-color: {self.i_widget_bg};
                        }}
                            QComboBox {{
                        combobox-popup:0;   /*qcomboboxın açılır menüsü ekrenın en üstünden en altına kadaruzanıp bide alta ve üste buton ekliyordu. bunu bu şekilde çözdüm ne anlama geldiğini bilmiyorum internette yazılan tek çözüm. bunu 1 yapınca o boydan boya açılır pencere geliyor.
                                            0 yapınca normal combobox gibi oluyor hatta item sayısını da 0 yapınca ayarlayabiliyoruz maxvisibleitem fonksiyonuyla. ötekinde oda ayarlanmıyordu. tek sorun bunu böyle yapınca comboboxun
                                            açılır menüsü qlistviewe dönüşüyor galiba yani stil tanımlamalarına qlistviewide eklemememiz gerekiyor*/
                        background-color: {self.combobox_bg};          
                        color: {self.combobox_color}; 
                        border: {0.5*screen_scale}px ridge {self.combobox_border};
                        border-radius: {1*screen_scale}px;
                        padding: {2*screen_scale}px;
                        padding-left: {4*screen_scale}px;
                        padding-right: {10*screen_scale}px; /*bunu koymamın sebebi uzun itemlerin textleri buton resmiyle altlı üstlü oluyor. o yüzden buton  resmi için yer açıyoruz*/
                        margin: {1*screen_scale}px;
                        font: bold {4*screen_scale}px;
                        outline: none;
                        }}
                            QComboBox::hover {{
                        background-color: {self.combobox_hover_bg};
                        color: {self.combobox_hover_color};
                        border-color: {self.combobox_hover_border}; 
                        }}
                            QComboBox QAbstractItemView {{              /* comboboxa tıklanıldıktan sonra açılan listenin tasarımı */
                        border: {1*screen_scale}px dashed {self.combobox_abstract_border};     /*açılır menü dış kenarlık*/
                        border-radius: {1*screen_scale}px;
                        background-color: {self.combobox_abstract_bg};                               /*açılır menü iç renk*/
                        padding: {2*screen_scale}px;
                        margin: 0px;
                        font: bold {4*screen_scale}px;
                        outline: none;                /*açılan listede fare itemin üzerine gelince küçük gri noktalar yada border gibi şeyler çiziyordu.outline none yaparak bundan kurtulduk.*/
                        }}
                            QComboBox QAbstractItemView::item {{        /*burası combobox açıldıktan sonra ki o listedeki itemleri kontrol ediyor padding margin burda uygulanınca oluyor. ama font burda uyarlanmıyor.*/
                        background-color: {self.combobox_abstractitem_bg};          
                        color: {self.combobox_abstractitem_color}; 
                        padding: {3*screen_scale}px;
                        margin: {1*screen_scale}px;
                        border-radius: {1*screen_scale}px;
                        selection-color: {self.combobox_item_hover_color};
                        outline: none;
                        }}
                            QComboBox QAbstractItemView::item:hover {{      /*burda yazı rengi değişmiyor. üzerine gelince yazının renginin değişmesini istiyorsanQAbstractItemView::item selection-coloru ayarla. orda yapınca üzerine gelince renk değiştiriyor yazı.*/
                        background-color: {self.combobox_item_hover_bg}; 
                        }}
                            QComboBox::drop-down {{
                        width: 0px;
                        border: none;
                        border-radius: {3*screen_scale}px;
                        outline: none;
                        }}
                            QComboBox:!editable {{ 
                        }}
                            QComboBox:editable {{   
                        }}
                            QComboBox::down-arrow {{         /* ok kısmının olduğu yer */
                        width: {7*screen_scale}px;
                        height: {7*screen_scale}px;
                        padding-right: {10*screen_scale}px;
                        image: url(icon/down.png); 
                        }}      
                            QMessageBox {{
                        background-color: {self.messagebox_bg}; 
                        color: {self.messagebox_color};         
                        padding: 0px;
                        margin: 0px;   
                        }}
                            QMessageBox QLabel {{
                        font: bold {4*screen_scale}px;
                        background-color: {self.messagebox_label_bg}; 
                        color: {self.messagebox_label_color};
                        padding: 0px;
                        margin:0px;
                        }}
                            QMessageBox QPushButton {{          /*buton için varsayılan ayarları kullandık sadece yazıyla oynadık, eğer özelleştirmek istersen aşağıdaki düzenle*/
                        font: bold {4*screen_scale}px;
                        color: {self.messagebox_button_color}; 
                        background-color: {self.messagebox_button_bg}; 
                        }}
                            #Form{{         /* kullandığımız ana pencere Qwidget olduğu için buraya qwidget yazarsam tüm butonları falan buraya göre düzeltiyor çünkü hepsi qwidget kategorisinde
                                            o yüzden başına '#' bu işareti koyarak obje adını verdiğimizde sadece bu objeye tasarımı uyguluyor. obje adını şu şekilde öğrendim. print(objectName()).*/
                        background-color: {self.form_bg};
                        }}
                            QTextEdit {{
                        background-color: {self.textedit_bg};          
                        color: {self.textedit_color}; 
                        selection-background-color: {self.textedit_selectbg};       /* fareyle seçtiğimiz yazının arka planı */
                        selection-color: {self.textedit_selectcolor};
                        border: {1*screen_scale}px solid {self.textedit_border};
                        padding: {3*screen_scale}px;
                        }}
                            QCheckBox::indicator {{
                        width: {10*screen_scale}px;
                        height: {10*screen_scale}px; 
                        image: url(/icon/unchecked.png);    /*checkboxa resim ekleme. o tik işareti yerine kendi resmimizi koyabiliyoruz.*/
                        background-color: {self.checkbox_indicator_bg};
                        border: none;
                        padding: 0px;
                        margin: 0px;
                        }}
                            QCheckBox::indicator:checked {{ /*checkbox seçiliyken olan ayarlar*/
                        image: url(icon/checked.png); 
                        }}
                            QCheckBox::indicator:unchecked {{ /*seçili değilkenki ayarlar ama zaten başlangıçta belirtsekte oluyor bunları. lazım olursa diye bıraktım burayı*/
                        }}

                            QScrollBar:vertical, QScrollBar:horizontal  {{
                        background-color: {self.scrollbar_vrt_hrz_bg};
                        width: {3*screen_scale}px;
                        border-radius: {1*screen_scale}px;
                        margin: 0px;
                        }}
                            QScrollBar::handle:vertical, QScrollBar::handle:horizontal{{
                        background-color: {self.scrollbar_handle_bg};
                        min-height: {5*screen_scale}px;
                        border-radius: {1*screen_scale}px;
                        }}
                            QScrollBar::handle:vertical:pressed, QScrollBar::handle:horizontal:pressed {{  /* scrollbar tutma yeri için hover olayıda var lazım olursa kullan */
                        background-color: {self.scrollbar_pressed_bg};
                        }}
                            QScrollBar::add-line:vertical,
                            QScrollBar::sub-line:vertical,
                            QScrollBar::add-line:horizontal,
                            QScrollBar::sub-line:horizontal {{
                        height: 0px;
                        }}
                            QScrollBar::corner {{       /* Köşe birleşimi */
                        background-color: {self.scrollbar_corner_bg};
                        }}

                            QMenu {{
                        background-color: {self.menu_bg};
                        color: {self.menu_color};
                        border: {self.menu_border};
                        margin: {1*screen_scale}px; 
                        }}

                            QMenu::item {{
                        padding: {2*screen_scale};
                        border: 0px solid {self.menu_item_border}; 
                        background-color: {self.menu_item_bg};
                        color: {self.menu_item_color};
                        }}

                            QMenu::item:selected {{
                        border-color: dark{self.menu_item_selected_border};
                        background-color: {self.menu_item_selected_bg};
                        color: {self.menu_item_selected_color};
                        }}

                            QMenu::indicator {{
                        width: {4*screen_scale};
                        height: {4*screen_scale};
                        }}
                                                ''')   
        return style_sheet_string       #setstylesheet fonksiyonuna direk burdaki fonksiyonu verince renkleri değiştirip bu stringi geri gönderip uygulaması için return yapıyoz.


ThemaClass = Thema()   #burda oluşturdum ki genel tanım olsun her yerden erişilebilir olsun.


ThemaDict = {                  #thema menüsündeki seçeneklerle birebir uyumlu olsun tema iisimleri unutma
'Dark Mocha' : {  
    'mainwindow_bg' : 'transparent', 
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#0f0e0d',
    'form_bg' : '#1a1816',
    'button_bg' : '#2b241e',
    'button_color' : '#e8e6e3',
    'button_border' : '#3c342c',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg' : '#362f29',
    'button_hover_color' : '#f0eeec',
    'button_hover_border' : '#7a9980',
    'button_pressed_bg' : '#3a2e25',
    'button_pressed_color' : '#ffffff',
    'button_pressed_border' : '#5e4b3c',
    'combobox_bg' : '#1e1c1a',
    'combobox_color' : '#e6e3df',
    'combobox_border' : '#3a332c',
    'combobox_hover_bg' : '#2b2622',
    'combobox_hover_color' : '#f2f1ee',
    'combobox_hover_border' : '#4c4236',
    'combobox_abstract_bg' : '#151311',
    'combobox_abstract_border' : '#2c2621',
    'combobox_abstractitem_bg' : '#241f1b',
    'combobox_abstractitem_color' : '#dedbd7',
    'combobox_item_hover_color' : '#ffffff',
    'combobox_item_hover_bg' : '#4a3d33',
    'messagebox_bg' : '#191715',
    'messagebox_color' : '#e7e4e0',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#f0efed',
    'messagebox_button_color' : '#ffffff',
    'messagebox_button_bg' : '#4d3f35',
    'textedit_bg' : '#12100f',
    'textedit_color' : '#e8e6e3',
    'textedit_selectbg' : '#5a483b',
    'textedit_selectcolor' : '#ffffff',
    'textedit_border' : '#3b332c',
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#1e1c1a',
    'scrollbar_handle_bg' : '#4c3f34',
    'scrollbar_pressed_bg' : '#3e3229',
    'scrollbar_corner_bg' : '#1a1816',
    'menu_bg' : '#0f0e0d',
    'menu_color' : '#e8e6e3',
    'menu_border' : '#3b342d',
    'menu_item_bg' : '#2b241e',
    'menu_item_color' : '#e8e6e3',
    'menu_item_border' : '#3c342c',
    'menu_item_selected_bg' : '#4e3f33',
    'menu_item_selected_color' : '#ffffff',
    'menu_item_selected_border' : '#5a483b'},

'Midnight Terminal': {
    'mainwindow_bg': 'transparent',
    'toolbar_bg': 'transparent',
    'i_widget_bg': '#0d1117',
    'form_bg': '#161b22',
    'button_bg': '#21262d',
    'button_color': '#c9d1d9',
    'button_border': '#30363d',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg': '#30363d',
    'button_hover_color': '#f0f6fc',
    'button_hover_border': '#7a9980',
    'button_pressed_bg': '#1f6feb',
    'button_pressed_color': '#ffffff',
    'button_pressed_border': '#388bfd',
    'combobox_bg': '#161b22',
    'combobox_color': '#c9d1d9',
    'combobox_border': '#30363d',
    'combobox_hover_bg': '#21262d',
    'combobox_hover_color': '#ffffff',
    'combobox_hover_border': '#484f58',
    'combobox_abstract_bg': '#0d1117',
    'combobox_abstract_border': '#30363d',
    'combobox_abstractitem_bg': '#21262d',
    'combobox_abstractitem_color': '#c9d1d9',
    'combobox_item_hover_color': '#ffffff',
    'combobox_item_hover_bg': '#388bfd',
    'messagebox_bg': '#0d1117',
    'messagebox_color': '#c9d1d9',
    'messagebox_label_bg': 'transparent',
    'messagebox_label_color': '#f0f6fc',
    'messagebox_button_color': '#ffffff',
    'messagebox_button_bg': '#238636',
    'textedit_bg': '#0d1117',
    'textedit_color': '#c9d1d9',
    'textedit_selectbg': '#388bfd',
    'textedit_selectcolor': '#ffffff',
    'textedit_border': '#30363d',
    'checkbox_indicator_bg': 'transparent',
    'scrollbar_vrt_hrz_bg': '#161b22',
    'scrollbar_handle_bg': '#30363d',
    'scrollbar_pressed_bg': '#1f6feb',
    'scrollbar_corner_bg': '#0d1117',
    'menu_bg': '#0d1117',
    'menu_color': '#c9d1d9',
    'menu_border': '#30363d',
    'menu_item_bg': '#21262d',
    'menu_item_color': '#c9d1d9',
    'menu_item_border': '#30363d',
    'menu_item_selected_bg': '#1f6feb',
    'menu_item_selected_color': '#ffffff',
    'menu_item_selected_border': '#388bfd'},
  
'Violet Twilight' : {
    'mainwindow_bg' : 'transparent',
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#2c2738',
    'form_bg' : '#3a3349',
    'button_bg' : '#2a2240',
    'button_color' : '#dcd6f7',
    'button_border' : "#c1b4f8",
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg' : '#3a3152',
    'button_hover_color' : '#e6e1fa',
    'button_hover_border' : '#e6e1fa',
    'button_pressed_bg' : '#231a3b',
    'button_pressed_color' : '#e8e5fc',
    'button_pressed_border' : '#4c3f73',
    'combobox_bg' : '#3a3349',
    'combobox_color' : '#d4cef7',
    'combobox_border' : '#534a75',
    'combobox_hover_bg' : '#463f5b',
    'combobox_hover_color' : '#e3defa',
    'combobox_hover_border' : '#5f5390',
    'combobox_abstract_bg' : '#2b2440',
    'combobox_abstract_border' : '#453e6b',
    'combobox_abstractitem_bg' : '#3a3351',
    'combobox_abstractitem_color' : '#d6d0f8',
    'combobox_item_hover_color' : '#fff',
    'combobox_item_hover_bg' : '#534b7a',
    'messagebox_bg' : '#2f2a40',
    'messagebox_color' : '#d8d4fa',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#dcd8fb',
    'messagebox_button_color' : '#e7e4fc',
    'messagebox_button_bg' : '#3c3360',
    'textedit_bg' : '#352e4a',
    'textedit_color' : '#dad6fa',
    'textedit_selectbg' : '#534b7a',
    'textedit_selectcolor' : '#fff',
    'textedit_border' : "#aeabb6",
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#3a3349',
    'scrollbar_handle_bg' : '#534b7a',
    'scrollbar_pressed_bg' : '#453e6b',
    'scrollbar_corner_bg' : '#2f2a40',
    'menu_bg' : '#2e2942',
    'menu_color' : '#d4cef7',
    'menu_border' : '#443f6a',
    'menu_item_bg' : '#3a3349',
    'menu_item_color' : '#d6d0f8',
    'menu_item_border' : '#4c476a',
    'menu_item_selected_bg' : '#534b7a',
    'menu_item_selected_color' : '#fff',
    'menu_item_selected_border' : '#665d8e'},

'Sunset Isle':{
    'mainwindow_bg': 'transparent',
    'toolbar_bg': 'transparent',
    'i_widget_bg': '#1b0f1a',  
    'form_bg': '#2a1729',      
    'button_bg': '#4a2238',    
    'button_color': '#ffeedd', 
    'button_border': '#5e2c45',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg': '#5e2c45',
    'button_hover_color': '#fff8f0',
    'button_hover_border': '#86445f',
    'button_pressed_bg': '#cf3b57',  
    'button_pressed_color': '#ffffff',
    'button_pressed_border': '#e95a70',
    'combobox_bg': '#2a1729',
    'combobox_color': '#ffeedd',
    'combobox_border': '#5e2c45',
    'combobox_hover_bg': '#4a2238',
    'combobox_hover_color': '#ffffff',
    'combobox_hover_border': '#86445f',
    'combobox_abstract_bg': '#1b0f1a',
    'combobox_abstract_border': '#5e2c45',
    'combobox_abstractitem_bg': '#4a2238',
    'combobox_abstractitem_color': '#ffeedd',
    'combobox_item_hover_color': '#ffffff',
    'combobox_item_hover_bg': '#e26a2c',
    'messagebox_bg': '#1b0f1a',
    'messagebox_color': '#ffeedd',
    'messagebox_label_bg': 'transparent',
    'messagebox_label_color': '#fff5e6',
    'messagebox_button_color': '#ffffff',
    'messagebox_button_bg': '#e26a2c',
    'textedit_bg': '#1b0f1a',
    'textedit_color': '#ffeedd',
    'textedit_selectbg': '#cf3b57',
    'textedit_selectcolor': '#ffffff',
    'textedit_border': '#5e2c45',
    'checkbox_indicator_bg': 'transparent',
    'scrollbar_vrt_hrz_bg': '#2a1729',
    'scrollbar_handle_bg': '#5e2c45',
    'scrollbar_pressed_bg': '#cf3b57',
    'scrollbar_corner_bg': '#1b0f1a',
    'menu_bg': '#1b0f1a',
    'menu_color': '#ffeedd',
    'menu_border': '#5e2c45',
    'menu_item_bg': '#4a2238',
    'menu_item_color': '#ffeedd',
    'menu_item_border': '#5e2c45',
    'menu_item_selected_bg': '#cf3b57',
    'menu_item_selected_color': '#ffffff',
    'menu_item_selected_border': '#e95a70'},

'Deep Blue Night' : {
    'mainwindow_bg' : 'transparent',
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#0b0f1a',
    'form_bg' : '#101624',
    'button_bg' : '#1a2338',
    'button_color' : '#d0d8e8',
    'button_border' : '#2c354b',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg' : '#26324d',
    'button_hover_color' : '#e8f0ff',
    'button_hover_border' : '#3a4663',
    'button_pressed_bg' : '#1c4ed8',
    'button_pressed_color' : '#ffffff',
    'button_pressed_border' : '#2b61f3',
    'combobox_bg' : '#101624',
    'combobox_color' : '#d0d8e8',
    'combobox_border' : '#2c354b',
    'combobox_hover_bg' : '#1a2338',
    'combobox_hover_color' : '#ffffff',
    'combobox_hover_border' : '#3a4663',
    'combobox_abstract_bg' : '#0b0f1a',
    'combobox_abstract_border' : '#1e273a',
    'combobox_abstractitem_bg' : '#182235',
    'combobox_abstractitem_color' : '#c5cfe0',
    'combobox_item_hover_color' : '#ffffff',
    'combobox_item_hover_bg' : '#32518c',
    'messagebox_bg' : '#0e1420',
    'messagebox_color' : '#dce3ef',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#f1f6ff',
    'messagebox_button_color' : '#ffffff',
    'messagebox_button_bg' : '#2f4a7d',
    'textedit_bg' : '#0a0f19',
    'textedit_color' : '#d0d8e8',
    'textedit_selectbg' : '#3f5ba4',
    'textedit_selectcolor' : '#ffffff',
    'textedit_border' : '#2c354b',
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#101624',
    'scrollbar_handle_bg' : '#2c3c5b',
    'scrollbar_pressed_bg' : '#1f4bcc',
    'scrollbar_corner_bg' : '#0e1420',
    'menu_bg' : '#0b0f1a',
    'menu_color' : '#d0d8e8',
    'menu_border' : '#2e384d',
    'menu_item_bg' : '#1a2338',
    'menu_item_color' : '#d0d8e8',
    'menu_item_border' : '#2c354b',
    'menu_item_selected_bg' : '#2f4a7d',
    'menu_item_selected_color' : '#ffffff',
    'menu_item_selected_border' : '#3f5ba4'},

'Verdant Grove' : {
    'mainwindow_bg' : 'transparent',
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#0d1a13',
    'form_bg' : '#12261b',
    'button_bg' : '#1a3528',
    'button_color' : '#d8ede0',
    'button_border' : '#274b38',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg' : '#234a35',
    'button_hover_color' : '#e8fff3',
    'button_hover_border' : '#32634a',
    'button_pressed_bg' : '#1f613f',
    'button_pressed_color' : '#ffffff',
    'button_pressed_border' : '#2c8057',
    'combobox_bg' : '#12261b',
    'combobox_color' : '#d8ede0',
    'combobox_border' : '#274b38',
    'combobox_hover_bg' : '#1a3528',
    'combobox_hover_color' : '#ffffff',
    'combobox_hover_border' : '#32634a',
    'combobox_abstract_bg' : '#0d1a13',
    'combobox_abstract_border' : '#1e3b2c',
    'combobox_abstractitem_bg' : '#193426',
    'combobox_abstractitem_color' : '#c5e2d1',
    'combobox_item_hover_color' : '#ffffff',
    'combobox_item_hover_bg' : '#3b7e5c',
    'messagebox_bg' : '#101f17',
    'messagebox_color' : '#dbf0e2',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#f1fff8',
    'messagebox_button_color' : '#ffffff',
    'messagebox_button_bg' : '#2e5e45',
    'textedit_bg' : '#0b1811',
    'textedit_color' : '#d8ede0',
    'textedit_selectbg' : '#3a8f67',
    'textedit_selectcolor' : '#ffffff',
    'textedit_border' : '#274b38',
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#12261b',
    'scrollbar_handle_bg' : '#2b4c3a',
    'scrollbar_pressed_bg' : '#207f55',
    'scrollbar_corner_bg' : '#101f17',
    'menu_bg' : '#0d1a13',
    'menu_color' : '#d8ede0',
    'menu_border' : '#274b38',
    'menu_item_bg' : '#1a3528',
    'menu_item_color' : '#d8ede0',
    'menu_item_border' : '#274b38',
    'menu_item_selected_bg' : '#2e5e45',
    'menu_item_selected_color' : '#ffffff',
    'menu_item_selected_border' : '#3a8f67'},

'Cloudlight Bloom' : {
    'mainwindow_bg' : 'transparent',
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#ffffff',
    'form_bg' : '#f0f0f3',
    'button_bg' : '#2d3e50',
    'button_color' : '#f5f7f9',
    'button_border' : '#3a4f66',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg' : '#435d77',
    'button_hover_color' : '#ffffff',
    'button_hover_border' : '#57738e',
    'button_pressed_bg' : '#1f2e3d',
    'button_pressed_color' : '#ffffff',
    'button_pressed_border' : '#3a4f66',
    'combobox_bg' : '#ffffff',
    'combobox_color' : '#2d3e50',
    'combobox_border' : '#c0c4c8',
    'combobox_hover_bg' : '#f0f0f3',
    'combobox_hover_color' : '#2d3e50',
    'combobox_hover_border' : '#b3b8be',
    'combobox_abstract_bg' : '#f4f4f7',
    'combobox_abstract_border' : "#28446e",
    'combobox_abstractitem_bg' : '#2d3e50',
    'combobox_abstractitem_color' : '#ffffff',
    'combobox_item_hover_color' : "#f4f6f8",
    'combobox_item_hover_bg' : '#4d6c89',
    'messagebox_bg' : '#ffffff',
    'messagebox_color' : '#2d3e50',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#2d3e50',
    'messagebox_button_color' : '#ffffff',
    'messagebox_button_bg' : '#3c5973',
    'textedit_bg' : '#ffffff',
    'textedit_color' : '#2d3e50',
    'textedit_selectbg' : '#4d6c89',
    'textedit_selectcolor' : '#ffffff',
    'textedit_border' : '#c0c4c8',
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#e8eaed',
    'scrollbar_handle_bg' : '#c1c7cf',
    'scrollbar_pressed_bg' : '#aeb6c1',
    'scrollbar_corner_bg' : '#f0f0f3',
    'menu_bg' : '#ffffff',
    'menu_color' : '#2d3e50',
    'menu_border' : '#d1d4da',
    'menu_item_bg' : '#f0f0f3',
    'menu_item_color' : '#2d3e50',
    'menu_item_border' : '#c7cbd0',
    'menu_item_selected_bg' : '#3c5973',
    'menu_item_selected_color' : '#ffffff',
    'menu_item_selected_border' : '#4d6c89'},

'Snowy Pine':{
    'mainwindow_bg': 'transparent',
    'toolbar_bg': 'transparent',
    'i_widget_bg': '#e6f0f2',
    'form_bg': '#d0e1e7',
    'button_bg': '#4b5d55',    
    'button_color': '#ffffff', 
    'button_border': '#3c4d46',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg': '#5d7268',
    'button_hover_color': '#ffffff',
    'button_hover_border': '#4a5f56',
    'button_pressed_bg': '#223730',
    'button_pressed_color': '#ffffff',
    'button_pressed_border': '#304d43',
    'combobox_bg': '#4b5d55',         
    'combobox_color': '#ffffff',
    'combobox_border': '#3c4d46',
    'combobox_hover_bg': '#5d7268',
    'combobox_hover_color': '#ffffff',
    'combobox_hover_border': '#4a5f56',
    'combobox_abstract_bg': '#e6f0f2',  
    'combobox_abstract_border': '#91b3a1',
    'combobox_abstractitem_bg': '#a9c5b5',
    'combobox_abstractitem_color': '#1c2b27',
    'combobox_item_hover_color': '#ffffff',
    'combobox_item_hover_bg': '#49796b',
    'messagebox_bg': '#e6f0f2',
    'messagebox_color': '#1c2b27',
    'messagebox_label_bg': 'transparent',
    'messagebox_label_color': '#0e1f1c',
    'messagebox_button_color': '#ffffff',
    'messagebox_button_bg': '#49796b',
    'textedit_bg': '#e6f0f2',
    'textedit_color': '#1c2b27',
    'textedit_selectbg': '#49796b',
    'textedit_selectcolor': '#ffffff',
    'textedit_border': '#91b3a1',
    'checkbox_indicator_bg': 'transparent',
    'scrollbar_vrt_hrz_bg': '#d0e1e7',
    'scrollbar_handle_bg': '#a9c5b5',
    'scrollbar_pressed_bg': '#49796b',
    'scrollbar_corner_bg': '#e6f0f2',
    'menu_bg': '#e6f0f2',
    'menu_color': '#1c2b27',
    'menu_border': '#91b3a1',
    'menu_item_bg': '#a9c5b5',
    'menu_item_color': '#1c2b27',
    'menu_item_border': '#91b3a1',
    'menu_item_selected_bg': '#49796b',
    'menu_item_selected_color': '#ffffff',
    'menu_item_selected_border': '#5e9c88'},

'Peach Cream' : {
    'mainwindow_bg' : 'transparent',
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#fdf5f0',
    'form_bg' : '#fae3d5',
    'button_bg' : "#351104",
    'button_color' : '#fef9f5',
    'button_border' : '#8b3a1d',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg' : '#8c3a1d',
    'button_hover_color' : '#ffffff',
    'button_hover_border' : '#ae5028',
    'button_pressed_bg' : '#58240f',
    'button_pressed_color' : '#ffffff',
    'button_pressed_border' : '#76301a',
    'combobox_bg' : '#fdf5f0',
    'combobox_color' : '#5d2810',
    'combobox_border' : '#cbb1a3',
    'combobox_hover_bg' : '#f0d3c3',
    'combobox_hover_color' : '#5d2810',
    'combobox_hover_border' : '#b99f90',
    'combobox_abstract_bg' : '#eed6cb',
    'combobox_abstract_border' : '#cdb6a9',
    'combobox_abstractitem_bg' : '#d8a98a',
    'combobox_abstractitem_color' : '#331308',
    'combobox_item_hover_color' : '#ffffff',
    'combobox_item_hover_bg' : '#893f21',
    'messagebox_bg' : '#fff4eb',
    'messagebox_color' : '#5d2810',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#5d2810',
    'messagebox_button_color' : '#ffffff',
    'messagebox_button_bg' : '#6b2f14',
    'textedit_bg' : '#ffffff',
    'textedit_color' : '#5d2810',
    'textedit_selectbg' : '#ddb29a',
    'textedit_selectcolor' : '#2f1409',
    'textedit_border' : '#c4a293',
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#f9e8dd',
    'scrollbar_handle_bg' : '#ae5028',
    'scrollbar_pressed_bg' : '#8b3a1d',
    'scrollbar_corner_bg' : '#fae3d5',
    'menu_bg' : '#fdf5f0',
    'menu_color' : '#5d2810',
    'menu_border' : '#cbb1a3',
    'menu_item_bg' : '#f0d3c3',
    'menu_item_color' : '#5d2810',
    'menu_item_border' : '#c4a293',
    'menu_item_selected_bg' : '#893f21',
    'menu_item_selected_color' : '#ffffff',
    'menu_item_selected_border' : '#ae5028'},

'Frosted Mint' : {
    'mainwindow_bg' : 'transparent',
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#eef9f5',
    'form_bg' : '#d7f0ea',
    'button_bg' : '#2a4b45',
    'button_color' : '#f1fffb',
    'button_border' : '#3b5e58',
    'button_checked_bg' : '#1e3c37',
    'button_checked_color' : '#ffffff',
    'button_checked_border' : '#4d7e75',
    'button_hover_bg' : '#35675f',
    'button_hover_color' : '#ffffff',
    'button_hover_border' : '#599e93',
    'button_pressed_bg' : '#1a3530',
    'button_pressed_color' : '#ffffff',
    'button_pressed_border' : '#40776d',
    'combobox_bg' : '#eef9f5',
    'combobox_color' : '#1f3733',
    'combobox_border' : '#a0ccc2',
    'combobox_hover_bg' : '#d1ede6',
    'combobox_hover_color' : '#1f3733',
    'combobox_hover_border' : '#7fbfb2',
    'combobox_abstract_bg' : '#d9f2eb',
    'combobox_abstract_border' : '#aed6cc',
    'combobox_abstractitem_bg' : '#a0ccc2',
    'combobox_abstractitem_color' : '#10211d',
    'combobox_item_hover_color' : '#ffffff',
    'combobox_item_hover_bg' : '#3c6058',
    'messagebox_bg' : '#f2fbf7',
    'messagebox_color' : '#1f3733',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#1f3733',
    'messagebox_button_color' : '#ffffff',
    'messagebox_button_bg' : '#2a4b45',
    'textedit_bg' : '#ffffff',
    'textedit_color' : '#1f3733',
    'textedit_selectbg' : '#b2e0d6',
    'textedit_selectcolor' : '#14302a',
    'textedit_border' : '#9fc9bf',
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#e3f5f1',
    'scrollbar_handle_bg' : '#3c6058',
    'scrollbar_pressed_bg' : '#2a4b45',
    'scrollbar_corner_bg' : '#d7f0ea',
    'menu_bg' : '#eef9f5',
    'menu_color' : '#1f3733',
    'menu_border' : '#a0ccc2',
    'menu_item_bg' : '#d1ede6',
    'menu_item_color' : '#1f3733',
    'menu_item_border' : '#9fc9bf',
    'menu_item_selected_bg' : '#3c6058',
    'menu_item_selected_color' : '#ffffff',
    'menu_item_selected_border' : '#5aa49a'},

'Golden Dawn' : {
    'mainwindow_bg' : 'transparent',
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#fff9ed',
    'form_bg' : '#fff3d6',
    'button_bg' : '#1a1a1a',
    'button_color' : '#fcefa1',
    'button_border' : '#2c2c2c',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg' : '#2e2e2e',
    'button_hover_color' : '#fff9c4',
    'button_hover_border' : '#4a4a4a',
    'button_pressed_bg' : '#000000',
    'button_pressed_color' : '#fffeb7',
    'button_pressed_border' : '#5a5a5a',
    'combobox_bg' : '#fff9ed',
    'combobox_color' : '#5a4c00',
    'combobox_border' : '#f3e4a9',
    'combobox_hover_bg' : '#fff4cc',
    'combobox_hover_color' : '#6b5a00',
    'combobox_hover_border' : '#f7e99c',
    'combobox_abstract_bg' : '#fff1b8',
    'combobox_abstract_border' : '#6b5a00',
    'combobox_abstractitem_bg' : "#a19343",
    'combobox_abstractitem_color' : '#5c4b00',
    'combobox_item_hover_color' : '#ffffff',
    'combobox_item_hover_bg' : '#b58f00',
    'messagebox_bg' : '#fff8e1',
    'messagebox_color' : '#5c4b00',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#5c4b00',
    'messagebox_button_color' : '#ffffff',
    'messagebox_button_bg' : '#1a1a1a',
    'textedit_bg' : '#fffef0',
    'textedit_color' : '#5a4c00',
    'textedit_selectbg' : '#f7e99c',
    'textedit_selectcolor' : '#3f2e00',
    'textedit_border' : '#f0d96a',
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#fff8e1',
    'scrollbar_handle_bg' : '#b58f00',
    'scrollbar_pressed_bg' : '#a37d00',
    'scrollbar_corner_bg' : '#fff3d6',
    'menu_bg' : '#fff9ed',
    'menu_color' : '#5c4b00',
    'menu_border' : '#f3e4a9',
    'menu_item_bg' : '#fff4cc',
    'menu_item_color' : '#5c4b00',
    'menu_item_border' : '#f7e99c',
    'menu_item_selected_bg' : '#b58f00',
    'menu_item_selected_color' : '#ffffff',
    'menu_item_selected_border' : '#a37d00'}, 

'Soft Dawn' : {
    'mainwindow_bg' : 'transparent',
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#f9faf9',
    'form_bg' : '#f0f2f1',
    'button_bg' : '#1d1d1d',
    'button_color' : '#e6e6e6',
    'button_border' : '#333333',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg' : '#2e2e2e',
    'button_hover_color' : '#fafafa',
    'button_hover_border' : '#555555',
    'button_pressed_bg' : '#111111',
    'button_pressed_color' : '#f5f5f5',
    'button_pressed_border' : '#666666',
    'combobox_bg' : '#f9faf9',
    'combobox_color' : '#3a3a3a',
    'combobox_border' : '#d3d3d3',
    'combobox_hover_bg' : '#f0f1f0',
    'combobox_hover_color' : '#4d4d4d',
    'combobox_hover_border' : '#bdbdbd',
    'combobox_abstract_bg' : '#e6e7e6',
    'combobox_abstract_border' : '#c2c3c2',
    'combobox_abstractitem_bg' : '#c2c3c2',
    'combobox_abstractitem_color' : '#3c3c3c',
    'combobox_item_hover_color' : '#ffffff',
    'combobox_item_hover_bg' : '#555555',
    'messagebox_bg' : '#f2f4f3',
    'messagebox_color' : '#3b3b3b',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#3b3b3b',
    'messagebox_button_color' : '#ffffff',
    'messagebox_button_bg' : '#1d1d1d',
    'textedit_bg' : '#fafbfa',
    'textedit_color' : '#3a3a3a',
    'textedit_selectbg' : '#c1c2c1',
    'textedit_selectcolor' : '#1a1a1a',
    'textedit_border' : '#dcdede',
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#f0f1f0',
    'scrollbar_handle_bg' : '#595959',
    'scrollbar_pressed_bg' : '#444444',
    'scrollbar_corner_bg' : '#f0f2f1',
    'menu_bg' : '#f9faf9',
    'menu_color' : '#3a3a3a',
    'menu_border' : '#d3d3d3',
    'menu_item_bg' : '#f0f1f0',
    'menu_item_color' : '#3a3a3a',
    'menu_item_border' : '#bfbfbf',
    'menu_item_selected_bg' : '#595959',
    'menu_item_selected_color' : '#ffffff',
    'menu_item_selected_border' : '#444444'},

'Violet Dawn' : {
    'mainwindow_bg' : 'transparent',
    'toolbar_bg' : 'transparent',
    'i_widget_bg' : '#e6e4f3',
    'form_bg' : '#dedbf1',
    'button_bg' : '#322a4f',
    'button_color' : '#e8e5fc',
    'button_border' : '#5a4b8a',
    'button_checked_bg' : "#234414",
    'button_checked_color' : '#f5f4f2',
    'button_checked_border' : "#7a9980",
    'button_hover_bg' : '#665d8e',
    'button_hover_color' : '#f4f2ff',
    'button_hover_border' : '#7a74a7',
    'button_pressed_bg' : '#3a3152',
    'button_pressed_color' : '#dcd6f7',
    'button_pressed_border' : '#4c476a',
    'combobox_bg' : '#463f5b',
    'combobox_color' : '#e3defa',
    'combobox_border' : '#5f5390',
    'combobox_hover_bg' : '#534b7a',
    'combobox_hover_color' : '#edeaff',
    'combobox_hover_border' : '#665d8e',
    'combobox_abstract_bg' : '#4c476a',
    'combobox_abstract_border' : '#f0eeff',
    'combobox_abstractitem_bg' : '#665d8e',
    'combobox_abstractitem_color' : '#f0eeff',
    'combobox_item_hover_color' : '#ffffff',
    'combobox_item_hover_bg' : '#7a74a7',
    'messagebox_bg' : '#e2dff7',
    'messagebox_color' : '#4c3f73',
    'messagebox_label_bg' : 'transparent',
    'messagebox_label_color' : '#4c3f73',
    'messagebox_button_color' : '#dedbf1',
    'messagebox_button_bg' : '#5a4b8a',
    'textedit_bg' : '#e6e4f3',
    'textedit_color' : '#463f5b',
    'textedit_selectbg' : '#534b7a',
    'textedit_selectcolor' : '#fff',
    'textedit_border' : '#665d8e',
    'checkbox_indicator_bg' : 'transparent',
    'scrollbar_vrt_hrz_bg' : '#dedbf1',
    'scrollbar_handle_bg' : '#5a4b8a',
    'scrollbar_pressed_bg' : '#534b7a',
    'scrollbar_corner_bg' : '#e2dff7',
    'menu_bg' : '#e2dff7',
    'menu_color' : '#463f5b',
    'menu_border' : '#b8b3dc',
    'menu_item_bg' : '#dedbf1',
    'menu_item_color' : '#463f5b',
    'menu_item_border' : '#b8b3dc',
    'menu_item_selected_bg' : '#665d8e',
    'menu_item_selected_color' : '#ffffff',
    'menu_item_selected_border' : '#7a74a7'}
}







        




