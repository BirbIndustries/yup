import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
#                                 Web Browser (HTML Frame)
from PyQt5.QtWidgets import *


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))
        self.browser.urlChanged.connect(self.update_AddressBar)
        self.setCentralWidget(self.browser)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.navigation_bar = QToolBar('Navigation Toolbar')
        self.addToolBar(self.navigation_bar)

        back_button = QAction("Back", self)
        back_button.setStatusTip('Go to previous page you visited')
        back_button.triggered.connect(self.browser.back)
        self.navigation_bar.addAction(back_button)

        refresh_button = QAction("Refresh", self)
        refresh_button.setStatusTip('Refresh this page')
        refresh_button.triggered.connect(self.browser.reload)
        self.navigation_bar.addAction(refresh_button)

        next_button = QAction("Next", self)
        next_button.setStatusTip('Go to next page')
        next_button.triggered.connect(self.browser.forward)
        self.navigation_bar.addAction(next_button)

        home_button = QAction("Home", self)
        home_button.setStatusTip('Go to home page (Google page)')
        home_button.triggered.connect(self.go_to_home)
        self.navigation_bar.addAction(home_button)

        self.navigation_bar.addSeparator()

        self.URLBar = QLineEdit()
        self.URLBar.returnPressed.connect(lambda: self.go_to_URL(
            QUrl(self.URLBar.text())))  # This specifies what to do when enter is pressed in the Entry field
        self.navigation_bar.addWidget(self.URLBar)

        self.addToolBarBreak()

        # Adding another toolbar which contains the bookmarks
        bookmarks_toolbar = QToolBar('Bookmarks', self)
        self.addToolBar(bookmarks_toolbar)

        pythongeeks = QAction("watch sex", self)
        pythongeeks.setStatusTip("cornography lol")
        pythongeeks.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.youtube.com/watch?v=p7YXXieghto")))
        bookmarks_toolbar.addAction(pythongeeks)

        self.show()

    def go_to_home(self):
        self.browser.setUrl(QUrl('https://www.google.com/'))

    def go_to_URL(self, url: QUrl):
        if url.scheme() == '':
            url.setScheme('https://')
        self.browser.setUrl(url)
        self.update_AddressBar(url)

    def update_AddressBar(self, url):
        self.URLBar.setText(url.toString())
        self.URLBar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName('PythonGeeks Web Browser')

window = Window()
app.exec_()

sys.exit(app.exec_())