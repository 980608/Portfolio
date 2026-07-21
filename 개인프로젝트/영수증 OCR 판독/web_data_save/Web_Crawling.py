from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests

# =====================
# 설정
# =====================

items = [
    "계란",      # egg
    "양파",      # onion
    "감자",      # potato
    "당근",      # carrot
    "토마토",    # tomato
    "마늘",      # garlic
    "대파",      # green_onion
    "양배추",    # cabbage
    "버섯"       # mushroom
]


base_dir = "C:/Users/tldk2/Desktop/img_data"
os.makedirs(base_dir, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # 필요하면 켜기

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)

# =====================
# 네이버 이미지 검색 진입
# =====================
browser.get("https://search.naver.com/search.naver?where=image")

for query in items:

    save_dir = os.path.join(base_dir, query)
    os.makedirs(save_dir, exist_ok=True)

    # 검색 입력
    search_box = wait.until(
        EC.presence_of_element_located((By.NAME, "query"))
    )
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)

    time.sleep(2)

    # =====================
    # 스크롤 (이미지 로딩)
    # =====================
    last_height = browser.execute_script("return document.body.scrollHeight")

    for _ in range(5):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # =====================
    # 이미지 수집
    # =====================
    images = browser.find_elements(By.CSS_SELECTOR, "img")

    count = 0

    for img in images:
        try:
            img_url = img.get_attribute("data-source") or img.get_attribute("src")

            if not img_url:
                continue
            if "http" not in img_url:
                continue
            if "data:image" in img_url:
                continue

            headers = {"User-Agent": "Mozilla/5.0"}

            r = requests.get(img_url, headers=headers, timeout=5)

            if r.status_code != 200:
                continue

            file_path = os.path.join(save_dir, f"{query}_{count}.jpg")

            with open(file_path, "wb") as f:
                f.write(r.content)

            count += 1

            if count >= 400:  # 이미지 개수 제한
                break

        except:
            pass

    print(f"{query} 완료: {count}장 저장")

browser.quit()
print("전체 완료")



from PIL import Image
import os
import hashlib

#1. 이미지 유효성 필터링 (깨진 파일 제거)
def filter_corrupt_images(root_dir):
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            try:
                img = Image.open(file_path)
                img.verify()  # 깨진 이미지 체크
            except:
                os.remove(file_path)
                print("삭제:", file_path)

# 2. 이미지 해상도 통일 (YOLO 필수)
def resize_images(root_dir, size=(640, 640)):
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            try:
                img = Image.open(file_path).convert("RGB")
                img = img.resize(size)
                img.save(file_path)
            except:
                pass

# 3. 중복 이미지 제거
def remove_duplicates(root_dir):
    hashes = set()

    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            try:
                with open(file_path, "rb") as f:
                    img_hash = hashlib.md5(f.read()).hexdigest()

                if img_hash in hashes:
                    os.remove(file_path)
                    print("중복 삭제:", file_path)
                else:
                    hashes.add(img_hash)

            except:
                pass


# 4. 너무 작은 이미지 제거 (노이즈 제거)
def remove_small_images(root_dir, min_size=200):
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            try:
                img = Image.open(file_path)
                w, h = img.size

                if w < min_size or h < min_size:
                    os.remove(file_path)
                    print("작아서 삭제:", file_path)

            except:
                pass

root_dir = "C:/Users/tldk2/Desktop/img_data"

filter_corrupt_images(root_dir)
remove_duplicates(root_dir)
remove_small_images(root_dir)
resize_images(root_dir, (640, 640))

print("전처리 완료")











from icrawler.builtin import BingImageCrawler

items = [
    "egg",
    "onion",
    "potato",
    "carrot",
    "tomato",
    "cucumber",
    "banana",
    "apple",
    "garlic"
]

for item in items:
    crawler = BingImageCrawler(
        storage={'root_dir': f'C:/Users/tldk2/Desktop/img_data/{item}'}
    )

    crawler.crawl(
        keyword=f'{item} isolated white background',
        max_num=200
    )

    print(item, "완료")
















