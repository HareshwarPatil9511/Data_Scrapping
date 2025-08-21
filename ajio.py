import time
import csv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Step 1: Start Chrome with stealth mode
driver = uc.Chrome()

try:
    # Step 2: Open the AJIO backpacks category
    driver.get("https://www.ajio.com/men-backpacks/c/830201001")
    time.sleep(5)

    # Step 3: Scroll until all products are loaded
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Step 4: Find all product containers
    products = driver.find_elements(By.CLASS_NAME, 'item')

    # Step 5: Extract data
    data = []
    for product in products:
        try:
            brand = product.find_element(By.CLASS_NAME, 'brand').text
        except:
            brand = ""
        try:
            name = product.find_element(By.CLASS_NAME, 'nameCls').text
        except:
            name = ""
        try:
            price = product.find_element(By.CLASS_NAME, 'price').text
        except:
            price = ""
        try:
            image = product.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except:
            image = ""
        try:
            link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except:
            link = ""

        data.append([brand, name, price, image, link])

    # Step 6: Save to CSV
    with open("ajio_backpacks.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Brand', 'Product Name', 'Price', 'Image URL', 'Product Link'])
        writer.writerows(data)

    print(f"✅ Scraped {len(data)} products. Saved to ajio_backpacks.csv")
    time.sleep(10)

finally:
    try:
        driver.quit()  # Safely attempt quit
    except:
        pass  # Silently ignore if already closed
