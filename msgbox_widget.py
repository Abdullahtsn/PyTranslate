import os

from PyQt5.QtWidgets import QMessageBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, Qt, QSize

from move_class import MoveClass



class MsgBox(QMessageBox):
    def __init__(self, screen_w, screen_h, screen_scale):
        super().__init__()
        self.screen_w, self.screen_h, self.screen_scale = screen_w, screen_h, screen_scale
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.style_sheet_string = f'''
                    QMessageBox {{
                background-color: rgb(50, 50, 50); 
                color: rgb(210, 210, 210);         
                padding: 0px;
                margin: 0px;   
                }}
                    QLabel {{
                font: bold {8*self.screen_scale}px;
                background-color: transparent; 
                color: rgb(220, 220, 220);
                padding: 0px;
                margin:0px;
                }}
                    QPushButton {{          /*buton için varsayılan ayarları kullandık sadece yazıyla oynadık, eğer özelleştirmek istersen aşağıdaki düzenle*/
                font: bold {8*self.screen_scale}px;
                }}
                    /*QPushButton {{
                background-color: rgb(30, 30, 30);          
                color: rgb(220, 220, 220); 
                border: {2*self.screen_scale}px solid rgb(100, 100, 100);
                border-radius: {6*self.screen_scale}px;
                padding: 0px;
                margin: 0px;
                font: bold {8*self.screen_scale}px;
                }}
                    QPushButton::hover {{
                background-color: rgb(220, 220, 220);
                color: rgb(30, 30, 30);
                }}*/
                                '''
        self.setStyleSheet(self.style_sheet_string)
        
        self.info_icon = QPixmap(os.path.join('icon','info_msg.png')).scaled(40*self.screen_scale, 40*self.screen_scale, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)    #keepaspectratio = oranı koruması için, smoothtransformation = daha yumuşak kaliteyle ölçmesi için

        self.setWindowTitle('Message To User')
        self.setWindowIcon(QIcon(self.info_icon))     
        self.setStandardButtons(self.StandardButton.Ok)    # bunu dışardan parametre olarak birden fazla duruma göre buton ekleyebiliriz ama bu uygulama için her koşulda sadece ok butonu olcağı için gerek görülmedi.
        #self.button(self.Ok).setStyleSheet('padding-right:90px')   #messageboxun içindeki ok botununu ortalama. grid layout şeklinde yerleştirildiği için padding ile sağdan boşluk bırakarak ortalamış gibi gösterebiliyoruz.
        self.setIconPixmap(self.info_icon)
        self.button_ok = self.button(self.StandardButton.Ok)
        self.button_ok.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_ok.setIcon(QIcon(os.path.join('icon','ok_msg.png')))
        self.button_ok.setIconSize(QSize(16*self.screen_scale, 16*self.screen_scale))
        self.setContentsMargins(0, 0, 12*self.screen_scale, 0)
        self.move_button_click()
        
    def edit(self, text):     #her mesaj kutusunu ayrı ayrı oluşturmak yerine bir mesaj kutusunu dışardan gelcek verilerle güncelleyip bellek kullanımını azaltıcaz.
        self.setText(text)
        self.exec_()    # Qt6 da  .exec() olmuş.
        if self.clickedButton() == self.button_ok:
            self.close()
        

        '''for i in self.children():        #qmessageboxun içindeki widgetleri listeleme
            print(i)'''

    def move_button_click(self):    #burası init kısmında sadece bir defa çalıştırılcak şekilde ayarlandı. movebutonu için olan mouse eventlerini override ettiğimiz yer. tüm move işlemleri için moveclası hazırladık , değişkenleri oraya gönderiyoruz ve her  pencere widgeti için tek tek eklemek zorunda kalmıyoruz.
        self.move_class = MoveClass(self, self.screen_w, self.screen_h)     #burda pencereyi taşımak için buton değil messagbox widgetinin kendisi kullanıldı.
        self.mousePressEvent = self.move_class.move_button_mouse_press_event
        self.mouseMoveEvent = self.move_class.move_button_mouse_move_event
        self.mouseReleaseEvent = self.move_class.move_button_mouse_release_event
    
    def closeEvent(self, event):    #bu widget için ana widget kapatılırken bunuda kapatma sinyali yapmadık çünkü ;
                                    #bunu exec ile gösterdiğimiz için modal oluyor ve bu diğer gui üyelerini kilitliyor sadece bu widgete odaklanılmasını sağlıyor. yani özet;
                                    #widgeti show = non-modal, exec = modal göstermek anlamlarına geliyor.showla gösterilende özel kapatma işlemi yapabiliriz o diğer guiyi ve widgetleri kitlemiyor.
        print('Messagebox widgeti kapatıldı')
        super().closeEvent(event)