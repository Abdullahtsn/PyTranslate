from PyQt5.QtWidgets import QToolButton, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class MoveClass:
    def __init__(self, widget, screen_w, screen_h):
        self.initial_pos = None
        self.widget = widget
        self.screen_w = screen_w
        self.screen_h = screen_h


    def move_button_mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.pos()
        #super(QToolButton, self.toolbar_widget_dict['move']['widget']).mousePressEvent(event)    #burda sınıfın kendi içinde olmadığımız için super mantıksız kalıyor olabilir o yüzden bu satır aşağıdaki şekilde güncellendi.
        if isinstance(self.widget, QPushButton):    #burda widget hangi sınıfa ait diye kontrol edip ona göre aşağıdaki kalıtımı yapıyoz. çünkü mainwidgette toolbutton move butonuyken, speech widgette pushbutton move butonu.
            QPushButton.mousePressEvent(self.widget, event)    #yukardaki satırı bu şekle dönüştürdük. supere gerek yok. direktoolbuttonun tıklamaısnı alıyoz.
                                                                                                    #Bu, 'widget’a ait olan Qt'nin orijinal mousePressEvent metodunu elle çağır' demek. kısaca ;
                                                                                                    #super(...).method()	Sadece bir sınıfın içinden, self o sınıfken mantıklı,
                                                                                                    #QToolButton.method(widget, event)	Eğer QToolButton nesnesinin içinden değilsen, bu şekilde çağırmak gerekiyor
        elif isinstance(self.widget, QToolButton):
            QToolButton.mousePressEvent(self.widget, event)
        elif isinstance(self.widget, QMessageBox):
            QMessageBox.mousePressEvent(self.widget, event)
        else:
            print('Tanımlanmayan Widget türü')
        event.accept()
        
    def move_button_mouse_move_event(self,event):
        self.widget.setCursor(Qt.BlankCursor)       #move tuşuna basılıyken farenin görünmez olmasını sağlıyor.
        if self.initial_pos is not None:
            delta = event.pos() - self.initial_pos
            self.widget.window().move(
                self.widget.window().x() + delta.x(),
                self.widget.window().y() + delta.y(),
            )
        #super(QToolButton, self.toolbar_widget_dict['move']['widget']).mouseMoveEvent(event)
        if isinstance(self.widget, QPushButton):
            QPushButton.mouseMoveEvent(self.widget, event)    
        elif isinstance(self.widget, QToolButton):
            QToolButton.mouseMoveEvent(self.widget, event)
        elif isinstance(self.widget, QMessageBox):
            QMessageBox.mouseMoveEvent(self.widget, event)
        else:
            print('Tanımlanmayan Widget türü')
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
        geometry = self.widget.window().geometry() #bu satırda windowu eklememiz demek gönderilen widgetin bağlı olduğu pencereeyi al demek.
        x, y, width, height = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if x < 0 :
            x = 0
        elif x + width > self.screen_w :
            x = self.screen_w - width
        if y < 0 :
            y = 0
        elif y + height > self.screen_h :
            y = self.screen_h - height
        self.widget.window().setGeometry(x, y, width, height)

        if event is not None:
            self.widget.unsetCursor()          #farenin tuşu bırakılınca cursor ayarını kaldırıp eski haline getiriyor.
            self.initial_pos = None 
            #super(QToolButton, self.toolbar_widget_dict['move']['widget']).mouseReleaseEvent(event)
            if isinstance(self.widget, QPushButton):
                QPushButton.mouseReleaseEvent(self.widget, event)    
            elif isinstance(self.widget, QToolButton):
                QToolButton.mouseReleaseEvent(self.widget, event)
            elif isinstance(self.widget, QMessageBox):
                QMessageBox.mouseReleaseEvent(self.widget, event)
            else:
                print('Tanımlanmayan Widget türü')
            event.accept()