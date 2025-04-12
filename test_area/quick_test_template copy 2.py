# 基本裝飾器示例


def timer_decorator(func):
    """計時裝飾器：計算函數執行時間"""
    import time

    def wrapper(*args, **kwargs):
        # 裝飾器增強功能：開始計時
        start_time = time.time()

        # 執行原始函數
        result = func(*args, **kwargs)

        # 裝飾器增強功能：結束計時並輸出時間
        end_time = time.time()
        print(f"函數 {func.__name__} 執行時間: {end_time - start_time:.4f} 秒")

        # 返回原始函數的結果
        return result

    return wrapper


# 使用裝飾器語法
@timer_decorator
def process_data(data):
    """處理資料的函數，被裝飾器增強了"""
    import time

    time.sleep(5)  # 模擬耗時操作
    result = data * 2
    return result


# 等同於以下寫法:
# process_data = timer_decorator(process_data)

# 調用裝飾後的函數
result = process_data(5)
print(f"處理結果: {result}")
