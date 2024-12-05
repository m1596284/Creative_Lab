import cv2
import time
from datetime import datetime

# 替換成你的RTSP網址
rtsp_url = 'rtsp://m1596284:t1596284@220.135.139.235:8554/stream1'

# 建立VideoCapture物件
video = cv2.VideoCapture(rtsp_url)

# 設定影像儲存路徑
folder_path = '/home/qma/coding_program/Creative_Lab/test_area/monitor_test'


# 檢查是否成功開啟影片
if not video.isOpened():
    print("無法開啟RTSP串流")
    exit()

# 逐幀處理
count = 0
while True:
    # 每10秒儲存一張圖片
    print(count)
    if count % 10 == 0:
        count = 0
        status, frame = video.read()
        print(status)
        try:
            if not status:
                while status is False:
                    print("無法擷取畫面")
                    video.release()
                    cv2.destroyAllWindows()
                    video = cv2.VideoCapture(rtsp_url)
                    status, frame = video.read()
            save_path = f"{folder_path}/{datetime.now().strftime('%m%d_%H%M%S')}.jpg"
            cv2.imwrite(save_path, frame)
            print(f"已儲存圖片: {save_path}")
        except Exception as e:
            print(f"錯誤: {e}")
            pass
    count += 1
    # 等待1秒 (可調整擷取頻率)
    time.sleep(1)
