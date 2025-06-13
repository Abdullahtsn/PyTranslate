# 💡 PyTranslate Nedir?

Yabancı forumlar, dokümanlar veya oyunlar gibi içeriklerde çeviri ihtiyacı sık yaşanıyor. Ancak mevcut çeviri çözümleri ya sürekli açık bir web sayfasına bağımlıydı, ya da bir görüntüden metin çevirmek için ekran görüntüsü al, siteye yükle, bekle gibi zaman kaybettiren adımlar içeriyordu. Bu hem odak kaybına neden oluyor hem de süreci gereksiz yere uzatıyordu.

Bu eksikliklerden yola çıkarak, **hızlı, pratik ve odağı bozmayan** bir çeviri aracı ihtiyacını fark ettim — ve **PyTranslate**'i geliştirdim.



## 🚀 Ne Yapar?

PyTranslate, ekranın herhangi bir köşesinde yer alabilen küçük bir araç çubuğu şeklinde çalışır.  

-🔹 **Metin tabanlı çeviri**  
-🔹 **Anlık ekran üzerindeki yazıyı tanıma ve çeviri (OCR destekli)**  
-🔹 **Minimum dikkat dağınıklığı, maksimum verimlilik**

Yani:  
**“İşimden kopmadan çeviri yapmamı sağlayan kişisel bir yardımcı.”**



## 🎯 Neden PyTranslate?

- ✅ Arka planda web sitesi açık tutma derdi yok.  
- ✅ Görselden çeviri için karmaşık adımlar yok.  
- ✅ Her şey hızlı, sade ve erişilebilir.  
- ✅ Çalışma akışını bölmeden yardımcı olur.

## 📄 Nasıl Çalışır?

- Uygulamanın ana penceresi bir **araç çubuğu** şeklindedir.  
- Kullanıcıya **metin çevirme** veya **resimdeki metni algılayıp çevirme** seçenekleri sunar.  
- Yazılım dili: **Python**  
- Arayüz: **PyQt5**  
- OCR (görüntüden metin algılama) öncesi resmi filtreleme işlemi için: **open-cv** kütüphanesi ,
- OCR (görüntüden metin algılama) işlemi için: **pytesseract** kütüphanesi ve onun dil modelleri ,
- Çeviri işlemleri için: **deep-translator** kütüphanesi ,
- Dil bilgisi düzeltme için: **language-tool-python** kütüphanesi ,
- Kelime düzeltme için: **pyspellchecker** kütüphanesi kullanılır  
- Projeyle ilgili tüm kütüphane ve bağımlılıklar `requirements.txt` dosyasında listelenmiştir.

## 📦 İndir

Tüm ortamlarda bağımsız çalışabilmesi için bağlantıdan kurulum dosyasını indirebilirsin:

📘 [PyTranslate – Son Güncelleme Notları](https://github.com/Abdullahtsn/PyTranslate/releases/latest)  

📥 [PyTranslate v1.0.2 – Kurulum Dosyasını İndir](https://github.com/Abdullahtsn/PyTranslate/releases/download/v1.0.2/PyTranslate_setup.exe)  


> ⚠️ **Not:** Kurulum dosyası (`setup.exe`), PyTranslate’in bağımsız olarak çalışabilmesi için hazırlanmıştır.  
> Yani Python ya da ek kütüphaneler sisteminde kurulu olmasa bile, bu kurulum dosyası sayesinde uygulamayı doğrudan çalıştırabilirsin.  
>
> Uygulama tamamen açık kaynak kodludur ve GitHub sayfasında tüm kodları şeffaf bir şekilde paylaşıyorum.  
>  
> İstersen kendin derleyebilir, hatta kendi sisteminde çalıştırarak güvenliğini bizzat test edebilirsin.

## 🔘 Butonlar ve İşlevleri

<p>
  <img src="icon/close.png" width="36" style="vertical-align: middle;"/>
  <strong>Çıkış ( ESC ) :</strong> Uygulamayı kapatır.
</p>

<p>
  <img src="icon/maximize.png" width="36" style="vertical-align: middle;"/>
  <strong>Tam ekran:</strong> Pencereyi tam ekran yapar.
</p>

<p>
  <img src="icon/minimize.png" width="36" style="vertical-align: middle;"/>
  <strong>Küçült:</strong> Görev çubuğuna küçültür.
</p>

<p>
  <img src="icon/move.png" width="36" style="vertical-align: middle;"/>
  <strong>Taşı:</strong> Pencereyi sürükleyerek taşımanı sağlar.
</p>

<p>
  <img src="icon/info.png" width="36" style="vertical-align: middle;"/>
  <strong>İpuçları:</strong> Butonların açıklamalarını gösterir.
</p>

---

<p>
  <img src="icon/text.png" width="36" style="vertical-align: middle;"/>
  <strong>Metin Çevirisi  ( Alt + 1 ) :</strong> Metin Çeviri penceresini açar.
</p>

<p>
  <img src="icon/image_text.png" width="36" style="vertical-align: middle;"/>
  <strong>Ekran Çevirisi ( Alt + 2 ) :</strong> Ekrandan seçilen bölgedeki metinleri algılar, metin çevirisine gönderir. (Açılan pencerede ki ekranın üst orta bölgesinde bulunan dil seçimine göre algılama yapar.)
</p>

<p>
  <img src="icon/transparent.png" width="36" style="vertical-align: middle;"/>
  <strong>Saydamlaştır:</strong> Uygulamayı kısmen arka planı görünecek şekilde ayarlar.
</p>

<p>
  <img src="icon/pinned.png" width="36" style="vertical-align: middle;"/>
  <strong>Sabitle:</strong> Uygulamayı her zaman en üstte tutar.
</p>

<p>
  <img src="icon/rotation.png" width="36" style="vertical-align: middle;"/>
  <strong>Döndür:</strong> Uygulama yatay ve dikey kullanımlar arasında geçiş yapar.
</p>

<p>
  <img src="icon/thema.png" width="36" style="vertical-align: middle;"/>
  <strong>Tema:</strong> Koyu ve açık renk paletleriyle uygulama tasarımını değiştirir.
</p>

<p>
  <img src="icon/expand.png" width="36" style="vertical-align: middle;"/>
  <strong>Küçült:</strong> Fazlalık butonları gizleyerek uygulamanın kapladığı alanı küçültür.
</p>

---

<p>
  <img src="icon/lang_change.png" width="36" style="vertical-align: middle;"/>
  <strong>Dil Değişimi:</strong> Çevrilecek ve çevrilen dil seçiminin yerlerini değiştirir.
</p>

<p>
  <img src="icon/text_change.png" width="36" style="vertical-align: middle;"/>
  <strong>Metin Değişimi:</strong> Çevrilecek ve çevrilen metinlerinin yerlerini değiştirir.
</p>

<p>
  <img src="icon/correct_grammar.png" width="36" style="vertical-align: middle;"/>
  <strong>Dil Bilgisine Göre Düzelt ( F1 ) :</strong> Çevrilecek metindeki yanlışları o dilin kurallarına göre düzeltir.(Türkçe dil desteği yok.)
</p>

<p>
  <img src="icon/correct_word.png" width="36" style="vertical-align: middle;"/>
  <strong>Kelimeleri Düzelt ( F2 ) :</strong> Çevrilecek metindeki kelimeleri düzeltir.  (Desteklenen diller : English, Spanish, French, Italian, Portuguese, German, Russian, Arabic, Dutch, Persian.)
</p>

<p>
  <img src="icon/variant.png" width="36" style="vertical-align: middle;"/>
  <strong>Dil Varyantlarını:</strong> Dil seçimi için o dilin farklı bölgelerdeki varyantlarını dahil eder. (Kullanıcının dikkatini dağıttığı için gizlendi. Kodlardan aktif edilebilir.)
</p>

<p>
  <img src="icon/translation.png" width="36" style="vertical-align: middle;"/>
  <strong>Çevir (ENTER) :</strong> Çeviri yapar.
</p>

<p>
  <img src="icon/copy.png" width="36" style="vertical-align: middle;"/>
  <strong>Kopyala:</strong> Bağlı olduğu yerde ki metni kopyalar.
</p>

<p>
  <img src="icon/paste.png" width="36" style="vertical-align: middle;"/>
  <strong>Yapıştır:</strong> Bağlı olduğu yere kopyalanan metni yapıştırır.
</p>

<p>
  <img src="icon/clear.png" width="36" style="vertical-align: middle;"/>
  <strong>Temizle:</strong> Bağlı olduğu yerdeki metni siler.
</p>



## 🎨 Tema Galerisi - Theme Gallery
<p style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
    <img src="app_image/thema.png" style="width: 40%; border-radius: 8px;" />
    <img src="app_image/thema2.png" style="width: 40%; border-radius: 8px;" />
    <img src="app_image/vertical_minimalist.png" style="height: 322; border-radius: 8px" />
    <img src="app_image/vertical_maximalist.png" style="height: 322; border-radius: 8px" />
    <img src="app_image/1.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/2.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/3.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/4.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/5.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/6.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/7.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/8.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/9.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/10.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/11.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/12.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/13.png" style="width: 48%; border-radius: 8px;" />
</p>

--------------------------------------------

<span style="font-size: 36px;">English Guide</span>

# 💡 What is PyTranslate?

The need for translation often arises in foreign forums, documents, or games. However, existing translation solutions either depend on constantly having a web page open or involve time-consuming steps like taking a screenshot, uploading it to a site, and waiting to translate text from an image. This causes loss of focus and unnecessarily prolongs the process.

Based on these shortcomings, I realized the need for a **fast, practical, and non-distracting** translation tool — and developed **PyTranslate**.

## 🚀 What Does It Do?

PyTranslate works as a small toolbar that can be placed in any corner of the screen.

- 🔹 **Text-based translation**  
- 🔹 **Instant recognition and translation of text on the screen (OCR supported)**  
- 🔹 **Minimal distraction, maximum efficiency**

In other words:  
**“A personal assistant that lets me translate without breaking my workflow.”**

## 🎯 Why PyTranslate?

- ✅ No need to keep a website open in the background.  
- ✅ No complicated steps for image translation.  
- ✅ Everything is fast, simple, and accessible.  
- ✅ Helps without interrupting your workflow.

## 📄 How It Works

- The application's main window is in the form of a **toolbar**.  
- It offers users options to **translate text** or **detect and translate text from an image**.  
- Programming language: **Python**  
- Interface: **PyQt5**  
- For filtering the image before OCR (Optical Character Recognition): the **open-cv** library,  
- For OCR (detecting text from images): the **pytesseract** library and its language models,  
- For translation operations: the **deep-translator** library,  
- For grammar correction: the **language-tool-python** library,  
- For spell correction: the **pyspellchecker** library is used.  
- All project-related libraries and dependencies are listed in the `requirements.txt` file.


## 📦 Download

You can download the setup file from the link below to run independently on any system:

📘 [PyTranslate – Release Notes](https://github.com/Abdullahtsn/PyTranslate/releases/latest)  

📥 [PyTranslate v1.0.2 – Download Installer](https://github.com/Abdullahtsn/PyTranslate/releases/download/v1.0.2/PyTranslate_setup.exe)  


> ⚠️ **Note:** The setup file (`setup.exe`) is prepared so that PyTranslate can run independently.  
> That means even if Python or additional libraries are not installed on your system, you can run the application directly with this setup file.  
>  
> The application is fully open source and all the code is transparently shared on the GitHub page.  
>  
> You can compile it yourself or test its security by running it on your own system.

## 🔘 Buttons and Their Functions

<p>
  <img src="icon/close.png" width="36" style="vertical-align: middle;"/>
  <strong>Close ( ESC ):</strong> Closes the application.
</p>

<p>
  <img src="icon/maximize.png" width="36" style="vertical-align: middle;"/>
  <strong>Fullscreen:</strong> Makes the window fullscreen.
</p>

<p>
  <img src="icon/minimize.png" width="36" style="vertical-align: middle;"/>
  <strong>Minimize:</strong> Minimizes the window to the taskbar.
</p>

<p>
  <img src="icon/move.png" width="36" style="vertical-align: middle;"/>
  <strong>Move:</strong> Allows you to drag and move the window.
</p>

<p>
  <img src="icon/info.png" width="36" style="vertical-align: middle;"/>
  <strong>Tips:</strong> Shows descriptions of the buttons.
</p>

---
<p>
  <img src="icon/text.png" width="36" style="vertical-align: middle;"/>
  <strong>Text Translation ( Alt + 1 ) :</strong> Opens the Text Translation window.
</p>

<p>
  <img src="icon/image_text.png" width="36" style="vertical-align: middle;"/>
  <strong>Screen Translation ( Alt + 2 ) :</strong> Detects the text in the selected area on the screen and sends it to Text Translation. (Detection is based on the language selection located at the top center of the opened window.)
</p>

<p>
  <img src="icon/transparent.png" width="36" style="vertical-align: middle;"/>
  <strong>Make Transparent:</strong> Sets the app to be semi-transparent, allowing the background to show through.
</p>

<p>
  <img src="icon/pinned.png" width="36" style="vertical-align: middle;"/>
  <strong>Pin:</strong> Keeps the application always on top.
</p>

<p>
  <img src="icon/rotation.png" width="36" style="vertical-align: middle;"/>
  <strong>Rotate:</strong> Switches between horizontal and vertical layouts of the application.
</p>

<p>
  <img src="icon/thema.png" width="36" style="vertical-align: middle;"/>
  <strong>Theme:</strong> Switches the application design between light and dark color palettes.
</p>

<p>
  <img src="icon/expand.png" width="36" style="vertical-align: middle;"/>
  <strong>Minimize:</strong> Hides extra buttons to reduce the space the application occupies.
</p>

---

<p>
  <img src="icon/lang_change.png" width="36" style="vertical-align: middle;"/>
  <strong>Swap Languages:</strong> Switches the positions of the source and target language selections.
</p>

<p>
  <img src="icon/text_change.png" width="36" style="vertical-align: middle;"/>
  <strong>Swap Texts:</strong> Switches the source and translated texts.
</p>

<p>
  <img src="icon/correct_grammar.png" width="36" style="vertical-align: middle;"/>
  <strong>Correct Grammar ( F1 ):</strong> Fixes errors in the source text according to grammar rules of that language. (Turkish is not supported.)
</p>

<p>
  <img src="icon/correct_word.png" width="36" style="vertical-align: middle;"/>
  <strong>Correct Words ( F2 ) :</strong> Corrects spelling mistakes in the source text. (Supported languages: English, Spanish, French, Italian, Portuguese, German, Russian, Arabic, Dutch, Persian.)
</p>

<p>
  <img src="icon/variant.png" width="36" style="vertical-align: middle;"/>
  <strong>Language Variants:</strong> Includes regional variants for language selection. (Hidden by default to reduce distraction. Can be enabled from the code.)
</p>

<p>
  <img src="icon/translation.png" width="36" style="vertical-align: middle;"/>
  <strong>Translate:</strong> Executes the translation. (Can also be triggered with the ENTER key.)
</p>

<p>
  <img src="icon/copy.png" width="36" style="vertical-align: middle;"/>
  <strong>Copy:</strong> Copies the text in the associated field.
</p>

<p>
  <img src="icon/paste.png" width="36" style="vertical-align: middle;"/>
  <strong>Paste:</strong> Pastes the copied text into the associated field.
</p>

<p>
  <img src="icon/clear.png" width="36" style="vertical-align: middle;"/>
  <strong>Clear:</strong> Deletes the text in the associated field.
</p>
