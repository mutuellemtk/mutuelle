# main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy_garden.webview import WebView
from android.permissions import request_permissions, Permission
from android.storage import primary_external_storage_path
from kivy.utils import platform
from jnius import autoclass, cast
import os
import urllib.request

# Android classes
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
File = autoclass('java.io.File')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
PrintManager = autoclass('android.print.PrintManager')

class WebApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        if platform == 'android':
            request_permissions([
                Permission.INTERNET,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])

        self.pdf_path = f"{primary_external_storage_path()}/MTK/Coupon/coupon.pdf"
        self._ensure_directory()

        self.webview = WebView()
        self.webview.url = "https://mutuellemtk.netlify.app/"
        self.webview.bind(on_url=self._handle_pdf)
        self.add_widget(self.webview)

        self.btn_print = Button(text="🖨️ Imprimer ce coupon", size_hint_y=None, height=50)
        self.btn_print.bind(on_release=self._print_pdf)
        self.add_widget(self.btn_print)

    def _ensure_directory(self):
        coupon_dir = os.path.dirname(self.pdf_path)
        if not os.path.exists(coupon_dir):
            os.makedirs(coupon_dir)

    def _handle_pdf(self, instance, url):
        if url.lower().endswith(".pdf"):
            self._download_pdf(url)

    def _download_pdf(self, url):
        try:
            response = urllib.request.urlopen(url)
            data = response.read()
            with open(self.pdf_path, 'wb') as f:
                f.write(data)
            print("PDF téléchargé avec succès :", self.pdf_path)
            self._open_pdf(self.pdf_path)
        except Exception as e:
            print("Erreur lors du téléchargement du PDF:", e)

    def _open_pdf(self, file_path):
        file = File(file_path)
        uri = Uri.fromFile(file)
        intent = Intent(Intent.ACTION_VIEW)
        intent.setDataAndType(uri, "application/pdf")
        intent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY | Intent.FLAG_GRANT_READ_URI_PERMISSION)
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)

    def _print_pdf(self, instance):
        try:
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            file = File(self.pdf_path)
            uri = Uri.fromFile(file)

            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(uri, "application/pdf")
            intent.setFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)

            currentActivity.startActivity(intent)
        except Exception as e:
            print("Erreur d'impression:", e)

class MutuelleApp(App):
    def build(self):
        return WebApp()

if __name__ == '__main__':
    MutuelleApp().run()