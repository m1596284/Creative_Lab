import hashlib


def custom_urlencode(s):
    """
    自定義 URL 編碼函數，符合 ECPAY .NET 規則
    根據提供的編碼對照表進行轉換
    """
    encoding_map = {
        ' ': '+',  # space轉換為加號
        '!': '!',  # 保持原樣
        '"': '%22',
        '#': '%23',
        '$': '%24',
        '%': '%25',
        '&': '%26',
        "'": '%27',
        '(': '(',  # 保持原樣
        ')': ')',  # 保持原樣
        '*': '*',  # 保持原樣
        '+': '%2b',
        ',': '%2c',
        '/': '%2f',
        ':': '%3a',
        ';': '%3b',
        '<': '%3c',
        '=': '%3d',
        '>': '%3e',
        '?': '%3f',
        '@': '%40',
        '[': '%5b',
        '\\': '%5c',
        ']': '%5d',
        '^': '%5e',
        '`': '%60',
        '{': '%7b',
        '|': '%7c',
        '}': '%7d',
        '~': '%7e',
    }

    result = []
    for char in s:
        if char in encoding_map:
            result.append(encoding_map[char])
        elif ord(char) < 128:
            result.append(char)
        else:
            result.append('%{:02x}'.format(ord(char)))
    return ''.join(result)


# 設定參數
params = {
    "ChoosePayment": "Credit",
    "ClientBackURL": "https://csnc.com.tw/",
    "EncryptType": "1",
    "ItemName": "apple iphone 18",
    "MerchantID": "1190066",
    "MerchantTradeDate": "2025/02/22 14:31:22",
    "MerchantTradeNo": "marktest0101",
    "PaymentType": "aio",
    "ReturnURL": "https://hoyo.idv.tw/?a=Tools/EcPay&b=ReturnURL",
    "TotalAmount": "100",
    "TradeDesc": "my test from postman",
}

HashKey = "thUgweJIc6FiezjS"
HashIV = "vJq9FnLgkwYOOGiY"

# 步驟1: 將參數依照字母順序排序並用&串接
print("步驟1: 參數依照字母順序排序並串接")
sorted_params = sorted(params.items())
param_string = "&".join([f"{key}={value}" for key, value in sorted_params])
print(param_string)
print("\n")

# 步驟2: 加上HashKey和HashIV
print("步驟2: 加上HashKey和HashIV")
str_with_hash = f"HashKey={HashKey}&{param_string}&HashIV={HashIV}"
print(str_with_hash)
print("\n")

# 步驟3: 使用符合 ECPAY 規則的 URL encode
print("步驟3: 使用符合 ECPAY 規則的 URL encode")
url_encoded = custom_urlencode(str_with_hash)
print(url_encoded)
print("\n")

# 步驟4: 轉為小寫
print("步驟4: 轉為小寫")
lower_case = url_encoded.lower()
print(lower_case)
print("\n")

# 步驟5: SHA256加密
print("步驟5: SHA256加密")
sha256_hash = hashlib.sha256(lower_case.encode('utf-8')).hexdigest()
print(sha256_hash)
print("\n")

# 步驟6: 轉為大寫得到最終的CheckMacValue
print("步驟6: 轉為大寫得到最終的CheckMacValue")
check_mac_value = sha256_hash.upper()
print(check_mac_value)

# https://www.eggboy.com.tw/thank-you-page/
# 0179ed03-42e7-4375-845b-59c1b20ca18a?
# appSectionParams=%7B%22objectType%22%3A%22order%22%2C%22origin%22%3A%22checkout%22%7D


# https://www.eggboy.com.tw/checkout?appSectionParams={%22a11y%22%3Atrue%2C%22cartId%22%3A%22a55d09a4-429d-424c-9927-952ff04e219e%22%2C%22storeUrl%22%3A%22https%3A%2F%2Fwww.eggboy.com.tw%22%2C%22cashierPaymentId%22%3A%22%22%2C%22origin%22%3A%22shopping+cart%22%2C%22originType%22%3A%22addToCart%22%2C%22checkoutId%22%3A%225531edac-921f-4be3-a05e-dc68d005a2cc%22%2C%22isPreselectedFlow%22%3Afalse}&checkoutOOI=true

# https://www.eggboy.com.tw/checkout?appSectionParams=%7B%22a11y%22%3Atrue%2C%22cartId%22%3A%22a55d09a4-429d-424c-9927-952ff04e219e%22%2C%22storeUrl%22%3A%22https%3A%2F%2Fwww.eggboy.com.tw%22%2C%22cashierPaymentId%22%3A%22%22%2C%22origin%22%3A%22shopping+cart%22%2C%22originType%22%3A%22addToCart%22%2C%22checkoutId%22%3A%225531edac-921f-4be3-a05e-dc68d005a2cc%22%2C%22isPreselectedFlow%22%3Afalse%7D&checkoutOOI=true
