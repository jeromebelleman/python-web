'''
Web scraper library
'''

import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.QtWebEngineWidgets

class Web(object):
    '''
    Web scraper class
    '''

    def __init__(self, firsttimeout=.5, timeout=5, retries=5, debug=False):
        '''
        Initialise
        '''

        self.firsttimeout = firsttimeout * 1000
        self.timeout = timeout * 1000
        self.retries = 5

        self.view = PyQt5.QtWebEngineWidgets.QWebEngineView()
        self.page = self.view.page()
        self.page.runJavaScript('let elms')
        self.timer = PyQt5.QtCore.QTimer()

        self.selector = None
        self.callback = None

        if debug:
            self.view.show()

    def load(self, url):
        '''
        Load page
        '''

        self.view.load(PyQt5.QtCore.QUrl(url))

    def runcallback(self, variant):
        '''
        Run JavaScript callback
        '''

        if variant:
            self.timer.stop()
            self.callback(variant)

    def query(self):
        '''
        Query
        '''

        if self.timer.interval != self.timeout:
            self.timer.setInterval(self.timeout)

        self.page.runJavaScript("""
        elms = document.querySelectorAll('%s');
        Object
            .keys(elms)
            .map(key => elms[key].innerText);
        """ % self.selector, self.runcallback)

    def get(self, selector, callback):
        '''
        Get text from page
        '''

        self.selector = selector
        self.callback = callback

        self.timer.timeout.connect(self.query)
        self.timer.start(self.firsttimeout)
