import cv2
import numpy as np

capture = cv2.VideoCapture(r"C:\Users\BY-FARIKS\OneDrive\Рабочий стол\pythonn\videoplayback.mp4")

# Параметры вращения
angle = 0  # Начальный угол
rotation_speed = 0.01  # Скорость увеличения угла (уменьшите для медленного вращения)

while capture.isOpened():
    ret, frame = capture.read()

    if not ret:
        break

    # Настройка ширины и высоты окна
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cv2.namedWindow('Result', cv2.WINDOW_NORMAL)

    # Определяем размеры кадра
    height, width = frame.shape[:2]

    # Центр кадра
    center_x, center_y = width // 2, height // 2

    # Смещение вершин для эффекта вращения
    offset_x = int(300 * np.sin(angle))
    offset_y = int(100 * np.cos(angle))

    # Перспективное преобразование для имитации 3D-поворота
    src_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    dst_points = np.float32([[offset_x, offset_y],
                             [width - offset_x, offset_y],
                             [width - offset_x, height - offset_y],
                             [offset_x, height - offset_y]])

    # Построение матрицы перспективного преобразования
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Применение перспективного преобразования
    rotated_frame = cv2.warpPerspective(frame, matrix, (width, height))

    # Преобразование кадра в оттенки серого
    gray_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2GRAY)

    # Показ результата
    cv2.imshow('Result', gray_frame)
    cv2.resizeWindow('Result', 1920, 1080)

    # Увеличение угла для плавного вращения
    angle += rotation_speed  # Увеличиваем угол на каждый кадр

    # Выход из цикла при нажатии 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
capture.release()
cv2.destroyAllWindows()
