from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = 'jia_areej' 
password = 'Kamli99!'   
targetUser = 'kole404_'
post_url = 'https://www.instagram.com/kole404_'  

driver = webdriver.Chrome()  

try:
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(5) 

    # Enter username
    username_input = driver.find_element(By.NAME, 'username')
    username_input.send_keys(username)

    # Enter password
    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN) 

    time.sleep(5) 

    driver.get(post_url)
    time.sleep(2)  
    post_links = []
    # Scroll to load posts
    for _ in range(5):  
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Wait until posts are visible
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/p/"]'))
            )
        except:
            print("No new posts found")

        posts = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]')

        for post in posts:
            link = post.get_attribute('href')
            if '/p/' in link:  
                post_links.append(link)

    print("\nFound posts:")
    for i, post in enumerate(post_links, start=1):
        print(f"{i}. {post}")

    # Ask user to select a post number
    selected_post = int(input("\nEnter the post number to fetch comments: ")) - 1

    if 0 <= selected_post < len(post_links):
        post_url = post_links[selected_post]
        driver.get(post_url)
        time.sleep(5)  

        print(f"\nFetching comments for {post_url}:")

        # Scroll down to load more comments
        for _ in range(3):  
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # **Updated comment selector**
        comment_elements = driver.find_elements(By.CSS_SELECTOR, '[role="presentation"] ul div li div span')

        if not comment_elements:
            print("No comments found. Instagram might be blocking automation.")
        else:
            for comment in comment_elements:
                print(f"- {comment.text}")

    else:
        print("Invalid post number selected!")

finally:
    driver.quit()