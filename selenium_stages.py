import json
from datetime import datetime
from pprint import pprint
from time import sleep

import pandas as pd
from selenium.webdriver import DesiredCapabilities

from driver import driver, data_path, base_url


def run_selenium(data: pd.DataFrame) -> None:
    login()
    sleep(2)
    go_from_main_to_3ndfl()
    sleep(2)
    set_data(data)
    # driver.quit()


def login() -> None:
    with (data_path / 'data.json').open('r') as f:
        user_data = json.loads(f.read())
    driver.get(f"{base_url}/lkfl/login")
    # Enter inn
    driver.find_element_by_xpath(
        '//*[@id="scroll-wrapper"]/div[1]/div[3]/div/div/div/div[1]/form/div[1]/div[2]/input'
    ).send_keys(user_data['inn'])
    # Enter password
    driver.find_element_by_xpath(
        '//*[@id="scroll-wrapper"]/div[1]/div[3]/div/div/div/div[1]/form/div[2]/div[2]/input[5]'
    ).send_keys(user_data['password'])
    # Submit
    driver.find_element_by_xpath(
        '//*[@id="scroll-wrapper"]/div[1]/div[3]/div/div/div/div[1]/form/div[4]/div[1]/div/button'
    ).submit()


def go_from_main_to_3ndfl() -> None:
    driver.get(f"{base_url}/lkfl/situations/3NDFL")

    sleep(5)

    # Go next
    driver.find_element_by_xpath(
        '//*[@id="scroll-wrapper"]/div[1]/div[3]/div/div[3]/div/section/div/div[2]/div[2]/div/button[2]'
    ).click()

    sleep(4)

    # Go to no russian money
    driver.find_element_by_xpath(
        '//*[@id="react-tabs-2"]'
    ).click()


def set_data(data: pd.DataFrame) -> None:
    print()
    for i in range(data.shape[0]):
        row: pd.Series = data.iloc[i]
        # add income
        driver.find_element_by_xpath(
            f'//*[@id="react-tabs-3"]/div/div[{i + 1}]/div/div/div/button'
        ).click()
        # add income
        driver.find_element_by_xpath(
            f'//*[@id="react-tabs-3"]/div/div[{i + 1}]/div[1]/div[1]'
        ).click()

        # set compony name
        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].incomeSourceName"]'
        ).send_keys(row['Наименование ценной бумаги'])

        # set country from
        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].oksmIst"]/div[1]/div/div/span[2]'
        ).click()  # .send_keys('840 - СОЕДИНЕННЫЕ ШТАТЫ ')
        [
            element
            for element in
            driver.find_element_by_xpath(
                f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].oksmIst"]/div[1]/div/div[2]'
            ).find_elements_by_class_name('Select-option')
            if element.get_attribute('aria-label') == '840 - СОЕДИНЕННЫЕ ШТАТЫ '
        ][0].click()

        # set country to
        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].oksmZach"]/div[1]/div/div/span[2]'
        ).click()
        [
            element
            for element in
            driver.find_element_by_xpath(
                f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].oksmZach"]/div[1]/div/div[2]'
            ).find_elements_by_class_name('Select-option')
            if element.get_attribute('aria-label') == '643 - РОССИЯ '
        ][0].click()

        # set income code
        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].incomeTypeCode"]/div[1]/div/div/span[2]'
        ).click()
        [
            element
            for element in
            driver.find_element_by_xpath(
                f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].incomeTypeCode"]/div[1]/div[1]'
            ).find_elements_by_class_name('Select-option')
            if element.get_attribute('aria-label') == '1010 - Дивиденды'
        ][0].click()

        # set taxDeductionCode
        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].taxDeductionCode"]/div/div/div/span[2]'
        ).click()
        [
            element
            for element in
            driver.find_element_by_xpath(
                f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].taxDeductionCode"]/div[1]/div[1]'
            ).find_elements_by_class_name('Select-option')
            if element.get_attribute('aria-label') == 'Не предоставлять вычет'
        ][0].click()

        # set my income in $
        date: datetime = row['Дата выплаты'].to_pydatetime()
        str_date = date.strftime("%d.%m.%Y")

        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].incomeAmountCurrency"]'
        ).send_keys(row['Сумма до удержания налога'])
        # set income date
        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].incomeDate"]/div[2]/div[1]/div/div/input'
        ).send_keys(str_date)
        # set tax payment date
        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].taxPaymentDate"]/div[2]/div[1]/div/div/input'
        ).send_keys(str_date)

        # set currencyCode
        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].currencyCode"]/div[1]/div/div/span[2]'
        ).click()
        [
            element
            for element in
            driver.find_element_by_xpath(
                f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].currencyCode"]/div[1]/div[1]'
            ).find_elements_by_class_name('Select-option')
            if element.get_attribute('aria-label') == '840 - Доллар США'
        ][0].click()

        # set default CurrencyInfo
        driver.find_element_by_xpath(
            f'//*[@id="react-tabs-3"]/div/div[{i+1}]/div[2]/div/div[3]/div[2]/div[2]/div[5]'
        ).click()

        # set tax sum of tinkoff
        driver.find_element_by_xpath(
            f'//*[@id="Ndfl3Package.payload.sheetB.sources[{i}].paymentAmountCurrency"]'
        ).send_keys(row['Сумма налога, удержанного агентом'])
