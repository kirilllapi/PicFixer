import numpy as np
import shutil
import cv2
import os
os.startfile(r'C:/Users/User/Desktop/Радик/Practic/mysite/main/img.jpg')
shutil.copy(
    os.path.join('C:/Users/User/Desktop/Радик/Practic/mysite/uploads/', 'img.jpg'),
    os.path.join('C:/Users/User/Desktop/Радик/Practic/mysite/main'))


def method(a):
    print(a)
    contrast = 70
    blur = (1, 1)
    img_for_blur = cv2.imread('img.jpg', 0)  # Сохраняем изображение в ч/б
    img = img_for_blur  # Используем фильтр размытия по Гауссу
    print('Вывод:',img)
    G_x = ([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])  # Оператор Собеля по горизонтали
    G_y = ([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])  # Оператор Собеля по вертикали

    # Задаем количество строк и столбцов
    rows = np.size(img, 0)
    columns = np.size(img, 1)

    # Заполняем клонированное изображение (матрицу) нулями
    mag = np.zeros(img.shape)

    # Выполнение производной по вертикали и горизонтали
    for i in range(0, rows - 2):
        for j in range(0, columns - 2):
            v = sum(sum(G_x * img[i:i + 3, j:j + 3]))
            h = sum(sum(G_y * img[i:i + 3, j:j + 3]))
            mag[i + 1, j + 1] = np.sqrt((v * v) + (h * h))  # Результирующая матрица изображения

        # Задаем порог контрастности изображения
    for i in range(0, rows):
        for j in range(0, columns):
            if mag[i, j] < contrast:
                mag[i, j] = 0

    # #Вывод результирующего изображения
    # img_show(mag)
    # Сохраним преобразованное изображение
    cv2.imwrite('sobel.jpg', mag)
    shutil.copy(
        os.path.join('C:/Users/User/Desktop/Радик/Practic/mysite/main', 'sobel.jpg'),
        os.path.join('C:/Users/User/Desktop/Радик/Practic/mysite/uploads/'))
    os.remove(os.path.join('C:/Users/User/Desktop/Радик/Practic/mysite/main', 'sobel.jpg'))
    os.remove(os.path.join('C:/Users/User/Desktop/Радик/Practic/mysite/main', 'img.jpg'))
