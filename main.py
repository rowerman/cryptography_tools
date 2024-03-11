from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer,QDateTime
import sys, time, base64

from pyqt5_plugins.examplebuttonplugin import QtGui

from GUI import Gui
import SymEnc

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.timer = QTimer(self)
        StartTime = QDateTime.currentDateTime()
        self.ui.timer.timeout.connect(lambda : self.showtime(StartTime))
        self.ui.timer.start(500)
        
        # 选择不同的功能，对应不同的page
        # AES
        self.ui.pushButton.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_19.clicked.connect(lambda : self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_20.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        # Camellia
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_22.clicked.connect(lambda : self.ui.stackedWidget_3.setCurrentIndex(0))
        self.ui.pushButton_24.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentIndex(1))
        # Chachapoly1305
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_27.clicked.connect(lambda : self.ui.stackedWidget_4.setCurrentIndex(0))
        self.ui.pushButton_28.clicked.connect(lambda: self.ui.stackedWidget_4.setCurrentIndex(1))
        # SM4
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton_39.clicked.connect(lambda : self.ui.stackedWidget_5.setCurrentIndex(0))
        self.ui.pushButton_40.clicked.connect(lambda: self.ui.stackedWidget_5.setCurrentIndex(1))
        
        
        # 勾选复选框后显示对应内容
        # AES
        self.ui.pushButton_21.setEnabled(False)
        self.ui.lineEdit.setReadOnly(True)
        self.ui.plainTextEdit_2.setReadOnly(True)
        self.ui.checkBox.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_21, self.ui.plainTextEdit,self.ui.lineEdit))
        self.ui.checkBox_2.clicked.connect(
            lambda : self.ui.plainTextEdit_2.setReadOnly(not self.ui.plainTextEdit_2.isReadOnly()))
        
        self.ui.pushButton_26.setEnabled(False)
        self.ui.lineEdit_3.setReadOnly(True)
        self.ui.checkBox_6.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_26, self.ui.plainTextEdit_6, self.ui.lineEdit_3))
        # Camellia
        self.ui.pushButton_31.setEnabled(False)
        self.ui.lineEdit_5.setReadOnly(True)
        self.ui.plainTextEdit_8.setReadOnly(True)
        self.ui.checkBox_5.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_31, self.ui.plainTextEdit_7,self.ui.lineEdit_5))
        self.ui.checkBox_7.clicked.connect(
            lambda : self.ui.plainTextEdit_8.setReadOnly(not self.ui.plainTextEdit_8.isReadOnly()))
        
        self.ui.pushButton_31.setEnabled(False)
        self.ui.lineEdit_5.setReadOnly(True)
        self.ui.checkBox_8.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_31, self.ui.plainTextEdit_9, self.ui.lineEdit_5))
        # Chachapoly1305
        self.ui.pushButton_34.setEnabled(False)
        self.ui.lineEdit_6.setReadOnly(True)
        self.ui.plainTextEdit_12.setReadOnly(True)
        self.ui.checkBox_9.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_34, self.ui.plainTextEdit_11,self.ui.lineEdit_6))
        self.ui.checkBox_12.clicked.connect(
            lambda : self.ui.plainTextEdit_12.setReadOnly(not self.ui.plainTextEdit_8.isReadOnly()))
        
        self.ui.pushButton_43.setEnabled(False)
        self.ui.lineEdit_9.setReadOnly(True)
        self.ui.checkBox_13.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_43, self.ui.plainTextEdit_17, self.ui.lineEdit_9))
        # SM4
        self.ui.pushButton_41.setEnabled(False)
        self.ui.lineEdit_12.setReadOnly(True)
        self.ui.plainTextEdit_15.setReadOnly(True)
        self.ui.checkBox_11.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_41, self.ui.plainTextEdit_16,self.ui.lineEdit_12))
        self.ui.checkBox_15.clicked.connect(
            lambda : self.ui.plainTextEdit_15.setReadOnly(not self.ui.plainTextEdit_8.isReadOnly()))
        
        self.ui.pushButton_48.setEnabled(False)
        self.ui.lineEdit_14.setReadOnly(True)
        self.ui.checkBox_16.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_48, self.ui.plainTextEdit_21, self.ui.lineEdit_14))
        
        
        # 点击选择文件后，就选择文件...
        # AES
        self.ui.pushButton_21.clicked.connect(lambda : self.browse_file(self.ui.lineEdit))
        self.ui.pushButton_26.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_3))
        # Camellia
        self.ui.pushButton_30.clicked.connect(lambda : self.browse_file(self.ui.lineEdit_4))
        self.ui.pushButton_31.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_5))
        # Chachapoly1305
        self.ui.pushButton_34.clicked.connect(lambda : self.browse_file(self.ui.lineEdit_6))
        self.ui.pushButton_43.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_9))
        # SM4
        self.ui.pushButton_41.clicked.connect(lambda : self.browse_file(self.ui.lineEdit_12))
        self.ui.pushButton_48.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_14))
        
        # 点击加密按钮后，就加密...
        # AES
        self.ui.pushButton_23.clicked.connect(lambda : self.aesEncrypt(self.ui.lineEdit,self.ui.plainTextEdit,
                                                                       self.ui.plainTextEdit_2,
                                                                       self.ui.checkBox,self.ui.checkBox_2))
        
        self.ui.pushButton_25.clicked.connect(lambda : self.aesDecrypt(self.ui.lineEdit_3,self.ui.plainTextEdit_6,
                                                                       self.ui.plainTextEdit_5,
                                                                       self.ui.checkBox_6,self.ui.checkBox_6))
        # Camellia
        self.ui.pushButton_29.clicked.connect(lambda: self.Camellia_encrypt(self.ui.lineEdit_4, self.ui.plainTextEdit_7,
                                                                      self.ui.plainTextEdit_8,
                                                                      self.ui.checkBox_5, self.ui.checkBox_7))
        
        self.ui.pushButton_32.clicked.connect(lambda: self.Camellia_decrypt(self.ui.lineEdit_5, self.ui.plainTextEdit_9,
                                                                      self.ui.plainTextEdit_10,
                                                                      self.ui.checkBox_8, self.ui.checkBox_8))
        # Chachapoly1305
        self.ui.pushButton_33.clicked.connect(lambda: self.Chacha_encrypt(self.ui.lineEdit_9, self.ui.plainTextEdit_11,
                                                                            self.ui.plainTextEdit_12,
                                                                            self.ui.checkBox_9, self.ui.checkBox_12,
                                                                            self.ui.lineEdit_10))
        
        self.ui.pushButton_44.clicked.connect(lambda: self.Chacha_decrypt(self.ui.lineEdit_9, self.ui.plainTextEdit_17,
                                                                            self.ui.plainTextEdit_18,
                                                                            self.ui.checkBox_13, self.ui.checkBox_13,
                                                                            self.ui.lineEdit_2))
        # SM4
        self.ui.pushButton_42.clicked.connect(lambda: self.SM4_encrypt(self.ui.lineEdit_12, self.ui.plainTextEdit_16,
                                                                            self.ui.plainTextEdit_15,
                                                                            self.ui.checkBox_11, self.ui.checkBox_15))
        self.ui.pushButton_47.clicked.connect(lambda: self.SM4_decrypt(self.ui.lineEdit_14, self.ui.plainTextEdit_21,
                                                                            self.ui.plainTextEdit_22,
                                                                            self.ui.checkBox_16,self.ui.checkBox_16))
        
        
    def showtime(self,StartTime):
        datetime = QDateTime.currentDateTime()
        workingTime = StartTime.secsTo(datetime)
        
        hours = workingTime // 3600  # 计算小时数
        workingTime %= 3600  # 更新剩余的秒数
        minutes = workingTime // 60  # 计算分钟数
        workingTime %= 60  # 更新剩余的秒数
        
        text = "你已经工作了" + str(hours) + "小时"+ str(minutes) + "分钟"+ str(workingTime) + "秒"
        self.ui.label_2.setText(text)
        
    def show_fileDialog(self,button,textedit,lineedit):
        button.setEnabled(not button.isEnabled())
        textedit.setReadOnly(not textedit.isReadOnly())
        lineedit.setReadOnly(not lineedit.isReadOnly())
        
    def browse_file(self,lineedit):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if filename:
            lineedit.setText(filename)
            
    def aesEncrypt(self,LineEdit1,PlainTextEdit_1,PlainTextEdit_2,CheckBox_1,ChcekBox_2):
        if CheckBox_1.isChecked() and LineEdit1.text() == "" :
            QMessageBox.information(self, '提示', '你需要选择文件！')
        elif not CheckBox_1.isChecked() and PlainTextEdit_1.toPlainText() == "" or ChcekBox_2.isChecked() and PlainTextEdit_2.toPlainText() == "":
            QMessageBox.information(self,"提示","你需要输入内容！")
        # type=1:输入密文+自定义密钥 type=2:文件读取密文+自定义密钥 type=3:输入密文+随机密钥 type=4:文件读取密文+随机密钥
        # def aes_encrypt(message, len_key, type, key, filepath):
        if not CheckBox_1.isChecked() and ChcekBox_2.isChecked():
            len_key = self.ui.comboBox.currentText()
            message = PlainTextEdit_1.toPlainText()
            key = PlainTextEdit_2.toPlainText()
            filepath = ""
            Encrypted_content, GetKey = SymEnc.aes_encrypt(message, len_key, 1, key, filepath)
            if Encrypted_content in ["error_key","error_filepath","encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit.setText(Encrypted_content)
            return
        
        if CheckBox_1.isChecked() and ChcekBox_2.isChecked():
            len_key = self.ui.comboBox.currentText()
            message = ""
            key = PlainTextEdit_2.toPlainText()
            filepath = LineEdit1.text()
            Encrypted_content, GetKey = SymEnc.aes_encrypt(message, len_key, 2, key, filepath)
            if Encrypted_content in ["error_key","error_filepath","encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit.setText(Encrypted_content)
            return
        
        if not CheckBox_1.isChecked() and not ChcekBox_2.isChecked():
            len_key = self.ui.comboBox.currentText()
            message = PlainTextEdit_1.toPlainText()
            key = ""
            filepath = ""
            Encrypted_content, GetKey = SymEnc.aes_encrypt(message, len_key, 3, key, filepath)
            if Encrypted_content in ["error_key","error_filepath","encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit.setText(Encrypted_content)
            self.ui.textEdit_2.setText(GetKey.decode())
            return
        
        if CheckBox_1.isChecked() and not ChcekBox_2.isChecked():
            len_key = self.ui.comboBox.currentText()
            message = ""
            key = ""
            filepath = LineEdit1.text()
            Encrypted_content, GetKey = SymEnc.aes_encrypt(message, len_key, 4, key, filepath)
            if Encrypted_content in ["error_key","error_filepath","encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit.setText(Encrypted_content)
            self.ui.textEdit_2.setText(GetKey.decode())
            return
        
    def aesDecrypt(self,LineEdit1,PlainTextEdit_1,PlainTextEdit_2,CheckBox_1,CheckBox_2):
    # def aes_decrypt(ciphertext,key, len_key):
        if CheckBox_1.isChecked() and LineEdit1.text() == "" :
            QMessageBox.information(self, '提示', '你需要选择文件！')
        elif not CheckBox_1.isChecked() and PlainTextEdit_1.toPlainText() == "" :
            QMessageBox.information(self,"提示","你需要输入内容！")
            
        if CheckBox_1.isChecked():
            filepath = LineEdit1.text()
            try:
                file = open(filepath, "r")
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
        else:
            message = PlainTextEdit_1.toPlainText()
        
        if PlainTextEdit_2.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入密钥！")
            
        key = PlainTextEdit_2.toPlainText()
        len_key = self.ui.comboBox_3.currentText()
        DeEncrypted_content = SymEnc.aes_decrypt(message,key,len_key)
        self.ui.textEdit_4.setText(DeEncrypted_content)
        
    def Camellia_encrypt(self,LineEdit1,PlainTextEdit_1,PlainTextEdit_2,CheckBox_1,ChcekBox_2):
        if CheckBox_1.isChecked() and LineEdit1.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
        elif not CheckBox_1.isChecked() and PlainTextEdit_1.toPlainText() == "" or ChcekBox_2.isChecked() and PlainTextEdit_2.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
        # type=1:输入密文+自定义密钥 type=2:文件读取密文+自定义密钥 type=3:输入密文+随机密钥 type=4:文件读取密文+随机密钥
        # def aes_encrypt(message, len_key, type, key, filepath):
        if not CheckBox_1.isChecked() and ChcekBox_2.isChecked():
            len_key = self.ui.comboBox.currentText()
            message = PlainTextEdit_1.toPlainText()
            key = PlainTextEdit_2.toPlainText()
            filepath = ""
            Encrypted_content, GetKey = SymEnc.Camellia_encrypt(message, len_key, 1, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_5.setText(Encrypted_content)
            return
        
        if CheckBox_1.isChecked() and ChcekBox_2.isChecked():
            len_key = self.ui.comboBox.currentText()
            message = ""
            key = PlainTextEdit_2.toPlainText()
            filepath = LineEdit1.text()
            Encrypted_content, GetKey = SymEnc.Camellia_encrypt(message, len_key, 2, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_5.setText(Encrypted_content)
            return
        
        if not CheckBox_1.isChecked() and not ChcekBox_2.isChecked():
            len_key = self.ui.comboBox.currentText()
            message = PlainTextEdit_1.toPlainText()
            key = ""
            filepath = ""
            Encrypted_content, GetKey = SymEnc.Camellia_encrypt(message, len_key, 3, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_5.setText(Encrypted_content)
            self.ui.textEdit_6.setText(GetKey.decode())
            return
        
        if CheckBox_1.isChecked() and not ChcekBox_2.isChecked():
            len_key = self.ui.comboBox.currentText()
            message = ""
            key = ""
            filepath = LineEdit1.text()
            Encrypted_content, GetKey = SymEnc.Camellia_encrypt(message, len_key, 4, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_5.setText(Encrypted_content)
            self.ui.textEdit_6.setText(GetKey.decode())
            return
    def Camellia_decrypt(self,LineEdit1,PlainTextEdit_1,PlainTextEdit_2,CheckBox_1,CheckBox_2):
        # def aes_decrypt(ciphertext,key, len_key):
        if CheckBox_1.isChecked() and LineEdit1.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
        elif not CheckBox_1.isChecked() and PlainTextEdit_1.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
        
        if CheckBox_1.isChecked():
            filepath = LineEdit1.text()
            try:
                file = open(filepath, "r")
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
        else:
            message = PlainTextEdit_1.toPlainText()
        
        if PlainTextEdit_2.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入密钥！")
        
        key = PlainTextEdit_2.toPlainText()
        len_key = self.ui.comboBox_3.currentText()
        DeEncrypted_content = SymEnc.Camellia_decrypt(message, key, len_key)
        self.ui.label_19.setText(DeEncrypted_content)
        
        
    def Chacha_encrypt(self,LineEdit1,PlainTextEdit_1,PlainTextEdit_2,CheckBox_1,ChcekBox_2,LineEdit2):
        if CheckBox_1.isChecked() and LineEdit1.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
        elif not CheckBox_1.isChecked() and PlainTextEdit_1.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
        # type=1:输入密文+自定义密钥 type=2:文件读取密文+自定义密钥 type=3:输入密文+随机密钥 type=4:文件读取密文+随机密钥
        # def ChaCha20Poly1305_encrypt(message,type, key, filepath):
        if CheckBox_1.isChecked() and LineEdit1.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
        elif not CheckBox_1.isChecked() and PlainTextEdit_1.toPlainText() == "" or ChcekBox_2.isChecked() and PlainTextEdit_2.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
        if not CheckBox_1.isChecked() and ChcekBox_2.isChecked():
            message = PlainTextEdit_1.toPlainText()
            key = PlainTextEdit_2.toPlainText()
            filepath = ""
            Encrypted_content, GetKey, Nonce= SymEnc.ChaCha20Poly1305_encrypt(message,1, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_7.setText(Encrypted_content)
            self.ui.lineEdit_10.setText(Nonce.decode())
            return
        
        if CheckBox_1.isChecked() and ChcekBox_2.isChecked():
            message = ""
            key = PlainTextEdit_2.toPlainText()
            filepath = LineEdit1.text()
            Encrypted_content, GetKey, Nonce= SymEnc.ChaCha20Poly1305_encrypt(message,2, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_7.setText(Encrypted_content)
            self.ui.lineEdit_10.setText(Nonce.decode())
            return
        
        if not CheckBox_1.isChecked() and not ChcekBox_2.isChecked():
            message = PlainTextEdit_1.toPlainText()
            key = ""
            filepath = ""
            Encrypted_content, GetKey, Nonce = SymEnc.ChaCha20Poly1305_encrypt(message,3, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_7.setText(Encrypted_content)
            self.ui.lineEdit_10.setText(Nonce.decode())
            self.ui.textEdit_8.setText(GetKey.decode())
            return
        
        if CheckBox_1.isChecked() and not ChcekBox_2.isChecked():
            len_key = self.ui.comboBox.currentText()
            message = ""
            key = ""
            filepath = LineEdit1.text()
            Encrypted_content, GetKey, Nonce= SymEnc.ChaCha20Poly1305_encrypt(message, 4, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_7.setText(Encrypted_content)
            self.ui.lineEdit_10.setText(Nonce.decode())
            self.ui.textEdit_8.setText(GetKey.decode())
            return
            
    def Chacha_decrypt(self,LineEdit1,PlainTextEdit_1,PlainTextEdit_2,CheckBox_1,CheckBox_2,LineEdit2):
        # def aes_decrypt(ciphertext,key, len_key):
        if CheckBox_1.isChecked() and LineEdit1.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
        elif not CheckBox_1.isChecked() and PlainTextEdit_1.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
        
        if CheckBox_1.isChecked():
            filepath = LineEdit1.text()
            try:
                file = open(filepath, "r")
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
        else:
            message = PlainTextEdit_1.toPlainText()
        
        if PlainTextEdit_2.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入密钥！")
        
        key = PlainTextEdit_2.toPlainText()
        Nonce = LineEdit2.text()
        DeEncrypted_content = SymEnc.ChaCha20Poly1305_decrypt(message, key, Nonce)
        self.ui.label_34.setText(DeEncrypted_content)
        
    def SM4_encrypt(self,LineEdit1,PlainTextEdit_1,PlainTextEdit_2,CheckBox_1,CheckBox_2):
        if CheckBox_1.isChecked() and LineEdit1.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
        elif not CheckBox_1.isChecked() and PlainTextEdit_1.toPlainText() == "" or CheckBox_2.isChecked() and PlainTextEdit_2.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
        # type=1:输入密文+自定义密钥 type=2:文件读取密文+自定义密钥 type=3:输入密文+随机密钥 type=4:文件读取密文+随机密钥
        # def aes_encrypt(message, len_key, type, key, filepath):
        if not CheckBox_1.isChecked() and CheckBox_2.isChecked():
            message = PlainTextEdit_1.toPlainText()
            key = PlainTextEdit_2.toPlainText()
            filepath = ""
            Encrypted_content, GetKey = SymEnc.SM4_encrypt(message,1, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_10.setText(Encrypted_content)
            return
        
        if CheckBox_1.isChecked() and CheckBox_2.isChecked():
            message = ""
            key = PlainTextEdit_2.toPlainText()
            filepath = LineEdit1.text()
            Encrypted_content, GetKey = SymEnc.SM4_encrypt(message, 2, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_10.setText(Encrypted_content)
            return
        
        if not CheckBox_1.isChecked() and not CheckBox_2.isChecked():
            message = PlainTextEdit_1.toPlainText()
            key = ""
            filepath = ""
            Encrypted_content, GetKey = SymEnc.SM4_encrypt(message, 3, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_10.setText(Encrypted_content)
            self.ui.textEdit_9.setText(GetKey.decode())
            return
        
        if CheckBox_1.isChecked() and not CheckBox_2.isChecked():
            message = ""
            key = ""
            filepath = LineEdit1.text()
            Encrypted_content, GetKey = SymEnc.SM4_encrypt(message, 4, key, filepath)
            if Encrypted_content in ["error_key", "error_filepath", "encrypt_error"]:
                QMessageBox.information(self, "错误", Encrypted_content)
            self.ui.textEdit_10.setText(Encrypted_content)
            self.ui.textEdit_9.setText(GetKey.decode())
            return
        
    def SM4_decrypt(self,LineEdit1,PlainTextEdit_1,PlainTextEdit_2,CheckBox_1,ChcekBox_2):
        if CheckBox_1.isChecked() and LineEdit1.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
        elif not CheckBox_1.isChecked() and PlainTextEdit_1.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
        
        if CheckBox_1.isChecked():
            filepath = LineEdit1.text()
            try:
                file = open(filepath, "r")
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
        else:
            message = PlainTextEdit_1.toPlainText()
        
        if PlainTextEdit_2.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入密钥！")
        
        key = PlainTextEdit_2.toPlainText()
        DeEncrypted_content = SymEnc.SM4_decrypt(message, key)
        self.ui.textEdit_3.setText(DeEncrypted_content)

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    MainWindow = MyMainWindow()  # 创建主窗口
    MainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 在主线程中退出
