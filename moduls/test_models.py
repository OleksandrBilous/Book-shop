from selenium import webdriver

def test_webpage(url):
    driver = webdriver.Chrome()
    driver.get(url)
    assert "Expected Title" in driver.title
    driver.quit()

test_webpage('http://127.0.0.1:5000/')
