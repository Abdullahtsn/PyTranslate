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

- ✅ Arka planda web sitesi açık tutma derdi yok  
- ✅ Görselden çeviri için karmaşık adımlar yok  
- ✅ Her şey hızlı, sade ve erişilebilir  
- ✅ Çalışma akışını bölmeden yardımcı olur

## 📄 Nasıl Çalışır?

- Uygulamanın ana penceresi bir **araç çubuğu** şeklindedir.  
- Kullanıcıya **metin çevirme** veya **resimdeki metni algılayıp çevirme** seçenekleri sunar.  
- Yazılım dili: **Python**  
- Arayüz: **PyQt5**  
- OCR (görüntüden metin algılama) işlemi için: **pytesseract** ve onun dil modelleri  
- Çeviri işlemleri için: **deep-translator** kütüphanesi  
- Kelime düzeltme için: **language-tool-python** kullanılır  
- Projeyle ilgili tüm kütüphane ve bağımlılıklar `requirements.txt` dosyasında listelenmiştir.

## 📦 İndir

Tüm ortamlarda bağımsız çalışabilmesi için bağlantıdan kurulum dosyasını indirebilirsin:

📥 [PyTranslate Kurulum Dosyasını İndir](https://github.com/Abdullahtsn/PyTranslate/releases/tag/v1.0.0)

> ⚠️ **Not:** Kurulum dosyası (`setup.exe`), PyTranslate’in bağımsız olarak çalışabilmesi için hazırlanmıştır.  
> Yani Python ya da ek kütüphaneler sisteminde kurulu olmasa bile, bu kurulum dosyası sayesinde uygulamayı doğrudan çalıştırabilirsin.  
>
> Uygulama tamamen açık kaynak kodludur ve GitHub sayfasında tüm kodları şeffaf bir şekilde paylaşıyorum.  
>  
> İstersen kendin derleyebilir, hatta kendi sisteminde çalıştırarak güvenliğini bizzat test edebilirsin.

## 🔘 Butonlar ve İşlevleri

<p>
  <img src="icon/close.png" width="36" style="vertical-align: middle;"/>
  <strong>Çıkış:</strong> Uygulamayı kapatır.
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
  <strong>Metin Çevirisi:</strong> Metin Çeviri penceresini açar.
</p>

<p>
  <img src="icon/image_text.png" width="36" style="vertical-align: middle;"/>
  <strong>Ekran Çevirisi:</strong> Ekrandan seçilen bölgedeki metinleri algılar, metin çevirisine gönderir. (Dil seçimine göre algılama yapar.)
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
  <img src="icon/correct_text.png" width="36" style="vertical-align: middle;"/>
  <strong>Kelime Düzeltme:</strong> Çevrilecek metindeki kelime yanlışlarını düzeltir. (Türkçe dil desteği yok.)
</p>

<p>
  <img src="icon/variant.png" width="36" style="vertical-align: middle;"/>
  <strong>Dil Varyantlarını:</strong> Dil seçimi için o dilin farklı bölgelerdeki varyantlarını dahil eder.
</p>

<p>
  <img src="icon/translation.png" width="36" style="vertical-align: middle;"/>
  <strong>Çevir:</strong> Çeviri yapar. (ENTER tuşuyla da yapılabilir.)
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
    <img src="app_image/thema.png" style="border-radius: 8px;" />
    <img src="app_image/vertical_minimalist.png" style="height: 322; border-radius: 8px;" />
    <img src="app_image/Cloudlight Bloom.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Dark Mocha.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Deep Blue Night.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Frosted Mint.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Golden Dawn.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Midnight Terminal.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Peach Cream.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Snowy pine.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Soft Dawn.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Sunset Isle.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Verdant Grove.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Violet Dawn.png" style="width: 48%; border-radius: 8px;" />
    <img src="app_image/Violet Twilight.png" style="width: 48%; border-radius: 8px;" />
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

- ✅ No need to keep a website open in the background  
- ✅ No complicated steps for image translation  
- ✅ Everything is fast, simple, and accessible  
- ✅ Helps without interrupting your workflow

## 📄 How Does It Work?

- The main window of the application is in the form of a **toolbar**.  
- It offers users options to **translate text** or **detect and translate text from images**.  
- Programming language: **Python**  
- Interface: **PyQt5**  
- For OCR (text recognition from images): **pytesseract** and its language models  
- For translation: **deep-translator** library  
- For word correction: **language-tool-python** is used  
- All related libraries and dependencies are listed in the `requirements.txt` file.

## 📦 Download

You can download the setup file from the link below to run independently on any system:

📥 [Download PyTranslate Setup File](https://github.com/Abdullahtsn/PyTranslate/releases/tag/v1.0.0)

> ⚠️ **Note:** The setup file (`setup.exe`) is prepared so that PyTranslate can run independently.  
> That means even if Python or additional libraries are not installed on your system, you can run the application directly with this setup file.  
>  
> The application is fully open source and all the code is transparently shared on the GitHub page.  
>  
> You can compile it yourself or test its security by running it on your own system.

## 🔘 Buttons and Their Functions

<p>
  <img src="icon/close.png" width="36" style="vertical-align: middle;"/>
  <strong>Close:</strong> Closes the application.
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
  <strong>Text Translation:</strong> Opens the text translation window.
</p>

<p>
  <img src="icon/image_text.png" width="36" style="vertical-align: middle;"/>
  <strong>Screen Translation:</strong> Detects text in the selected screen area and sends it for translation. (Detection depends on the selected language.)
</p>

<p>
  <img src="icon/transparent.png" width="36" style="vertical-align: middle;"/>
  <strong>Transparency:</strong> Sets the application to be partially transparent to show the background.
</p>

<p>
  <img src="icon/pinned.png" width="36" style="vertical-align: middle;"/>
  <strong>Pin:</strong> Keeps the application always on top.
</p>

<p>
  <img src="icon/rotation.png" width="36" style="vertical-align: middle;"/>
  <strong>Rotate:</strong> Switches the application between horizontal and vertical modes.
</p>

<p>
  <img src="icon/thema.png" width="36" style="vertical-align: middle;"/>
  <strong>Theme:</strong> Changes the application design with dark and light color palettes.
</p>

<p>
  <img src="icon/expand.png" width="36" style="vertical-align: middle;"/>
  <strong>Collapse:</strong> Hides extra buttons to reduce the application's occupied space.
</p>

---

<p>
  <img src="icon/lang_change.png" width="36" style="vertical-align: middle;"/>
  <strong>Swap Languages:</strong> Switches the source and target languages.
</p>

<p>
  <img src="icon/text_change.png" width="36" style="vertical-align: middle;"/>
  <strong>Swap Texts:</strong> Swaps the source and translated texts.
</p>

<p>
  <img src="icon/correct_text.png" width="36" style="vertical-align: middle;"/>
  <strong>Word Correction:</strong> Corrects word mistakes in the text to be translated. (No Turkish language support.)
</p>

<p>
  <img src="icon/variant.png" width="36" style="vertical-align: middle;"/>
  <strong>Language Variants:</strong> Includes different regional variants of the selected language.
</p>

<p>
  <img src="icon/translation.png" width="36" style="vertical-align: middle;"/>
  <strong>Translate:</strong> Performs the translation. (Can also be triggered with the ENTER key.)
</p>

<p>
  <img src="icon/copy.png" width="36" style="vertical-align: middle;"/>
  <strong>Copy:</strong> Copies the text from the associated field.
</p>

<p>
  <img src="icon/paste.png" width="36" style="vertical-align: middle;"/>
  <strong>Paste:</strong> Pastes the copied text into the associated field.
</p>

<p>
  <img src="icon/clear.png" width="36" style="vertical-align: middle;"/>
  <strong>Clear:</strong> Clears the text in the associated field.
</p>
