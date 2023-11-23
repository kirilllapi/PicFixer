from django.db import models
import numpy as np
from PIL import Image, ImageOps
import os
from math import *
import shutil
from io import BytesIO
from django.core.files.base import ContentFile
import cv2
# Create your models here.

class UploadFiles(models.Model):
    file = models.ImageField(upload_to='uploads_model')
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        pil_img = Image.open(self.file)
        pil_img = pil_img.convert('L')
        img = np.array(pil_img)
        G_x = ([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])  # Оператор Собеля по горизонтали
        G_y = ([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])  # Оператор Собеля по вертикали

        # Задаем количество строк и столбцов
        rows = np.size(img, 0)
        columns = np.size(img, 1)

        # Заполняем клонированное изображение (матрицу) нулями
        mag = np.zeros(img.shape)
        print('load...')
        # Выполнение производной по вертикали и горизонтали
        for i in range(0, rows - 2):
            for j in range(0, columns - 2):
                v = sum(sum(G_x * img[i:i + 3, j:j + 3]))
                h = sum(sum(G_y * img[i:i + 3, j:j + 3]))
                mag[i + 1, j + 1] = np.sqrt((v * v) + (h * h))  # Результирующая матрица изображения
                contrast = 70
                inter = mag[i, j]
                if inter < contrast:
                    mag[i, j] = 0
        #     # Задаем порог контрастности изображения
        # for i in range(0, rows):
        #     for j in range(0, columns):
        #         if mag[i, j] < contrast:
        #             mag[i, j] = 0
        path = 'static/main/img/portfolio'
        cv2.imwrite(os.path.join(path, 'sobel_result.jpg'), mag)

class UploadFiles_M(models.Model):
    file = models.ImageField(upload_to='uploads_model')
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        # Фильтрует изображение при помощи медианного фильтра
        inImage = Image.open(self.file)
        inImage = ImageOps.grayscale(inImage)
        imageMatr = np.array(inImage)

        ver = len(imageMatr)  # Вертикальный размер изображения (в пикселях)
        hor = len(imageMatr[0])  # Горизонтальный размер изображения (в пикселях)

        zeroRow = np.array([0] * (hor + 2))  # Строка длины hor, содержащая нули

        # Дополнение нулями
        imageMatr = np.insert(imageMatr, (0, hor), 0, axis=1)
        imageMatr = np.vstack([zeroRow, imageMatr])
        imageMatr = np.vstack([imageMatr, zeroRow])

        # Наложение маски и формирование медианной матрицы
        medianMatr = np.array([[0] * hor for _ in range(ver)])  # Медианная матрица (изначально нулевая)
        for row in range(1, ver + 1):
            for el in range(1, hor + 1):
                boxMatr = np.array([[imageMatr[row - 1][el - 1], imageMatr[row - 1][el], imageMatr[row - 1][el + 1]],
                                    [imageMatr[row][el - 1], imageMatr[row][el], imageMatr[row][el + 1]],
                                    [imageMatr[row + 1][el - 1], imageMatr[row + 1][el], imageMatr[row + 1][el + 1]]])
                boxMatr = sorted(boxMatr.reshape(-1))  # Преобразуем матрицу в вектор-строку и сортируем
                median = boxMatr[4]  # Медианой является пятый элемент
                medianMatr[row - 1][el - 1] = median

        #outImage = Image.fromarray(medianMatr)
        path = 'static/main/img/portfolio'
        cv2.imwrite(os.path.join(path, 'median_result.jpg'), medianMatr)


class UploadFiles_B(models.Model):
    file = models.ImageField(upload_to='uploads_model')
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        def gaussian_func_spatial(m, n):
            # Гауссианская функция для дальности пикселя; сигма = 2
            return exp(-(m ** 2 + n ** 2) / 8) / (8 * pi)

        def gaussian_func_brightness(k, sgm):
            # Гауссианская функция для контрастности пикселя
            return exp(-(1 / 2) * (k ** 2 / sgm ** 2)) / (sgm * sqrt(2 * pi))

        inImage = Image.open(self.file)

        inImage = ImageOps.grayscale(inImage)
        imageMatr = np.array(inImage)

        ver = len(imageMatr)  # Вертикальный размер изображения в пикселях
        hor = len(imageMatr[0])  # Горизонтальный размер изображения в пикселях

        zeroRow = np.array([0] * (hor + 12))  # Строка-заглушка, содержащая нули

        # Дополнение нулями
        imageMatr = np.insert(imageMatr, (0, hor), 0, axis=1)
        imageMatr = np.insert(imageMatr, (0, hor), 0, axis=1)
        imageMatr = np.insert(imageMatr, (0, hor), 0, axis=1)
        imageMatr = np.insert(imageMatr, (0, hor), 0, axis=1)
        imageMatr = np.insert(imageMatr, (0, hor), 0, axis=1)
        imageMatr = np.insert(imageMatr, (0, hor), 0, axis=1)
        imageMatr = np.vstack([zeroRow, zeroRow, zeroRow, zeroRow, zeroRow, zeroRow, imageMatr])
        imageMatr = np.vstack([imageMatr, zeroRow, zeroRow, zeroRow, zeroRow, zeroRow, zeroRow])

        # Наложение маски и формирование билатеральной матрицы
        bilateralMatr = np.array([[0] * hor for _ in range(ver)])  # Билатеральная матрица (изначально нулевая)
        for row in range(6, ver + 6):
            for el in range(6, hor + 6):
                w = 0  # Вес
                sum_boxMatr = 0  # Сумма пикселей вокруг
                for m in range(13):
                    for n in range(13):
                        stride_weight = gaussian_func_spatial(m, n) * gaussian_func_brightness(
                            (imageMatr[row - 6 + m][el - 6 + n] - imageMatr[row][el]), 140)
                        w += stride_weight
                        sum_boxMatr += imageMatr[row - 6 + m][el - 6 + n] * stride_weight

                target = sum_boxMatr // w  # Взвешенная сумма пикселей - новое значение
                bilateralMatr[row - 6][el - 6] = target

        # outImage = Image.fromarray(bilateralMatr)
        # outImage = ImageOps.grayscale(outImage)
        path = 'static/main/img/portfolio'
        cv2.imwrite(os.path.join(path, 'bil_result.jpg'), bilateralMatr)



