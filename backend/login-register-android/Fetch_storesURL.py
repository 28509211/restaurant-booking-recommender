import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import concurrent.futures

# 讀取店铺信息
def read_stores_from_file(file_path):
    stores = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析店名和地址
            store_info = line.split(":")[0]
            stores.append(store_info)
    return stores

# Google 搜索 URL 模板
search_url_template = "https://www.google.com/search?q={query}&tbm=isch"

# 搜索函数
def search_image(store_name):
    query = urllib.parse.quote(store_name)
    search_url = search_url_template.format(query=query)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        if len(images) > 1:
            # 返回第一個圖片的連結
            return images[1]['src']
        elif len(images) > 0:
            return images[0]['src']
    return None

# 併發處理搜索函數
def concurrent_search_image(store_name):
    return store_name, search_image(store_name)

# 主函數
def main():
    # 讀店鋪資訊
    file_path = '店家資訊.txt'
    stores = read_stores_from_file(file_path)


    store_images = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_store = {executor.submit(concurrent_search_image, store): store for store in stores}
        for future in concurrent.futures.as_completed(future_to_store):
            store, image_url = future.result()
            store_images[store] = image_url
            print(f"{store}: {image_url}")
            time.sleep(2)  # 添加延遲避免被搜索引擎屏蔽

    # 結果輸出到txt文件
    with open('店家圖片資訊.txt', 'w', encoding='utf-8') as file:
        for store, image_url in store_images.items():
            file.write(f"{store}: {image_url}\n")

    print("结果已保存到store_images.txt文件中")

if __name__ == '__main__':
    main()
