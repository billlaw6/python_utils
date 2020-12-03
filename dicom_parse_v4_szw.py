#!/usr/bin/env python
# -*- coding: utf8 -*-

import os #使用下面的自动读取路径下文加名，需要加上
from PIL import Image
import numpy as np
import SimpleITK as STK
import pydicom
import sys #不加这个无法使用opencv
sys.path.append('C:\\Users\\zhong\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages')
import cv2
import xlwt


Read_Path = 'E:\\CT coronary extraction'
Write_Path = 'E:\\ComplexDicomReadTest'
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
    #HeadInfo = []      #建立一个空的list对象存放所有dicom header info
    switch = 0  #当图像是灰度图而不是彩色，并且有overlay数据时，因为要扩充为rgb3维数据color，
    # 而且无法赋值给img_array[0/j]=color,因为整个矩阵不可能改变维度，所以用switch来标识是否
    # 直接cv2.imwrite(Image_path, color_img)，是的话switch =1，否则为0，证明灰度图无overlay数据，
    #常规写入cv2.imwrite(Image_path, img_array[0/j])即可
    if "PatientName" in Dicom_Head:             #从这里开始提取各种需要的参数，缺失的补充为NA
        PatientName = str(Dicom_Head.PatientName)
    else:
        PatientName = "NA"
    if "PatientID" in Dicom_Head:
        PatientID = str(Dicom_Head.PatientID)
    else:
        PatientID = "NA"
    if "PatientBirthDate" in Dicom_Head:
        PatientBirthDate = str(Dicom_Head.PatientBirthDate)
    else:
        PatientBirthDate = "NA"
    if "PatientSex" in Dicom_Head:
        PatientSex = str(Dicom_Head.PatientSex)
    else:
        PatientSex = "NA"
    if "StudyDate" in Dicom_Head:
        StudyDate = str(Dicom_Head.StudyDate)
    else:
        StudyDate = "NA"
    if "InstitutionName" in Dicom_Head:
        InstitutionName = str(Dicom_Head.InstitutionName)
    else:
        InstitutionName = "NA"
    if "StudyID" in Dicom_Head:
        StudyID = str(Dicom_Head.StudyID)
    else:
        StudyID = "NA"
    if "StudyInstanceUID" in Dicom_Head:
        StudyInstanceUID = str(Dicom_Head.StudyInstanceUID)
    else:
        StudyInstanceUID = PatientName + PatientID + StudyID + StudyDate   #注意最终显示的病例是按StudyInstanceUID
                                                # 来区分的，如果这个值缺失，按照这样的补全补上，否则无法提取jpg图片
    if "SeriesNumber" in Dicom_Head:
        SeriesNumber = str(Dicom_Head.SeriesNumber)
    else:
        SeriesNumber = "NA"
    if "SeriesInstanceUID" in Dicom_Head:
        SeriesInstanceUID_full = str(Dicom_Head.SeriesInstanceUID)
    else:
        SeriesInstanceUID_full = "00000" + SeriesNumber   #注意最终显示的序列是按SeriesInstanceUID
                                   # 来写文件夹单独显示块的，如果这个值缺失，用SeriesNumber补上,为了保证长度，加5个0
    if "InstanceNumber" in Dicom_Head:
        InstanceNumber = str(Dicom_Head.InstanceNumber)
    else:
        InstanceNumber = "NA"
    if "RecommendedDisplayFrameRate" in Dicom_Head:
        RecommendedDisplayFrameRate = str(Dicom_Head.RecommendedDisplayFrameRate)
    else:
        RecommendedDisplayFrameRate = "NA"
    if "WindowCenter" in Dicom_Head:
        if type(Dicom_Head.WindowCenter) == pydicom.multival.MultiValue : #比较坑人的是窗框床位居然有是数组的，比如例子CT
            #如果是这种类型，去数组的[0]就是窗框窗位值
            WindowCenter = str(Dicom_Head.WindowCenter[0])
        else:
            WindowCenter = str(Dicom_Head.WindowCenter)
    else:
        WindowCenter = "NA"
    if "WindowWidth" in Dicom_Head:
        if type(Dicom_Head.WindowWidth) == pydicom.multival.MultiValue :
            WindowWidth = str(Dicom_Head.WindowWidth[0])
        else:
            WindowWidth = str(Dicom_Head.WindowWidth)
    else:
        WindowWidth = "NA"
    if "Modality" in Dicom_Head:
        Modality = str(Dicom_Head.Modality)
    else:
        Modality = "NA"

    #用extend方法把信息一次加进来
    #HeadInfo.extend([PatientName,PatientID,PatientBirthDate,PatientSex,StudyDate,InstitutionName,StudyID,StudyInstanceUID,SeriesNumber,InstanceNumber,RecommendedDisplayFrameRate])
    Write_Path_Folder_StudyInstanceUID = Write_Path + PatientName + "_" + Modality + "_" + StudyInstanceUID    #第一分类标准为StudyInstanceUID，
                               # 如果写入路径下没有这个文件夹，则建立一个这个名字的文件夹，存放所有这个study的图片
    ifexist_1 = os.path.exists(Write_Path_Folder_StudyInstanceUID)
    if not ifexist_1 :
        os.makedirs(Write_Path_Folder_StudyInstanceUID)

    #建立了StudyInstanceUID文件夹后，把dicom header的信息写入xls文件存在该目录下，每个信息换一行
    DicomInfoFile_Path = Write_Path_Folder_StudyInstanceUID + "\\" + PatientName + "_" + Modality + "_" + StudyInstanceUID + "_DicomInfo.xls"
    ifexist_2 = os.path.exists(DicomInfoFile_Path)
    if not ifexist_2 :
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet('dicom_information', cell_overwrite_ok=True)
        sheet.write(0, 0, PatientName)
        sheet.write(1, 0, PatientID)
        sheet.write(2, 0, PatientBirthDate)
        sheet.write(3, 0, PatientSex)
        sheet.write(4, 0, StudyDate)
        sheet.write(5, 0, InstitutionName)
        #sheet.write(6, 0, StudyID)
        #sheet.write(7, 0, StudyInstanceUID)
        #sheet.write(8, 0, SeriesNumber)
        #sheet.write(9, 0, InstanceNumber)
        #sheet.write(10, 0, RecommendedDisplayFrameRate)
        #sheet.write(11, 0, WindowCenter)
        #sheet.write(12, 0, WindowWidth)
        #sheet.write(13, 0, Modality)
        book.save(DicomInfoFile_Path)

    SeriesInstanceUID = SeriesInstanceUID_full[-6:-1] #避免文件名太长无法成功创建文件夹

    # 第二分类标准为SeriesNumber，如果StudyInstanceUID文件夹下没有这么一个文件夹，则建立一个，存储同一序列的jpg图片
    Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID = Write_Path_Folder_StudyInstanceUID + "\\" + SeriesInstanceUID
    ifexist_3 = os.path.exists(Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID)
    if not ifexist_3 :
        os.makedirs(Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID)

    #同时要建立一个compress文件夹，存放compress后的普通片
    Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID_Compress = Write_Path_Folder_StudyInstanceUID + "\\" + SeriesInstanceUID + "_Compress"
    ifexist_4 = os.path.exists(Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID_Compress)
    if not ifexist_4 :
        os.makedirs(Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID_Compress)

    #用STK读入dicom文件的图片矩阵


    img_series = STK.ReadImage(Dicom_FileName[i])
    img_array = STK.GetArrayFromImage(img_series)


    Image_Number = int(img_array.shape[0])
    #对于只有一副图的dicom文件，说明其属于多个dicom文件构成一个序列的情况，其必有InstanceNumber，则以
    #StudyInstanceUID + "_" + SeriesNumber + "_" + InstanceNumber + ".jpg"的方式命名
    #而后在Write_Path_Folder_StudyInstanceUID_SeriesNumber和Write_Path_Folder_StudyInstanceUID_SeriesNumber_Compress
    #文件夹下分别写入高质量和压缩图片

    if Image_Number == 1 : #如果一个dicom文件里只有一张图，说明属于第一种情况：多幅图构成一个序列的，这些图之间
        #依靠InstanceNumber来区分先后顺序，因此图片的命名方式为：
        # StudyInstanceUID + "_" + SeriesNumber + "_" + InstanceNumber + ".jpg"
        Image_name = StudyInstanceUID + "_" + SeriesInstanceUID + "_" + InstanceNumber + ".jpg"
        Image_path = Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID + "\\" + Image_name
        Image_path_compress = Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID_Compress + "\\" + Image_name
        # 如果dicom head 含有窗宽窗位信息，用自己写的函数调节窗宽窗位--ISK的函数不靠谱啊，彩色影像如果含有窗宽窗位怎么办
        #就是下面if len(img_array[j].shape) == 3，这种应该没有窗框窗位把，不然三色怎么调节？但是如那个金色的报告呢
        #用TianKeng来转换uint16成float32（注意是双边，32才能保证对接），uint*255避免溢出的错误
        if WindowCenter != "NA" and WindowWidth != "NA":
            c = int(WindowCenter)
            w = int(WindowWidth)
            min = c - w / 2
            uint2float = np.float32(img_array[0])
            uint2float = uint2float - min
            uint2float = uint2float * (255/w)
            uint2float[uint2float < 0] = 0
            uint2float[uint2float > 255] = 255
            img_array[0] = np.uint16(uint2float)

        #用cv2的imwrite写入高质量图片
        #填补上opencv里面BGR2RBG的坑,但要注意，其实img_array[0]有512,512的灰度图，还有512,512,3的彩色图---还有1024的天哪哈哈哈
        if len(img_array[0].shape) == 3: #对于dicom解析出的图为彩色图的，要进行BGR2RGB的转化，不然存的时候颜色不对
            imgBGR2RGB = cv2.cvtColor(img_array[0], cv2.COLOR_BGR2RGB)
            try: #对彩色通用测试是否有overlay信息，如果有，就将overlay信息用黄色替换图片中相应的像素值
                overlay_data = Dicom_Head[0x60003000].value
                rows = Dicom_Head[0x60000010].value
                cols = Dicom_Head[0x60000011].value
                overlay_frames = Dicom_Head[0x60000015].value
                overlay_type = Dicom_Head[0x60000040].value
                bits_allocated = Dicom_Head[0x60000100].value
                overlay_origin = Dicom_Head[0x60000050].value

                np_dtype = np.dtype('uint8')
                length_of_pixel_array = len(overlay_data)
                expected_length = rows * cols

                if bits_allocated == 1:
                    expected_bit_length = expected_length
                    expected_length = int(expected_length / 8) + (expected_length % 8 > 0)

                    bit = 0
                    arr = np.ndarray(shape=(length_of_pixel_array * 8), dtype=np_dtype)

                    for byte in overlay_data:
                        for bit in range(bit, bit + 8):
                            arr[bit] = byte & 1
                            byte >>= 1
                        bit += 1

                    arr = arr[:expected_bit_length]

                if overlay_frames == 1:
                    arr = arr.reshape(rows, cols)

                # 自定义的金色描述标注信息
                imgBGR2RGB[np.where(arr != 0)] = [120, 251, 251]

            except KeyError:
                print("No Overlay Data in Dicom File")
            cv2.imwrite(Image_path, imgBGR2RGB)
        else:
            try: #如果dicom解析出的图示灰度图，又有overlay信息的，先要将图片转化为彩色图，再标注，否则
                #标注出的是255纯白色的，无法与图像原组织区分开（如果原组织也是白色）
                overlay_data = Dicom_Head[0x60003000].value
                rows = Dicom_Head[0x60000010].value
                cols = Dicom_Head[0x60000011].value
                overlay_frames = Dicom_Head[0x60000015].value
                overlay_type = Dicom_Head[0x60000040].value
                bits_allocated = Dicom_Head[0x60000100].value
                overlay_origin = Dicom_Head[0x60000050].value

                np_dtype = np.dtype('uint8')
                length_of_pixel_array = len(overlay_data)
                expected_length = rows * cols

                if bits_allocated == 1:
                    expected_bit_length = expected_length
                    expected_length = int(expected_length / 8) + (expected_length % 8 > 0)

                    bit = 0
                    arr = np.ndarray(shape=(length_of_pixel_array * 8), dtype=np_dtype)

                    for byte in overlay_data:
                        for bit in range(bit, bit + 8):
                            arr[bit] = byte & 1
                            byte >>= 1
                        bit += 1

                    arr = arr[:expected_bit_length]

                if overlay_frames == 1:
                    arr = arr.reshape(rows, cols)
                color_img = cv2.cvtColor(img_array[0], cv2.COLOR_GRAY2BGR)
                color_img[np.where(arr != 0)] = [120, 251, 251]
                cv2.imwrite(Image_path, color_img)
                switch = 1
            except KeyError:
                print("No Overlay Data in Dicom File")

            if switch == 0:
                cv2.imwrite(Image_path, img_array[0])
        # 用PLI的image.save写入压缩片
        Compress_Image = Image.open(Image_path)
        Compress_Image.save(Image_path_compress, optimize=True, quality=10)
    else : #一个dicom文件里有不止一幅图，说明属于第二种情况，这个dicom文件本身就是一个序列，以图片在序列里的
        #顺序给图片命名（因为这时没有instance number或者这些图instance number都是一样的），命名方式为：
        #Image_name = StudyInstanceUID + "_" + SeriesNumber + "_" + str(j) + ".jpg"
        for j in range(Image_Number):    #一个dicom含有多张图像的，就用其排布的图片顺序依次命名
            Image_name = StudyInstanceUID + "_" + SeriesInstanceUID + "_" + str(j) + ".jpg"
            Image_path = Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID + "\\" + Image_name
            Image_path_compress = Write_Path_Folder_StudyInstanceUID_SeriesInstanceUID_Compress + "\\" + Image_name

            if WindowCenter != "NA" and WindowWidth != "NA":
                c = int(WindowCenter)
                w = int(WindowWidth)
                min = c - w / 2
                uint2float = np.float32(img_array[j])
                uint2float = uint2float - min
                uint2float = uint2float * (255 / w)
                uint2float[uint2float < 0] = 0
                uint2float[uint2float > 255] = 255
                img_array[j] = np.uint16(uint2float)

            if len(img_array[j].shape) == 3:
                imgBGR2RGB = cv2.cvtColor(img_array[j], cv2.COLOR_BGR2RGB)
                try:
                    overlay_data = Dicom_Head[0x60003000].value
                    rows = Dicom_Head[0x60000010].value
                    cols = Dicom_Head[0x60000011].value
                    overlay_frames = Dicom_Head[0x60000015].value
                    overlay_type = Dicom_Head[0x60000040].value
                    bits_allocated = Dicom_Head[0x60000100].value
                    overlay_origin = Dicom_Head[0x60000050].value

                    np_dtype = np.dtype('uint8')
                    length_of_pixel_array = len(overlay_data)
                    expected_length = rows * cols

                    if bits_allocated == 1:
                        expected_bit_length = expected_length
                        expected_length = int(expected_length / 8) + (expected_length % 8 > 0)

                        bit = 0
                        arr = np.ndarray(shape=(length_of_pixel_array * 8), dtype=np_dtype)

                        for byte in overlay_data:
                            for bit in range(bit, bit + 8):
                                arr[bit] = byte & 1
                                byte >>= 1
                            bit += 1

                        arr = arr[:expected_bit_length]

                    if overlay_frames == 1:
                        arr = arr.reshape(rows, cols)

                    imgBGR2RGB[np.where(arr != 0)] = [120, 251, 251]
                except KeyError:
                    print("No Overlay Data in Dicom File")
                cv2.imwrite(Image_path, imgBGR2RGB)
            else:
                try:
                    overlay_data = Dicom_Head[0x60003000].value
                    rows = Dicom_Head[0x60000010].value
                    cols = Dicom_Head[0x60000011].value
                    overlay_frames = Dicom_Head[0x60000015].value
                    overlay_type = Dicom_Head[0x60000040].value
                    bits_allocated = Dicom_Head[0x60000100].value
                    overlay_origin = Dicom_Head[0x60000050].value

                    np_dtype = np.dtype('uint8')
                    length_of_pixel_array = len(overlay_data)
                    expected_length = rows * cols

                    if bits_allocated == 1:
                        expected_bit_length = expected_length
                        expected_length = int(expected_length / 8) + (expected_length % 8 > 0)

                        bit = 0
                        arr = np.ndarray(shape=(length_of_pixel_array * 8), dtype=np_dtype)

                        for byte in overlay_data:
                            for bit in range(bit, bit + 8):
                                arr[bit] = byte & 1
                                byte >>= 1
                            bit += 1

                        arr = arr[:expected_bit_length]

                    if overlay_frames == 1:
                        arr = arr.reshape(rows, cols)
                    color_img = cv2.cvtColor(img_array[j], cv2.COLOR_GRAY2BGR)
                    color_img[np.where(arr != 0)] = [120, 251, 251]
                    cv2.imwrite(Image_path, color_img)
                    switch = 1

                except KeyError:
                    print("No Overlay Data in Dicom File")
                if switch == 0:
                    cv2.imwrite(Image_path, img_array[j])
            # 用PLI的image.save写入压缩片
            Compress_Image = Image.open(Image_path)
            Compress_Image.save(Image_path_compress, optimize=True, quality=10)
