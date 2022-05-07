from pathlib import Path

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(
    executable_path=ChromeDriverManager().install(),
    options=options,
)

data_path = Path('.')
base_url = 'https://lkfl2.nalog.ru'
