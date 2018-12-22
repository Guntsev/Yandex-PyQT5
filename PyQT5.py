import sys
import os
import re
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QMessageBox, QFileDialog, QFontDialog
from PyQt5 import QtCore, QtGui, QtPrintSupport
from PyQt5.QtGui import QIcon
from pygame import mixer
import datetime
import time
from gtts import gTTS
import webbrowser



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.copiedtext=""
        self.initUI()


    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.textEdit.setText(" ")

        exitAction = QAction(QIcon('icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        newAction = QAction(QIcon('icons/new.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New Application')
        newAction.triggered.connect(self.__init__)

        openAction = QAction(QIcon('icons/open.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Application')
        openAction.triggered.connect(self.openo)

        saveAction = QAction(QIcon('icons/save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save Application')
        saveAction.triggered.connect(self.save)
        
        
        
        
        readAction = QAction(QIcon('icons/mp3.png'), 'Save as MP3 and read', self)
        readAction.setShortcut('Ctrl+F')
        readAction.setStatusTip('Save as MP3 and read')
        readAction.triggered.connect(self.read)          
        
        
        
        previewAction = QAction(QIcon("icons/pdf.png"),"Save as PDF",self)
        previewAction.setStatusTip("Save as PDF")
        previewAction.setShortcut("Ctrl+Shift+P")
        previewAction.triggered.connect(self.preview)        
        
        
        
        undoAction = QAction(QIcon('icons/undo.png'), 'Undo', self)
        undoAction.setShortcut('Ctrl+Z')
        undoAction.setStatusTip('Undo')
        undoAction.triggered.connect(self.textEdit.undo)

        redoAction = QAction(QIcon('icons/redo.png'), 'Redo', self)
        redoAction.setShortcut('Ctrl+Y')
        redoAction.setStatusTip('Undo')
        redoAction.triggered.connect(self.textEdit.redo)

        copyAction = QAction(QIcon('icons/copy.png'), 'Copy', self)
        copyAction.setShortcut('Ctrl+C')
        copyAction.setStatusTip('Copy')
        copyAction.triggered.connect(self.copy)

        pasteAction = QAction(QIcon('icons/paste.png'), 'Paste', self)
        pasteAction.setShortcut('Ctrl+V')
        pasteAction.setStatusTip('Paste')
        pasteAction.triggered.connect(self.paste)

        cutAction = QAction(QIcon('icons/cut.png'), 'Cut',self)
        cutAction.setShortcut('Ctrl+X')
        cutAction.setStatusTip('Cut')
        cutAction.triggered.connect(self.cut)
        
        fontAction = QAction(QIcon('icons/font.png'), 'Set font',self)
        fontAction.setShortcut('Ctrl+T')
        fontAction.setStatusTip('Set font')
        fontAction.triggered.connect(self.font)
        
        alignLeft = QAction(QIcon("icons/align-left.png"),"Align left",self)
        fontAction.setStatusTip('Align left')
        alignLeft.triggered.connect(self.alignLeft)
         
        alignCenter = QAction(QIcon("icons/align-center.png"),"Align center",self)
        fontAction.setStatusTip('Align center')
        alignCenter.triggered.connect(self.alignCenter)
         
        alignRight = QAction(QIcon("icons/align-right.png"),"Align right",self)
        fontAction.setStatusTip('Align right')
        alignRight.triggered.connect(self.alignRight)
         
        aboutAction=QAction(QIcon('about.png'), 'About Text Editor',self)
        aboutAction.setStatusTip('About Text Editor')
        aboutAction.triggered.connect(self.about)
        
        aboutmeAction=QAction(QIcon('about.png'), 'About Me',self)
        aboutmeAction.setStatusTip('About Me')
        aboutmeAction.triggered.connect(self.aboutme)        

        
        self.statusBar()

        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(previewAction)
        fileMenu.addAction(readAction)
        fileMenu.addAction(exitAction)
        
        
        
        fileMenu2=menubar.addMenu('&Edit')
        fileMenu2.addAction(undoAction)
        fileMenu2.addAction(redoAction)
        fileMenu2.addAction(cutAction)
        fileMenu2.addAction(copyAction)
        fileMenu2.addAction(pasteAction)
        fileMenu2.addAction(alignLeft)
        fileMenu2.addAction(alignCenter)
        fileMenu2.addAction(alignRight)
              
        fileMenu3=menubar.addMenu('&Settings')
        fileMenu3.addAction(fontAction)
        
        fileMenu4=menubar.addMenu('&Help')
        fileMenu4.addAction(aboutAction)
        fileMenu4.addAction(aboutmeAction)
        

        
        tb1 = self.addToolBar('File')
        tb1.addAction(newAction)
        tb1.addAction(openAction)
        tb1.addAction(saveAction)
        
        tb1.addAction(previewAction)
        tb1.addAction(readAction)

        tb2 = self.addToolBar('Edit')
        tb2.addAction(undoAction)
        tb2.addAction(redoAction)
        tb2.addAction(cutAction)
        tb2.addAction(copyAction)
        tb2.addAction(pasteAction)
        tb2.addAction(alignLeft)
        tb2.addAction(alignCenter)
        tb2.addAction(alignRight)
        
        tb3 = self.addToolBar('Settings')
        tb3.addAction(fontAction)
        
        tb4 = self.addToolBar('Exit')
        tb4.addAction(exitAction)

        
        self.setGeometry(0,0,600,600)
        self.setWindowTitle('Text Editor')
        self.setWindowIcon(QIcon('icons/text.png'))
        self.show()



    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit without Saving?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.statusBar().showMessage('Quiting...')
            event.accept()

        else:
            event.ignore()
            self.save()
            event.accept()

    def openo(self):
        
        self.statusBar().showMessage('Open Text Files ')
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.statusBar().showMessage('Open File')
        
        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)


    def save(self):
        
        self.statusBar().showMessage('Add extension to file name')
        fname = QFileDialog.getSaveFileName(self, 'Save File',"","Text Files (*.txt)")
        data=self.textEdit.toPlainText()

        file = open(fname[0],'w')
        file.write(data)
        file.close()
        
        
    
                
    
    def preview(self):
     
        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()
     
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.textEdit.print_(p))
     
        preview.exec_()
    
     
    
    def copy(self):
        
        cursor=self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedtext=textSelected

    def paste(self):
        
        self.textEdit.append(self.copiedtext)


    def cut(self):
        
        cursor=self.textEdit.textCursor()
        textSelected=cursor.selectedText()
        self.copiedtext=textSelected
        self.textEdit.cut()


    def alignLeft(self):
        
        self.textEdit.setAlignment(QtCore.Qt.AlignLeft)
     
     
    def alignRight(self):
        
        self.textEdit.setAlignment(QtCore.Qt.AlignRight)
     
     
    def alignCenter(self):
        
        self.textEdit.setAlignment(QtCore.Qt.AlignCenter)
     
   
    
    def about(self):
        
        url ="https://en.wikipedia.org/wiki/Text_editor"
        self.statusBar().showMessage('Loading url...')
        webbrowser.open(url)
        
    def aboutme(self):
        
        url ="https://vk.com/guntsevanton"
        self.statusBar().showMessage('Loading url...')
        webbrowser.open(url)        
        
        
    def font(self):
        
        font, ok = QFontDialog.getFont(self.textEdit.font(), self)
        
        if ok:
            #QApplication.setFont(font)
            self.textEdit.setFont(font)
            print("Display Fonts", font)    
            
            
            
            
            
            
            
    def read(self):
        # Для того чтобы не возникало коллизий при удалении mp3 файлов
        # заведем переменную mp3_nameold в которой будем хранить имя предыдущего mp3 файла
        mp3_nameold='111'
        mp3_name = "1.mp3"

        # Инициализируем звуковое устройство
        mixer.init()

        
        self.statusBar().showMessage('Add extension to file name')
        fname = QFileDialog.getSaveFileName(self, 'Save File',"","Text Files (*.txt)")
        data=self.textEdit.toPlainText()

        fi = open(fname[0],'w')
        fi.write(data)
        fi.close()
        
        
        # Открываем файл с текстом и по очереди читаем с него строки в ss
        f = open(fname[0],"r")
        ss = f.readline()
        while ss:
            # Делим прочитанные строки на отдельные предложения
            split_regex = re.compile(r'[.|!|?|…]')
            sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(ss)])

            # Перебираем массив с предложениями 
            for x in sentences:
                if(x!=""):
                    
                    # Эта строка отправляет предложение которое нужно озвучить гуглу
                    tts=gTTS(text=x, lang='ru')
                    # Получаем от гугла озвученное предложение в виде mp3 файла           
                    tts.save(mp3_name)
                    # Проигрываем полученный mp3 файл
                    mixer.music.load(mp3_name)
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)
                    # Если предыдущий mp3 файл существует удаляем его
                    # чтобы не захламлять папку с приложением кучей mp3 файлов
                    if(os.path.exists(mp3_nameold) and (mp3_nameold!="1.mp3")):
                        os.remove(mp3_nameold)
                    mp3_nameold=mp3_name
                    # Формируем имя mp3 файла куда будет сохраняться озвученный текст текущего предложения
                    # В качестве имени файла используем текущие дату и время
                    now_time = datetime.datetime.now()
                    mp3_name = now_time.strftime("%d%m%Y%I%M%S")+".mp3"
            
              # Читаем следующую порцию текста из файла
            ss = f.readline()

        # Закрываем файл    
        
        
        # Устаналиваем текущим файлом 1.mp3 и закрываем звуковое устройство
        # Это нужно чтобы мы могли удалить предыдущий mp3 файл без колизий
        mixer.music.load('1.mp3')
        mixer.stop
        mixer.quit
        


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())