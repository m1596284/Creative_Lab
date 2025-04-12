class Restaurant:
    """餐廳類 - 方法類型示例"""

    # 類變數/屬性
    restaurant_count = 0

    def __init__(self, name, cuisine):
        """初始化餐廳 (實例方法)"""
        # 實例變數/屬性
        self.name = name
        self.cuisine = cuisine
        self.is_open = False
        self.customers = 0

        # 更新餐廳計數
        Restaurant.restaurant_count += 1

    # 實例方法 - 需要訪問和修改特定實例的數據
    def open_restaurant(self):
        """開門營業 (實例方法)"""
        # 使用 self 訪問和修改實例的屬性
        if not self.is_open:
            self.is_open = True
            print(f"{self.name} 餐廳現在開門營業！")
        else:
            print(f"{self.name} 餐廳已經在營業中。")

    def serve_customer(self, count):
        """服務顧客 (實例方法)"""
        if self.is_open:
            self.customers += count
            print(f"{self.name} 餐廳現已服務 {self.customers} 位顧客。")
        else:
            print(f"{self.name} 餐廳尚未開門，無法服務顧客。")

    # 靜態方法 - 獨立功能，不需要訪問實例或類
    @staticmethod
    def convert_currency(amount, rate):
        """貨幣轉換工具 (靜態方法)
        不需要訪問實例或類的數據，純工具函數
        """
        return amount * rate

    @staticmethod
    def validate_cuisine(cuisine_type):
        """驗證菜系是否有效 (靜態方法)
        不需要訪問實例或類的數據
        """
        valid_cuisines = ['義式', '中式', '日式', '美式', '法式']
        return cuisine_type in valid_cuisines

    # 類方法 - 操作類本身的數據，而非特定實例
    @classmethod
    def get_restaurant_count(cls):
        """獲取餐廳總數 (類方法)
        訪問類變數，而非實例變數
        """
        return cls.restaurant_count

    @classmethod
    def create_franchise(cls, city):
        """創建連鎖店 (類方法)
        使用類作為工廠創建新實例
        """
        franchise_name = f"{city}分店"
        return cls(franchise_name, "連鎖特色料理")


# 使用方法
if __name__ == "__main__":
    print("===== 實例方法示例 =====")
    restaurant = Restaurant("小熊餐廳", "中式")
    restaurant.open_restaurant()  # 實例方法：需要特定餐廳的數據
    restaurant.serve_customer(5)  # 實例方法：操作特定餐廳的狀態

    print("\n===== 靜態方法示例 =====")
    # 可通過類調用，無需創建實例
    price_usd = 20
    price_twd = Restaurant.convert_currency(price_usd, 31.5)
    print(f"${price_usd} 美元 = ${price_twd} 台幣")

    # 驗證菜系
    cuisine = "義式"
    is_valid = Restaurant.validate_cuisine(cuisine)
    print(f"'{cuisine}' 是有效的菜系嗎? {is_valid}")

    # 靜態方法也可以通過實例調用，但不常見
    print(f"通過實例調用：${price_usd} 美元 = ${restaurant.convert_currency(price_usd, 31.5)} 台幣")

    print("\n===== 類方法示例 =====")
    # 獲取總餐廳數（通過類調用）
    count = Restaurant.get_restaurant_count()
    print(f"目前總共有 {count} 家餐廳")

    # 使用工廠方法創建新實例
    taipei_restaurant = Restaurant.create_franchise("台北")
    print(f"新開了 {taipei_restaurant.name}，菜系是 {taipei_restaurant.cuisine}")

    # 再次檢查餐廳數量
    print(f"現在總共有 {Restaurant.get_restaurant_count()} 家餐廳")
