import numpy as np
from PySide6.QtGui import  QImage

def prepare_for_qt(arr: np.ndarray) -> QImage:
    arr_disp = arr.astype(np.float32)
    arr_disp -= arr_disp.min()
    arr_disp /= arr_disp.max()
    arr_disp *= 65535
    arr_disp = arr_disp.astype(np.uint16)

    h, w = arr.shape
    return QImage(
        arr_disp.data,
        w, h,
        w * 2,
        QImage.Format_Grayscale16
    )
