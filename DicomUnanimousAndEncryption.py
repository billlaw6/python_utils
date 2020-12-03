#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import print_function
import os #使用下面的自动读取路径下文加名，需要加上
from PIL import Image
import numpy as np
import SimpleITK as STK
import pydicom
from pydicom.data import get_testdata_files
import sys #不加这个无法使用opencv
#sys.path.append('C:\\Users\\zhong\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages')
import xlwt
import xlrd
import xlutils
import xlutils.copy
from Crypto.Hash import SHA256



Read_Path = 'E:\\DicomUnanimousTestData'
DicomInfoFile_Path = "E:\\DicomInfo.xls"
#Read_Path = 'E:\\IMG-0002-00029.dcm'
Dicom_FileName = []
for fpathe, dirs, fs in os.walk(Read_Path):   #遍历找出路径下的所有文件，并在list中写出所有文件绝对读路径
    for f in fs:
        Each_File_Name = os.path.join(fpathe, f)     #当前遍历到的这个文件的文件名
        Each_File_Handle = open(Each_File_Name, "rb")     #以字节方式读这个文件
        Each_File_Handle.seek(128, 0)        #指针偏移128
        DICOM_ORNOT = Each_File_Handle.read(4)    #读取4个字节，也就是128,129,139,131这4个自己
        if DICOM_ORNOT[0] == 68 and DICOM_ORNOT[1] == 73 and DICOM_ORNOT[2] == 67 and DICOM_ORNOT[3] == 77:
            #判断这4个字节是否为大写的DICM，如果是文件为dicom文件，文件名加入dicom列表
            Dicom_FileName.append(os.path.join(fpathe, f))



for i in range(len(Dicom_FileName)):           #对遍历出来的每个dicom文件
    Dicom_Head = pydicom.dcmread(Dicom_FileName[i])       #读取头文件信息
    if "PatientName" in Dicom_Head:  # 从这里开始提取各种需要的参数，缺失的补充为NA
        PatientName = str(Dicom_Head.PatientName)
        Dicom_Head.data_element("PatientName").value = 'anonymous'
    else:
        PatientName = "NA"
    if "PatientID" in Dicom_Head:
        PatientID = str(Dicom_Head.PatientID)
        Dicom_Head.data_element("PatientID").value = '000000'
    else:
        PatientID = "NA"
    if "PatientBirthDate" in Dicom_Head:
        PatientBirthDate = str(Dicom_Head.PatientBirthDate)
        Dicom_Head.data_element("PatientBirthDate").value = '19000101'
    else:
        PatientBirthDate = "NA"
    if "PatientSex" in Dicom_Head:
        PatientSex = str(Dicom_Head.PatientSex)
        Dicom_Head.data_element("PatientSex").value = 'O'
    else:
        PatientSex = "NA"
    if "StudyDate" in Dicom_Head:
        StudyDate = str(Dicom_Head.StudyDate)
        Dicom_Head.data_element("StudyDate").value = '19000101'
    else:
        StudyDate = "NA"
    if "AcquisitionDateTime" in Dicom_Head:
        AcquisitionDateTime = str(Dicom_Head.AcquisitionDateTime)
        Dicom_Head.data_element("AcquisitionDateTime").value = '000000'
    else:
        AcquisitionDateTime = "NA"
    if "InstitutionName" in Dicom_Head:
        InstitutionName = str(Dicom_Head.InstitutionName)
        Dicom_Head.data_element("InstitutionName").value = 'Unknown'
    else:
        InstitutionName = "NA"
    if "SeriesTime" in Dicom_Head:
        SeriesTime = str(Dicom_Head.SeriesTime)
        Dicom_Head.data_element("SeriesTime").value = '000000.000000'
    else:
        SeriesTime = "NA"
    if "AcquisitionTime" in Dicom_Head:
        AcquisitionTime = str(Dicom_Head.AcquisitionTime)
        Dicom_Head.data_element("AcquisitionTime").value = '000000.000000'
    else:
        AcquisitionTime = "NA"
    if "ContentTime" in Dicom_Head:
        ContentTime = str(Dicom_Head.ContentTime)
        Dicom_Head.data_element("ContentTime").value = '000000.000000'
    else:
        ContentTime = "NA"
    if "StudyDate" in Dicom_Head:
        StudyDate = str(Dicom_Head.StudyDate)
        Dicom_Head.data_element("StudyDate").value = '19000101'
    else:
        StudyDate = "NA"
    if "SeriesDate" in Dicom_Head:
        SeriesDate = str(Dicom_Head.SeriesDate)
        Dicom_Head.data_element("SeriesDate").value = '19000101'
    else:
        SeriesDate = "NA"
    if "AcquisitionDate" in Dicom_Head:
        AcquisitionDate = str(Dicom_Head.AcquisitionDate)
        Dicom_Head.data_element("AcquisitionDate").value = '19000101'
    else:
        AcquisitionDate = "NA"
    if "ContentDate" in Dicom_Head:
        ContentDate = str(Dicom_Head.ContentDate)
        Dicom_Head.data_element("ContentDate").value = '19000101'
    else:
        ContentDate = "NA"
    if "StudyID" in Dicom_Head:
        StudyID = str(Dicom_Head.StudyID)
        Dicom_Head.data_element("StudyID").value = '000000'
    else:
        StudyID = "NA"
    if "StudyInstanceUID" in Dicom_Head:
        StudyInstanceUID = str(Dicom_Head.StudyInstanceUID)
    else:
        StudyInstanceUID = PatientID + StudyID + StudyDate   #注意最终显示的病例是按StudyInstanceUID
                                                # 来区分的，如果这个值缺失，按照这样的补全补上，否则无法提取jpg图片
        #Dicom_Head.data_element("StudyInstanceUID").value = StudyInstanceUID
    if Dicom_FileName[-4:] == '.dcm' :
        Dicom_Head.save_as(Dicom_FileName[i][:-5] + '_Anonymous' + '.dcm')
    else :
        Dicom_Head.save_as(Dicom_FileName[i] + '_Anonymous' + '.dcm')


    hash = SHA256.new()
    key = bytes(StudyInstanceUID, encoding='utf8')
    hash.update(key)
    #Codes = hash.digest()
    Codes = hash.hexdigest()
    #print(Codes)
    #CodesString = str(Codes, 'utf-8')
    #CodesString = Codes.decode()


    XlsData = xlrd.open_workbook(DicomInfoFile_Path)
    XlsCopyData = xlutils.copy.copy(XlsData)
    Sheet1 = XlsData.sheet_by_index(0)
    ExistingRow = Sheet1.nrows
    Sheet1Copy = XlsCopyData.get_sheet(0)
    #Sheet1Copy.write(0, ExistingRow, CodesString)
    #Sheet1Copy.write(1, ExistingRow, 'PatientName')
    #Sheet1Copy.write(2, ExistingRow, 'PatientID')
    #Sheet1Copy.write(3, ExistingRow, 'PatientBirthDate')
    #Sheet1Copy.write(4, ExistingRow, 'PatientSex')
    #Sheet1Copy.write(5, ExistingRow, 'StudyDate')
    #Sheet1Copy.write(6, ExistingRow, 'AcquisitionDateTime')
    #Sheet1Copy.write(7, ExistingRow, 'InstitutionName')
    #Sheet1Copy.write(8, ExistingRow, 'SeriesTime')
    #Sheet1Copy.write(9, ExistingRow, 'AcquisitionTime')
    #Sheet1Copy.write(10, ExistingRow, 'ContentTime')
    #Sheet1Copy.write(11, ExistingRow, 'StudyDate')
    #Sheet1Copy.write(12, ExistingRow, 'SeriesDate')
    #Sheet1Copy.write(13, ExistingRow, 'AcquisitionDate')
    #Sheet1Copy.write(14, ExistingRow, 'ContentDate')
    #Sheet1Copy.write(15, ExistingRow, 'StudyID')
    #Sheet1Copy.write(16, ExistingRow, 'StudyInstanceUID')

    Sheet1Copy.write(ExistingRow, 0, Codes)
    Sheet1Copy.write(ExistingRow, 1, PatientName)
    Sheet1Copy.write(ExistingRow, 2, PatientID)
    Sheet1Copy.write(ExistingRow, 3, PatientBirthDate)
    Sheet1Copy.write(ExistingRow, 4, PatientSex)
    Sheet1Copy.write(ExistingRow, 5, StudyDate)
    Sheet1Copy.write(ExistingRow, 6, AcquisitionDateTime)
    Sheet1Copy.write(ExistingRow, 7, InstitutionName)
    Sheet1Copy.write(ExistingRow, 8, SeriesTime)
    Sheet1Copy.write(ExistingRow, 9, AcquisitionTime)
    Sheet1Copy.write(ExistingRow, 10, ContentTime)
    Sheet1Copy.write(ExistingRow, 11, StudyDate)
    Sheet1Copy.write(ExistingRow, 12, SeriesDate)
    Sheet1Copy.write(ExistingRow, 13, AcquisitionDate)
    Sheet1Copy.write(ExistingRow, 14, ContentDate)
    Sheet1Copy.write(ExistingRow, 15, StudyID)
    Sheet1Copy.write(ExistingRow, 16, StudyInstanceUID)
    XlsCopyData.save(DicomInfoFile_Path)
