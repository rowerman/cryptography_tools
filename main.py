from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer, QDateTime, Qt, QThread, pyqtSignal
import sys, time, base64,imghdr,os

from cryptography.hazmat.primitives import serialization
from pyqt5_plugins.examplebuttonplugin import QtGui

import WaterMarking
from GUI import Gui
import SymEnc, AsyEnc, Signature


class EmbedTextThread(QThread):
    taskFinished = pyqtSignal(str, str)

    def __init__(self, imgPath, text, storePath):
        super().__init__()
        self.imgPath = imgPath
        self.text = text
        self.storePath = storePath

    def run(self):
        len_wm, output_path = WaterMarking.embed_text(self.imgPath, self.text, self.storePath)
        self.taskFinished.emit(output_path, str(len_wm))
        
class GetTextThread(QThread):
    taskFinished = pyqtSignal(str, str)

    def __init__(self, imgPath, len_wm, output_path):
        super().__init__()
        self.imgPath = imgPath
        self.len_wm = len_wm
        self.output_path = output_path

    def run(self):
        TextGet = WaterMarking.get_text(self.imgPath, self.len_wm, self.output_path)
        self.taskFinished.emit(TextGet)
        
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
        # RSA
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.pushButton_45.clicked.connect(lambda: self.ui.stackedWidget_6.setCurrentIndex(0))
        self.ui.pushButton_46.clicked.connect(lambda: self.ui.stackedWidget_6.setCurrentIndex(1))
        self.ui.pushButton_35.clicked.connect(lambda: self.ui.stackedWidget_6.setCurrentIndex(2))
        # Ed25519
        self.ui.pushButton_6.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))
        # Ed448
        self.ui.pushButton_7.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(6))
        # Ed448签名
        self.ui.pushButton_8.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(7))
        self.ui.pushButton_54.clicked.connect(lambda: self.ui.stackedWidget_7.setCurrentIndex(0))
        self.ui.pushButton_53.clicked.connect(lambda: self.ui.stackedWidget_7.setCurrentIndex(1))
        # CMAC
        self.ui.pushButton_9.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(8))
        self.ui.pushButton_60.clicked.connect(lambda: self.ui.stackedWidget_8.setCurrentIndex(1))
        self.ui.pushButton_61.clicked.connect(lambda: self.ui.stackedWidget_8.setCurrentIndex(0))
        # HMAC
        self.ui.pushButton_10.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(9))
        self.ui.pushButton_67.clicked.connect(lambda: self.ui.stackedWidget_9.setCurrentIndex(1))
        self.ui.pushButton_68.clicked.connect(lambda: self.ui.stackedWidget_9.setCurrentIndex(0))
        # poly1305
        self.ui.pushButton_11.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(10))
        self.ui.pushButton_74.clicked.connect(lambda: self.ui.stackedWidget_10.setCurrentIndex(1))
        self.ui.pushButton_75.clicked.connect(lambda: self.ui.stackedWidget_10.setCurrentIndex(0))
        # SHA
        self.ui.pushButton_12.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(11))
        # SHAKE
        self.ui.pushButton_13.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(12))
        # 嵌入文字
        self.ui.pushButton_14.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(13))
        self.ui.pushButton_93.clicked.connect(lambda: self.ui.stackedWidget_11.setCurrentIndex(0))
        self.ui.pushButton_94.clicked.connect(lambda: self.ui.stackedWidget_11.setCurrentIndex(1))
        
        
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
        # RSA
        self.ui.pushButton_49.setEnabled(False)
        self.ui.lineEdit_13.setReadOnly(True)
        self.ui.checkBox_14.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_49, self.ui.plainTextEdit_19,self.ui.lineEdit_13))
        
        self.ui.pushButton_51.setEnabled(False)
        self.ui.lineEdit_15.setReadOnly(True)
        self.ui.checkBox_18.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_51, self.ui.plainTextEdit_23, self.ui.lineEdit_15))
        # Ed448签名
        self.ui.pushButton_57.setEnabled(False)
        self.ui.lineEdit_17.setReadOnly(True)
        self.ui.checkBox_21.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_57, self.ui.plainTextEdit_26,self.ui.lineEdit_17))
        
        self.ui.pushButton_55.setEnabled(False)
        self.ui.pushButton_59.setEnabled(False)
        self.ui.lineEdit_8.setReadOnly(True)
        self.ui.lineEdit_16.setReadOnly(True)
        self.ui.checkBox_19.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_55, self.ui.plainTextEdit_20, self.ui.lineEdit_16))
        self.ui.checkBox_3.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_59, self.ui.plainTextEdit_3, self.ui.lineEdit_8))
        # CMAC
        self.ui.pushButton_66.setEnabled(False)
        self.ui.lineEdit_20.setReadOnly(True)
        self.ui.checkBox_22.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_66, self.ui.plainTextEdit_29,self.ui.lineEdit_20))
        
        self.ui.pushButton_64.setEnabled(False)
        self.ui.pushButton_62.setEnabled(False)
        self.ui.lineEdit_19.setReadOnly(True)
        self.ui.lineEdit_11.setReadOnly(True)
        self.ui.checkBox_20.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_64, self.ui.plainTextEdit_28, self.ui.lineEdit_19))
        self.ui.checkBox_4.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_62, self.ui.plainTextEdit_4, self.ui.lineEdit_11))
        
        #HMAC
        self.ui.pushButton_72.setEnabled(False)
        self.ui.lineEdit_24.setReadOnly(True)
        self.ui.checkBox_24.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_72, self.ui.plainTextEdit_32,self.ui.lineEdit_24))
        
        self.ui.pushButton_71.setEnabled(False)
        self.ui.pushButton_69.setEnabled(False)
        self.ui.lineEdit_23.setReadOnly(True)
        self.ui.lineEdit_21.setReadOnly(True)
        self.ui.checkBox_23.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_71, self.ui.plainTextEdit_31, self.ui.lineEdit_23))
        self.ui.checkBox_10.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_69, self.ui.plainTextEdit_13, self.ui.lineEdit_21))
        # poly1305
        self.ui.pushButton_79.setEnabled(False)
        self.ui.lineEdit_28.setReadOnly(True)
        self.ui.checkBox_27.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_79, self.ui.plainTextEdit_35,self.ui.lineEdit_28))
        
        self.ui.pushButton_78.setEnabled(False)
        self.ui.pushButton_76.setEnabled(False)
        self.ui.lineEdit_27.setReadOnly(True)
        self.ui.lineEdit_25.setReadOnly(True)
        self.ui.checkBox_26.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_78, self.ui.plainTextEdit_34, self.ui.lineEdit_27))
        self.ui.checkBox_25.clicked.connect(
            lambda: self.show_fileDialog(self.ui.pushButton_76, self.ui.plainTextEdit_14, self.ui.lineEdit_25))
        # SHA
        self.ui.pushButton_89.setEnabled(False)
        self.ui.lineEdit_36.setReadOnly(True)
        self.ui.checkBox_33.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_89, self.ui.plainTextEdit_43,self.ui.lineEdit_36))
        # SHAKE
        self.ui.pushButton_91.setEnabled(False)
        self.ui.lineEdit_37.setReadOnly(True)
        self.ui.checkBox_34.clicked.connect(
            lambda : self.show_fileDialog(self.ui.pushButton_91, self.ui.plainTextEdit_44,self.ui.lineEdit_37))
          
        
        
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
        # RSA
        self.ui.pushButton_49.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_13))
        self.ui.pushButton_51.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_15))
        # Ed448签名
        self.ui.pushButton_57.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_17))
        self.ui.pushButton_55.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_16))
        self.ui.pushButton_59.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_8))
        # CMAC
        self.ui.pushButton_66.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_20))
        self.ui.pushButton_64.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_19))
        self.ui.pushButton_62.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_11))
        # HMAC
        self.ui.pushButton_72.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_24))
        self.ui.pushButton_71.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_23))
        self.ui.pushButton_69.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_21))
        # poly1305
        self.ui.pushButton_79.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_28))
        self.ui.pushButton_78.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_27))
        self.ui.pushButton_76.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_25))
        # SHA
        self.ui.pushButton_89.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_36))
        # SHAKE
        self.ui.pushButton_91.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_37))
        # 嵌入文字
        self.ui.pushButton_98.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_42))
        self.ui.pushButton_99.clicked.connect(lambda: self.browse_folder(self.ui.lineEdit_41))
        self.ui.pushButton_101.clicked.connect(lambda: self.browse_file(self.ui.lineEdit_44))
        self.ui.pushButton_102.clicked.connect(lambda: self.browse_folder(self.ui.lineEdit_43))
        
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
        # RSA
        self.ui.pushButton_50.clicked.connect(lambda: self.RSA_encrypt(self.ui.lineEdit_13, self.ui.plainTextEdit_19,
                                                                       self.ui.checkBox_14,self.ui.comboBox_2))
        self.ui.pushButton_52.clicked.connect(lambda: self.RSA_decrypt(self.ui.lineEdit_15, self.ui.plainTextEdit_23,
                                                                       self.ui.plainTextEdit_24,self.ui.checkBox_18))
        self.ui.pushButton_36.clicked.connect(lambda: self.Gen_RSA_key(self.ui.comboBox_7))
        # Ed25519
        self.ui.pushButton_37.clicked.connect(lambda: self.Ed25519_generate())
        # Ed448
        self.ui.pushButton_38.clicked.connect(lambda: self.Ed448_generate())
        # Ed448签名
        self.ui.pushButton_58.clicked.connect(lambda: self.Ed448_sig(self.ui.lineEdit_17,self.ui.plainTextEdit_26,self.ui.checkBox_21))
        self.ui.pushButton_56.clicked.connect(lambda: self.Ed448_verify(self.ui.lineEdit_16,self.ui.lineEdit_8,
                                                                     self.ui.plainTextEdit_20,self.ui.plainTextEdit_3,self.ui.plainTextEdit_25,
                                                                     self.ui.checkBox_19,self.ui.checkBox_3))
        # CMAC
        self.ui.pushButton_65.clicked.connect(lambda: self.CMAC_en(self.ui.lineEdit_20,self.ui.plainTextEdit_29,
                                                                   self.ui.checkBox_22,self.ui.comboBox_6))
        self.ui.pushButton_63.clicked.connect(lambda: self.CMAC_de(self.ui.lineEdit_19,self.ui.lineEdit_11,
                                                                     self.ui.plainTextEdit_28,self.ui.plainTextEdit_4,self.ui.plainTextEdit_27,
                                                                     self.ui.checkBox_20,self.ui.checkBox_4))
        # HMAC
        self.ui.pushButton_73.clicked.connect(lambda: self.HMAC_en(self.ui.lineEdit_24,self.ui.plainTextEdit_32,
                                                                   self.ui.checkBox_24))
        self.ui.pushButton_70.clicked.connect(lambda: self.HMAC_de(self.ui.lineEdit_23,self.ui.lineEdit_21,
                                                                     self.ui.plainTextEdit_31,self.ui.plainTextEdit_13,self.ui.plainTextEdit_30,
                                                                     self.ui.checkBox_23,self.ui.checkBox_10))
        # poly1305
        self.ui.pushButton_80.clicked.connect(lambda: self.poly1305_en(self.ui.lineEdit_28,self.ui.plainTextEdit_35,
                                                                   self.ui.checkBox_27))
        self.ui.pushButton_77.clicked.connect(lambda: self.poly1305_de(self.ui.lineEdit_27,self.ui.lineEdit_25,
                                                                     self.ui.plainTextEdit_34,self.ui.plainTextEdit_14,self.ui.plainTextEdit_33,
                                                                     self.ui.checkBox_26,self.ui.checkBox_25))
        # SHA
        self.ui.pushButton_90.clicked.connect(lambda: self.SHA_family(self.ui.lineEdit_36,self.ui.plainTextEdit_43,
                                                                      self.ui.checkBox_33,self.ui.comboBox_8))
        # SHAKE
        self.ui.pushButton_92.clicked.connect(lambda: self.SHAKE_family(self.ui.lineEdit_37,self.ui.lineEdit_38,
                                                                        self.ui.plainTextEdit_44,self.ui.checkBox_34,
                                                                        self.ui.comboBox_9))
        
        # 数字水印相关
        self.ui.lineEdit_42.textChanged.connect(lambda: self.showImage(self.ui.lineEdit_42,self.ui.label_148))
        self.ui.lineEdit_44.textChanged.connect(lambda: self.showImage(self.ui.lineEdit_44, self.ui.label_153))
        self.ui.pushButton_100.clicked.connect(lambda: self.Embed_text(self.ui.lineEdit_42,self.ui.lineEdit_41,
                                                                       self.ui.textEdit_22,self.ui.label_146))
        self.ui.pushButton_103.clicked.connect(lambda: self.getText(self.ui.lineEdit_44,self.ui.lineEdit_43,
                                                                    self.ui.lineEdit_46,self.ui.textEdit_37))
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
        
    def showImage(self,LineEdit,Label):
        imagePath = LineEdit.text()
        try:
            # self.ui.label.setPixmap(QtGui.QPixmap('./pictures/4.jpg'))
            Label.setScaledContents(True)  # 设置scaledContents属性为True
            pixmap = QtGui.QPixmap(imagePath)
            pixmap = pixmap.scaled(Label.width(), Label.height(), Qt.KeepAspectRatio)
            Label.setPixmap(pixmap)
            return
        except:
            QMessageBox.information(self, "提示", "请选择一张图片！")
            return
        
        
    def browse_file(self,lineedit):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if filename:
            lineedit.setText(filename)
            
    def browse_folder(self,lineedit):
        foldername = QFileDialog.getExistingDirectory(self, 'Open Folder')
        if foldername:
            lineedit.setText(foldername)
            
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

    def RSA_encrypt(self,LineEdit,PlainTextEdit,CheckBox,ComboBox):
        # def RSA_encrypt(message, len_secret_key):
        if CheckBox.isChecked() and LineEdit.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
            return
        elif not CheckBox.isChecked() and PlainTextEdit.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
            return
        
        if CheckBox.isChecked():
            filepath = LineEdit.text()
            try:
                file = open(filepath,'r')
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            message = PlainTextEdit.toPlainText()
        len_key = ComboBox.currentText()
        Encrypted_content, public_key, private_key = AsyEnc.RSA_encrypt(message, len_key)
        # 将公私钥转化为PEM格式
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.ui.textEdit_11.setText(Encrypted_content)
        self.ui.textEdit_12.setText(public_pem.decode())
        self.ui.textEdit_14.setText(private_pem.decode())
        
    def RSA_decrypt(self,LineEdit,PlainTextEdit1,PlainTextEdit2,CheckBox):
        if CheckBox.isChecked() and LineEdit.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
            return
        elif not CheckBox.isChecked() and PlainTextEdit1.toPlainText() == "" or PlainTextEdit2.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
            return
        
        if CheckBox.isChecked():
            filepath = LineEdit.text()
            try:
                file = open(filepath, "r")
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            message = PlainTextEdit1.toPlainText()
            
        private_key = PlainTextEdit2.toPlainText()
        Decrypted_data = AsyEnc.RSA_decrypt(message, private_key)
        self.ui.textEdit_13.setText(Decrypted_data)
        
    def Gen_RSA_key(self,ComboBox):
        len_key = ComboBox.currentText()
        public_key, private_key = AsyEnc.generate_RSA_keys(int(len_key))
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.ui.textEdit_15.setText(public_pem.decode())
        self.ui.textEdit_16.setText(private_pem.decode())
        
    def Ed25519_generate(self):
        pub_key, pri_key = AsyEnc.generate_Ed25519_keys()
        # Convert the private key to PEM format
        pem_private_key = pri_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Convert the public key to PEM format
        pem_public_key = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.ui.textEdit_17.setText(pem_public_key.decode())
        self.ui.textEdit_18.setText(pem_private_key.decode())
        

    def Ed448_generate(self):
        pub_key, pri_key  = AsyEnc.generate_Ed448_keys()
        pem_private_key = pri_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Convert the public key to PEM format
        pem_public_key = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.ui.textEdit_19.setText(pem_public_key.decode())
        self.ui.textEdit_20.setText(pem_private_key.decode())
        
    def Ed448_sig(self,LineEdit,PlainTextEdit,CheckBox):
        if CheckBox.isChecked() and LineEdit.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
            return
        elif not CheckBox.isChecked() and PlainTextEdit.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
            return
        if CheckBox.isChecked():
            filepath = LineEdit.text()
            try:
                file = open(filepath,'r')
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            message = PlainTextEdit.toPlainText()
            
        signature, public_key, private_key = Signature.Ed448_Sig(message)
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Convert the public key to PEM format
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.ui.textEdit_23.setText(signature)
        self.ui.textEdit_24.setText(pem_public_key.decode())
        self.ui.textEdit_25.setText(pem_private_key.decode())
        
    def Ed448_verify(self,LineEdit1, LineEdit2,PlainTextEdit1,PlainTextEdit2,PlainTextEdit3,CheckBox1,CheckBox2):
        if CheckBox1.isChecked() and LineEdit1.text() == "" or CheckBox2.isChecked() and LineEdit2.text() == "":
            QMessageBox.information(self, "提示", "请输入文件路径!")
            return
        if not CheckBox1.isChecked() and PlainTextEdit1.toPlainText() == "" or not CheckBox2.isChecked() and PlainTextEdit2.toPlainText() == "":
            QMessageBox.information(self, "提示", "请输入签名或公钥!")
            return
        if PlainTextEdit3.toPlainText() == "":
            QMessageBox.information(self, "提示", "请输入公钥!")
            return
        
        if CheckBox1.isChecked():
            filepath = LineEdit1.text()
            try:
                file = open(filepath,'r')
                Sig = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            Sig = PlainTextEdit1.toPlainText()
            
        if CheckBox2.isChecked():
            filepath = LineEdit2.text()
            try:
                file = open(filepath,'r')
                origin_msg = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            origin_msg = PlainTextEdit2.toPlainText()
            
        public_key = PlainTextEdit3.toPlainText()
        
        result = Signature.Ed448_Verify(origin_msg,Sig,public_key)
        if result:
            self.ui.lineEdit_7.setText("验证成功！")
        else:
            self.ui.lineEdit_7.setText("验证失败！")
        
    def CMAC_en(self,LineEdit,PlainTextEdit,CheckBox,ComboBox):
        if CheckBox.isChecked() and LineEdit.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
            return
        elif not CheckBox.isChecked() and PlainTextEdit.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
            return
        if CheckBox.isChecked():
            filepath = LineEdit.text()
            try:
                file = open(filepath,'r')
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            message = PlainTextEdit.toPlainText()
            
        len_key = ComboBox.currentText()
        MAC, key = Signature.CMAC_en(message,len_key)
        self.ui.textEdit_27.setText(MAC)
        self.ui.textEdit_26.setText(key.decode())
        
    def CMAC_de(self,LineEdit1, LineEdit2,PlainTextEdit1,PlainTextEdit2,PlainTextEdit3,CheckBox1,CheckBox2):
        if CheckBox1.isChecked() and LineEdit1.text() == "" or CheckBox2.isChecked() and LineEdit2.text() == "":
            QMessageBox.information(self, "提示", "请输入文件路径!")
            return
        if not CheckBox1.isChecked() and PlainTextEdit1.toPlainText() == "" or not CheckBox2.isChecked() and PlainTextEdit2.toPlainText() == "":
            QMessageBox.information(self, "提示", "请输入签名或公钥!")
            return
        if PlainTextEdit3.toPlainText() == "":
            QMessageBox.information(self, "提示", "请输入公钥!")
            return
        
        if CheckBox1.isChecked():
            filepath = LineEdit1.text()
            try:
                file = open(filepath, 'r')
                Sig = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            Sig = PlainTextEdit1.toPlainText()
        
        if CheckBox2.isChecked():
            filepath = LineEdit2.text()
            try:
                file = open(filepath, 'r')
                origin_msg = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            origin_msg = PlainTextEdit2.toPlainText()
        
        public_key = PlainTextEdit3.toPlainText()
        
        result = Signature.CMAC_de(origin_msg, public_key, Sig)
        if result:
            self.ui.lineEdit_18.setText("验证成功！")
        else:
            self.ui.lineEdit_18.setText("验证失败！")
        
    def HMAC_en(self,LineEdit,PlainTextEdit,CheckBox):
        if CheckBox.isChecked() and LineEdit.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
            return
        elif not CheckBox.isChecked() and PlainTextEdit.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
            return
        if CheckBox.isChecked():
            filepath = LineEdit.text()
            try:
                file = open(filepath, 'r')
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            message = PlainTextEdit.toPlainText()
        
        MAC, key = Signature.HMAC_en(message)
        self.ui.textEdit_28.setText(MAC)
        self.ui.textEdit_29.setText(key.decode())
        
    def HMAC_de(self,LineEdit1, LineEdit2,PlainTextEdit1,PlainTextEdit2,PlainTextEdit3,CheckBox1,CheckBox2):
        if CheckBox1.isChecked() and LineEdit1.text() == "" or CheckBox2.isChecked() and LineEdit2.text() == "":
            QMessageBox.information(self, "提示", "请输入文件路径!")
            return
        if not CheckBox1.isChecked() and PlainTextEdit1.toPlainText() == "" or not CheckBox2.isChecked() and PlainTextEdit2.toPlainText() == "":
            QMessageBox.information(self, "提示", "请输入签名或公钥!")
            return
        if PlainTextEdit3.toPlainText() == "":
            QMessageBox.information(self, "提示", "请输入公钥!")
            return
        
        if CheckBox1.isChecked():
            filepath = LineEdit1.text()
            try:
                file = open(filepath, 'r')
                Sig = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            Sig = PlainTextEdit1.toPlainText()
        
        if CheckBox2.isChecked():
            filepath = LineEdit2.text()
            try:
                file = open(filepath, 'r')
                origin_msg = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            origin_msg = PlainTextEdit2.toPlainText()
        
        public_key = PlainTextEdit3.toPlainText()
        
        result = Signature.HMAC_de(origin_msg, public_key, Sig)
        if result:
            self.ui.lineEdit_22.setText("验证成功！")
        else:
            self.ui.lineEdit_22.setText("验证失败！")
        
    def poly1305_en(self,LineEdit,PlainTextEdit,CheckBox):
        if CheckBox.isChecked() and LineEdit.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
            return
        elif not CheckBox.isChecked() and PlainTextEdit.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
            return
        if CheckBox.isChecked():
            filepath = LineEdit.text()
            try:
                file = open(filepath, 'r')
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            message = PlainTextEdit.toPlainText()
        
        MAC, key = Signature.poly1305_en(message)
        self.ui.textEdit_30.setText(MAC)
        self.ui.textEdit_31.setText(key.decode())
        
    def poly1305_de(self,LineEdit1, LineEdit2,PlainTextEdit1,PlainTextEdit2,PlainTextEdit3,CheckBox1,CheckBox2):
        if CheckBox1.isChecked() and LineEdit1.text() == "" or CheckBox2.isChecked() and LineEdit2.text() == "":
            QMessageBox.information(self, "提示", "请输入文件路径!")
            return
        if not CheckBox1.isChecked() and PlainTextEdit1.toPlainText() == "" or not CheckBox2.isChecked() and PlainTextEdit2.toPlainText() == "":
            QMessageBox.information(self, "提示", "请输入签名或公钥!")
            return
        if PlainTextEdit3.toPlainText() == "":
            QMessageBox.information(self, "提示", "请输入公钥!")
            return
        
        if CheckBox1.isChecked():
            filepath = LineEdit1.text()
            try:
                file = open(filepath, 'r')
                Sig = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            Sig = PlainTextEdit1.toPlainText()
        
        if CheckBox2.isChecked():
            filepath = LineEdit2.text()
            try:
                file = open(filepath, 'r')
                origin_msg = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            origin_msg = PlainTextEdit2.toPlainText()
        
        public_key = PlainTextEdit3.toPlainText()
        
        result = Signature.poly1305_de(origin_msg, public_key, Sig)
        if result:
            self.ui.lineEdit_26.setText("验证成功！")
        else:
            self.ui.lineEdit_26.setText("验证失败！")
            
    def SHA_family(self,LineEdit,PlainTextEdit,CheckBox,ComboBox):
        if CheckBox.isChecked() and LineEdit.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
            return
        elif not CheckBox.isChecked() and PlainTextEdit.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
            return
        if CheckBox.isChecked():
            filepath = LineEdit.text()
            try:
                file = open(filepath, 'r')
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            message = PlainTextEdit.toPlainText()
        type_sha = ComboBox.currentText()
        Hash = Signature.SHA_family(message, type_sha)
        self.ui.textEdit_34.setText(Hash)
        
    def SHAKE_family(self,LineEdit1,LineEdit2,PlainTextEdit,CheckBox,ComboBox):
        if CheckBox.isChecked() and LineEdit1.text() == "":
            QMessageBox.information(self, '提示', '你需要选择文件！')
            return
        elif not CheckBox.isChecked() and PlainTextEdit.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
            return
        if CheckBox.isChecked():
            filepath = LineEdit1.text()
            try:
                file = open(filepath, 'r')
                message = file.read()
                file.close()
            except:
                QMessageBox.information(self, "提示", "文件路径错误！")
                return
        else:
            message = PlainTextEdit.toPlainText()
            
        if LineEdit2.text() == "":
            QMessageBox.information(self, "提示", "你需要选择密钥长度！")
            return
        len_output = LineEdit2.text()
        if int(len_output)< 128 or int(len_output) > 8192:
            QMessageBox.information(self, "提示", "密钥长度范围为128-8192！")
            return
        type_shake = ComboBox.currentText()
        HASH = Signature.Shake_family(message, len_output,type_shake)
        self.ui.textEdit_35.setText(HASH)
        
    def Embed_text(self,LineEdit1,LineEdit2,TextEdit, Label):
        if LineEdit1.text() == "" or LineEdit2.text() == "" or TextEdit.toPlainText() == "":
            QMessageBox.information(self, "提示", "你需要输入内容！")
            return
        if not os.path.exists(LineEdit1.text()) or not os.path.exists(LineEdit2.text()):
            QMessageBox.information(self, "提示", "文件路径错误！")
            return
        # 判断输入是否为图片
        imgPath = LineEdit1.text()
        storePath = LineEdit2.text()
        text = TextEdit.toPlainText()
        _, ext = os.path.splitext(imgPath)
        if ext.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            if imghdr.what(imgPath) == None:
                QMessageBox.information(self, "提示", "输入不是一个图片！")
                return
        else:
            QMessageBox.information(self, "提示", "输入不是一个图片！")
            return
        
        thread = EmbedTextThread(imgPath, text, storePath)
        thread.taskFinished.connect(self.on_embed_text_finished)  # 当任务完成时，关闭对话框
        thread.start()
        # 创建一个模态对话框
        self.messageBox = QMessageBox()
        self.messageBox.setText("正在嵌入...")
        self.messageBox.setStandardButtons(QMessageBox.NoButton)  # 不显示任何标准按钮
        self.messageBox.show()  # 显示对话框
    
    def on_embed_text_finished(self, output_path, len_wm):
        self.ui.lineEdit_41.setText(output_path)
        self.ui.lineEdit_45.setText(len_wm)
        # 展示成品
        self.ui.label_146.setScaledContents(True)  # 设置scaledContents属性为True
        pixmap = QtGui.QPixmap(output_path)
        pixmap = pixmap.scaled(self.ui.label_146.width(), self.ui.label_146.height(), Qt.KeepAspectRatio)
        self.ui.label_146.setPixmap(pixmap)
        self.messageBox.accept()  # 关闭对话框
        
    def getText(self,LineEdit1,LineEdit2,LineEdit3,TextEdit):
        if LineEdit1.text() == '':
            QMessageBox.information(self, "提示", "选择待提取的图片！")
            return
        if LineEdit2.text() == '':
            QMessageBox.information(self, "提示", "选择要存储到哪里！")
            return
        if LineEdit3.text() == '':
            QMessageBox.information(self, "提示", "请输入待提取文本的长度！")
            return
        
        imgPath = LineEdit1.text()
        _, ext = os.path.splitext(imgPath)
        if ext.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            if imghdr.what(imgPath) == None:
                QMessageBox.information(self, "提示", "输入不是一个图片！")
                return
        else:
            QMessageBox.information(self, "提示", "输入不是一个图片！")
            return
        
        output_path = LineEdit2.text()
        len_wm = LineEdit3.text()
        
        thread = GetTextThread(imgPath, len_wm, output_path)
        thread.taskFinished.connect(self.GetText_finished)  # 当任务完成时，关闭对话框
        thread.start()
        
        self.messageBox = QMessageBox()
        self.messageBox.setText("正在提取...")
        self.messageBox.setStandardButtons(QMessageBox.NoButton)  # 不显示任何标准按钮
        self.messageBox.show()  # 显示对话框
        
    def GetText_finished(self,wm_extract):
        self.ui.textEdit_37.setText(wm_extract)
        self.messageBox.accept()  # 关闭对话框
        
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    MainWindow = MyMainWindow()  # 创建主窗口
    MainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 在主线程中退出
