
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
        self.screen_w, self.screen_h, self.screen_scale = ScreenSize()
        super(TranslateApp,self).__init__()
        #self.ui = Ui_MainWindow()
        #self.ui.setupUi(self)


        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)   
        self.setStyleSheet('''
                            QMainWindow {
                        margin: 0; padding: 0; border:none; 
                        }
                            QToolBar { 
                        background-color: rgb(0,0,0); margin: 0; padding: 0; border:none;
                        }  
                        /*    QToolButton {             #toolbutton ayarları ilerde lazım olursa diye yazdım ama şuan burda kullanmıycaz carsayılan ayarı fena değil.
                        text-align: center; padding: 0px; margin: 0px; border-radius: 0px; border-style: solid; 
                        color: rgb(201, 243, 201); background-color: initial; border-color: rgb(47, 172, 126);
                        } 
                            QToolButton:hover {
                        background-color:rgb(255, 254, 219);
                        }
                            QToolButton:pressed {
                        border-color: rgb(168, 186, 253); background-color:rgb(207, 230, 7); color:  rgb(201, 243, 201);
                        } */
                            QComboBox {
                        border: 2px solid rgb(14, 156, 31);
                        padding: 2px;
                        margin: 5px;
                        }
                            QComboBox::drop-down {
                        border: none;
                        width: 0px;
                        }
                            QComboBox::down-arrow {
                        image: none;
                        }
                           ''')    #normalde toolbarın üst kısmında bi çizgi vardı boydan boya beyaz. borderi none yaparak bundan kurtulduk.
        self.widgets_load()
        self.adjust_window_size()       #pencereyi sadece toolbara göre ayarlaması için ölçeklendirme.
        
        

    def open_button_clicked(self):
        pass
    def picture_button_clicked(self):
        pass
    def speech_button_clicked(self):
        pass
    def change_button_clicked(self):
        pass
    def trash_button_clicked(self):
        pass
    def pinned_button_clicked(self):
        pass       
    def replace_button_clicked(self):
        pass
    def move_button_clicked(self):
        pass
    def close_button_clicked(self):
        self.close()

    def widgets_load(self):
        self.toolbutton_size = QtCore.QSize(20*self.screen_scale, 20*self.screen_scale)
        self.combobox_size = QtCore.QSize(30*self.screen_scale, 20*self.screen_scale) 

        self.toolbar = QtWidgets.QToolBar('ToolBar', self)
        self.toolbar.setIconSize(self.toolbutton_size)
        self.toolbar.layout().setSpacing(0)     #bu ve alttaki satır hiç bir tarafından boşluk kalmaması için
        self.toolbar.layout().setContentsMargins(0,0,0,0)
        self.toolbar.setMovable(False)       #kullanıcı hareket ettiremesin diye
        self.toolbar.setFloatable(False)    #pencere dışına bırakıldığında otomatik pencereye dönmesi için.
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolbar)  #direk en üste eklemesi için. çünkü mainwindowu buna göre ayarlıyoruz.

        

        toolbutton_str = [
            ('open','Open', 'action'),
            ('picture','Picture','action'),
            ('speech','Speech','action'),
            ('src_combobox','Source','combobox'),
            ('change','Change','action'),
            ('dest_combobox','Target','combobox'),
            ('trash','Trash','action'),
            ('pinned','Pinned','action'),        #bunu basılı tutan şekilde ayarla
            ('replace','Replace','action'),
            ('move','Move','action'),
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
        self.toolbar_widget_dict['pinned']['widget'].setCheckable(True)   #bu  pinned butonunu basılı tutulabilen hale getiriyor.
        self.toolbar_widget_dict['src_combobox']['widget'].setToolTip('Source Language')    #q acitonda oluşturduğumuz ikinci parametreler zaten tooltip gibi göründüğü için onlara yapmaya gerek yok ama qcomboboxlarınki fareyle üzerine gelince görünmüyor. bu ikisinielle ayarladık.
        self.toolbar_widget_dict['dest_combobox']['widget'].setToolTip('Target Language')
        
        for key, value in self.toolbar_widget_dict.items():
            if value['widgettype'] == 'combobox':
                self.toolbar.addWidget(value['widget'])
            else:
                self.toolbar.addAction(value['widget'])
        #self.toolbar.addActions(self.toolbar_widget_dict.values())      #addactionsa butonların asıl hallerini değerler olarak kaydettiğimiz için buraya o şekilde giriyoruz.





       
        
        
        
    def adjust_window_size(self):
        toolbar_w = self.toolbar.sizeHint().width()
        toolbar_h = self.toolbar.sizeHint().height()  
        self.setFixedSize(toolbar_w, toolbar_h)
        
        
    def DENEMELER(self):        #YUKARIDA BUTONLARI DİNAMİK OLUŞTURDUĞUM İÇİN TAMAMLAMA ÇIKMIYOR. ÖZELLİKLERE BAKMAK İSTERSEN BURDA DENE.
        button = QtWidgets.QToolButton()
        combobox = QtWidgets.QComboBox()
    
    

    '''def move_button_pressed_event(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.initial_pos = event.pos()
        super(QtWidgets.QToolButton, self.ui.toolButton_move).mousePressEvent(event)
        event.accept()

    def move_button_move_event(self,event):
        self.setCursor(QtCore.Qt.BlankCursor)       #move tuşuna basılıyken farenin görünmez olmasını sağlıyor.
        if self.initial_pos is not None:
            delta = event.pos() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super(QtWidgets.QToolButton, self.ui.toolButton_move).mouseMoveEvent(event)
        event.accept()

    def move_button_release_event(self, event):
        self.unsetCursor()          #farenin tuşu bırakılınca cursor ayarını kaldırıp eski haline getiriyor.
        self.initial_pos = None 
        super(QtWidgets.QToolButton, self.ui.toolButton_move).mouseReleaseEvent(event)
        event.accept()'''


            
        
        
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
    


