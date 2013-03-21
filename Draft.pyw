#!/usr/bin/env python
import sip
sip.setapi('QString', 2)
import sys, os
from PyQt4 import QtCore, QtGui

iconPath = os.path.join("data","icons")

class Draft(QtGui.QMainWindow):
    def __init__(self, fileName=None, parent=None):
        super(Draft, self).__init__(parent)

        self.setWindowIcon(QtGui.QIcon.fromTheme("applications-office"))
        
        tb = QtGui.QToolBar("File Actions")
        self.addToolBar(tb)

        self.actionNew = QtGui.QAction(QtGui.QIcon.fromTheme('document-new', QtGui.QIcon(iconPath + '/filenew.png')), 'New', self)
        self.actionNew.setShortcut('Ctrl+N')
        self.actionNew.triggered.connect(self.fileNew)
        
        self.actionOpen = QtGui.QAction(QtGui.QIcon.fromTheme('document-open', QtGui.QIcon(iconPath + '/fileopen.png')), 'Open...', self)
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.triggered.connect(self.fileOpen)
        
        self.actionSave = QtGui.QAction(QtGui.QIcon.fromTheme('document-save', QtGui.QIcon(iconPath + '/filesave.png')), 'Save', self, enabled=False)
        self.actionSave.setShortcut('Ctrl+S')
        self.actionSave.triggered.connect(self.fileSave)
        
        self.actionPrintPreview = QtGui.QAction(QtGui.QIcon.fromTheme('fileprint', QtGui.QIcon(iconPath + '/fileprint.png')), 'Preview...', self)
        self.actionPrintPreview.setShortcut('Ctrl+P')
        self.actionPrintPreview.triggered.connect(self.filePrintPreview)
        
        self.actionSavePdf = QtGui.QAction(QtGui.QIcon.fromTheme('document-export', QtGui.QIcon(iconPath + '/exportpdf.png')), 'Export PDF...', self)
        self.actionSavePdf.setShortcut('Ctrl+D')
        self.actionSavePdf.triggered.connect(self.filePrint)
        
        tb.setMovable(False)
        tb.addAction(self.actionNew)
        tb.addAction(self.actionOpen)        
        tb.addAction(self.actionSave)
        tb.addAction(self.actionPrintPreview)
        tb.addAction(self.actionSavePdf)
        
        self.actionQuit = QtGui.QAction("&Quit", self, triggered=self.close)
                
        self.setupEditActions()
        self.setupTextActions()
        
        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.currentCharFormatChanged.connect(self.currentCharFormatChanged)
        self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
        self.setCentralWidget(self.textEdit)
        self.textEdit.setFocus()
        self.setCurrentFileName()
        self.fontChanged(self.textEdit.font())
        self.colorChanged(self.textEdit.textColor())
        self.alignmentChanged(self.textEdit.alignment())
        self.textEdit.document().modificationChanged.connect(self.actionSave.setEnabled)
        self.textEdit.document().modificationChanged.connect(self.setWindowModified)
        self.textEdit.document().undoAvailable.connect(self.actionUndo.setEnabled)
        self.textEdit.document().redoAvailable.connect(self.actionRedo.setEnabled)
        self.setWindowModified(self.textEdit.document().isModified())
        self.actionSave.setEnabled(self.textEdit.document().isModified())
        self.actionUndo.setEnabled(self.textEdit.document().isUndoAvailable())
        self.actionRedo.setEnabled(self.textEdit.document().isRedoAvailable())
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        self.textEdit.copyAvailable.connect(self.actionCopy.setEnabled)
        QtGui.QApplication.clipboard().dataChanged.connect(self.clipboardDataChanged)

        if fileName is None:
            fileName = os.path.join("example.html")

        if not self.load(fileName):
            self.fileNew()

    def closeEvent(self, e):
        if self.maybeSave():
            e.accept()
        else:
            e.ignore()


    def setupEditActions(self):
        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("Edit Actions")
        self.addToolBar(tb)
        tb.setMovable(False)
        
        self.actionUndo = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-undo',
                        QtGui.QIcon(iconPath + '/editundo.png')),
                "&Undo", self, shortcut=QtGui.QKeySequence.Undo)
        tb.addAction(self.actionUndo)

        self.actionRedo = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-redo',
                        QtGui.QIcon(iconPath + '/editredo.png')),
                "&Redo", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Redo)
        tb.addAction(self.actionRedo)

        self.actionCut = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-cut',
                        QtGui.QIcon(iconPath + '/editcut.png')),
                "Cu&t", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Cut)
        #tb.addAction(self.actionCut)

        self.actionCopy = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-copy',
                        QtGui.QIcon(iconPath + '/editcopy.png')),
                "&Copy", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Copy)
        #tb.addAction(self.actionCopy)

        self.actionPaste = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-paste',
                        QtGui.QIcon(iconPath + '/editpaste.png')),
                "&Paste", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Paste,
                enabled=(len(QtGui.QApplication.clipboard().text()) != 0))
        #tb.addAction(self.actionPaste)

    def setupTextActions(self):
        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("Format Actions")
        self.addToolBar(tb)
        tb.setMovable(False)

        self.actionTextBold = QtGui.QAction(
                QtGui.QIcon.fromTheme('format-text-bold',
                        QtGui.QIcon(iconPath + '/textbold.png')),
                "&Bold", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_B,
                triggered=self.textBold, checkable=True)
        bold = QtGui.QFont()
        bold.setBold(True)
        self.actionTextBold.setFont(bold)
        tb.addAction(self.actionTextBold)

        self.actionTextItalic = QtGui.QAction(
                QtGui.QIcon.fromTheme('format-text-italic',
                        QtGui.QIcon(iconPath + '/textitalic.png')),
                "&Italic", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_I,
                triggered=self.textItalic, checkable=True)
        italic = QtGui.QFont()
        italic.setItalic(True)
        self.actionTextItalic.setFont(italic)
        tb.addAction(self.actionTextItalic)

        self.actionTextUnderline = QtGui.QAction(
                QtGui.QIcon.fromTheme('format-text-underline',
                        QtGui.QIcon(iconPath + '/textunder.png')),
                "&Underline", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_U,
                triggered=self.textUnderline, checkable=True)
        underline = QtGui.QFont()
        underline.setUnderline(True)
        self.actionTextUnderline.setFont(underline)
        tb.addAction(self.actionTextUnderline)


        grp = QtGui.QActionGroup(self, triggered=self.textAlign)
        
        
        tbc = QtGui.QToolBar(self)
        tbc.setWindowTitle("Menu")
        self.addToolBar(tbc)
        tbc.setMovable(False)
        left_spacer = QtGui.QWidget()
        left_spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)


        self.actionMenu = QtGui.QAction(QtGui.QIcon.fromTheme('document-properties', QtGui.QIcon(iconPath + '/document-properties.png')), 'Menu', self)
        self.actionMenu.triggered.connect(self.on_mouse_menu)
        tbc.addWidget(left_spacer)
        tbc.addAction(self.actionMenu)

        # create context menu
        self.popMenuMouse = QtGui.QMenu(self)
        self.popMenuMouse.addAction(QtGui.QAction('Create Document', self))    
        self.popMenuMouse.addAction(QtGui.QAction('Close Document', self))  
        self.popMenuMouse.addAction(QtGui.QAction('Fullscreen', self))  
        self.popMenuMouse.addSeparator()
        self.popMenuMouse.addAction(QtGui.QAction('Preferences', self))
        self.popMenuMouse.addSeparator()
        self.popMenuMouse.addAction(QtGui.QAction('About', self, triggered=self.about))

        

        # Make sure the alignLeft is always left of the alignRight.
        if QtGui.QApplication.isLeftToRight():
            self.actionAlignLeft = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-left',
                            QtGui.QIcon(iconPath + '/textleft.png')),
                    "&Left", grp)
            self.actionAlignCenter = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-center',
                            QtGui.QIcon(iconPath + '/textcenter.png')),
                    "C&enter", grp)
            self.actionAlignRight = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-right',
                            QtGui.QIcon(iconPath + '/textright.png')),
                    "&Right", grp)
        else:
            self.actionAlignRight = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-right',
                            QtGui.QIcon(iconPath + '/textright.png')),
                    "&Right", grp)
            self.actionAlignCenter = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-center',
                            QtGui.QIcon(iconPath + '/textcenter.png')),
                    "C&enter", grp)
            self.actionAlignLeft = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-left',
                            QtGui.QIcon(iconPath + '/textleft.png')),
                    "&Left", grp)
 
        self.actionAlignJustify = QtGui.QAction(
                QtGui.QIcon.fromTheme('format-justify-fill',
                        QtGui.QIcon(iconPath + '/textjustify.png')),
                "&Justify", grp)

        self.actionAlignLeft.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        self.actionAlignLeft.setCheckable(True)
        self.actionAlignLeft.setPriority(QtGui.QAction.LowPriority)

        self.actionAlignCenter.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.actionAlignCenter.setCheckable(True)
        self.actionAlignCenter.setPriority(QtGui.QAction.LowPriority)

        self.actionAlignRight.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.actionAlignRight.setCheckable(True)
        self.actionAlignRight.setPriority(QtGui.QAction.LowPriority)

        self.actionAlignJustify.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_J)
        self.actionAlignJustify.setCheckable(True)
        self.actionAlignJustify.setPriority(QtGui.QAction.LowPriority)

        tb.addActions(grp.actions())

        pix = QtGui.QPixmap(16, 16)
        pix.fill(QtCore.Qt.black)
        self.actionTextColor = QtGui.QAction(QtGui.QIcon(pix), "&Color...",
                self, triggered=self.textColor)
        tb.addAction(self.actionTextColor)

        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("Fonts and Size")
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        self.addToolBar(tb)
        tb.setMovable(False)

        self.comboFont = QtGui.QFontComboBox(tb)
        tb.addWidget(self.comboFont)
        self.comboFont.activated[str].connect(self.textFamily)

        self.comboSize = QtGui.QComboBox(tb)
        self.comboSize.setObjectName("comboSize")
        tb.addWidget(self.comboSize)
        self.comboSize.setEditable(True)

        db = QtGui.QFontDatabase()
        for size in db.standardSizes():
            self.comboSize.addItem("%s" % (size))

        self.comboSize.activated[str].connect(self.textSize)
        self.comboSize.setCurrentIndex(
                self.comboSize.findText(
                        "%s" % (QtGui.QApplication.font().pointSize())))
                        

    def on_mouse_menu(self):
        # show context menu
        self.pos = QtGui.QCursor.pos()
        self.popMenuMouse.exec_(self.pos)   
    def load(self, f):
        if not QtCore.QFile.exists(f):
            return False

        fh = QtCore.QFile(f)
        if not fh.open(QtCore.QFile.ReadOnly):
            return False

        data = fh.readAll()
        codec = QtCore.QTextCodec.codecForHtml(data)
        unistr = codec.toUnicode(data)

        if QtCore.Qt.mightBeRichText(unistr):
            self.textEdit.setHtml(unistr)
        else:
            self.textEdit.setPlainText(unistr)

        self.setCurrentFileName(f)
        return True

    def maybeSave(self):
        if not self.textEdit.document().isModified():
            return True

        if self.fileName.startswith(':/'):
            return True

        ret = QtGui.QMessageBox.warning(self, "Draft",
                "The document has been modified.\n"
                "Do you want to save your changes?",
                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                        QtGui.QMessageBox.Cancel)

        if ret == QtGui.QMessageBox.Save:
            return self.fileSave()

        if ret == QtGui.QMessageBox.Cancel:
            return False

        return True

    def setCurrentFileName(self, fileName=''):
        self.fileName = fileName
        self.textEdit.document().setModified(False)

        if not fileName:
            shownName = 'New document'
        else:
            shownName = QtCore.QFileInfo(fileName).fileName()

        self.setWindowTitle(self.tr("%s[*] - %s" % (shownName, "Draft")))
        self.setWindowModified(False)

    def fileNew(self):
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFileName()

    def fileOpen(self):
        fn = QtGui.QFileDialog.getOpenFileName(self, "Open File...", None,
                "HTML-Files (*.htm *.html);;All Files (*)")

        if fn:
            self.load(fn)

    def fileSave(self):
        if not self.fileName:
            return self.fileSaveAs()

        writer = QtGui.QTextDocumentWriter(self.fileName)
        success = writer.write(self.textEdit.document())
        if success:
            self.textEdit.document().setModified(False)

        return success

    def fileSaveAs(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, "Save as...", None,
                "ODF files (*.odt);;HTML-Files (*.htm *.html);;All Files (*)")

        if not fn:
            return False

        lfn = fn.lower()
        if not lfn.endswith(('.odt', '.htm', '.html')):
            # The default.
            fn += '.odt'

        self.setCurrentFileName(fn)
        return self.fileSave()

    def filePrint(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dlg = QtGui.QPrintDialog(printer, self)

        if self.textEdit.textCursor().hasSelection():
            dlg.addEnabledOption(QtGui.QAbstractPrintDialog.PrintSelection)

        dlg.setWindowTitle("Print Document")

        if dlg.exec_() == QtGui.QDialog.Accepted:
            self.textEdit.print_(printer)

        del dlg

    def filePrintPreview(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        preview = QtGui.QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.printPreview)
        preview.exec_()

    def printPreview(self, printer):
        self.textEdit.print_(printer)

    def filePrintPdf(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, "Export as PDF", None,
                "PDF files (*.pdf);;All Files (*)")
        if fn:
            if QtCore.QFileInfo(fn).suffix():
                fn += '.pdf'

            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print_(printer)

    def textBold(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontWeight(self.actionTextBold.isChecked() and QtGui.QFont.Bold or QtGui.QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    def textUnderline(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontUnderline(self.actionTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textItalic(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontItalic(self.actionTextItalic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textFamily(self, family):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)

    def textSize(self, pointSize):
        pointSize = float(pointSize)
        if pointSize > 0:
            fmt = QtGui.QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)


    def textColor(self):
        col = QtGui.QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return

        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)

    def textAlign(self, action):
        if action == self.actionAlignLeft:
            self.textEdit.setAlignment(
                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignAbsolute)
        elif action == self.actionAlignCenter:
            self.textEdit.setAlignment(QtCore.Qt.AlignHCenter)
        elif action == self.actionAlignRight:
            self.textEdit.setAlignment(
                    QtCore.Qt.AlignRight | QtCore.Qt.AlignAbsolute)
        elif action == self.actionAlignJustify:
            self.textEdit.setAlignment(QtCore.Qt.AlignJustify)

    def currentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    def cursorPositionChanged(self):
        self.alignmentChanged(self.textEdit.alignment())

    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(len(QtGui.QApplication.clipboard().text()) != 0)

    def about(self):
        QtGui.QMessageBox.about(self, "About", 
                "Draft"
                "This program is published under the terms of the gpl license, it comes with ABSOLUTELY NO WARRANTY; for details, visit http://www.gnu.org/licenses/gpl.html"
                "Designed by: Emilio Coppola ")

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def fontChanged(self, font):
        self.comboFont.setCurrentIndex(self.comboFont.findText(QtGui.QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(self.comboSize.findText("%s" % font.pointSize()))
        self.actionTextBold.setChecked(font.bold())
        self.actionTextItalic.setChecked(font.italic())
        self.actionTextUnderline.setChecked(font.underline())

    def colorChanged(self, color):
        pix = QtGui.QPixmap(20, 20)
        pix.fill(color)
        self.actionTextColor.setIcon(QtGui.QIcon(pix))

    def alignmentChanged(self, alignment):
        if alignment & QtCore.Qt.AlignLeft:
            self.actionAlignLeft.setChecked(True)
        elif alignment & QtCore.Qt.AlignHCenter:
            self.actionAlignCenter.setChecked(True)
        elif alignment & QtCore.Qt.AlignRight:
            self.actionAlignRight.setChecked(True)
        elif alignment & QtCore.Qt.AlignJustify:
            self.actionAlignJustify.setChecked(True)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    mainWindows = []
    for fn in sys.argv[1:] or [None]:
        textEdit = Draft(fn)
        textEdit.resize(700, 400)
        textEdit.show()
        mainWindows.append(textEdit)

    sys.exit(app.exec_())
