from pathlib import Path

import pandas as pd

import selenium_stages
from driver import data_path


def read_tax_data_from_excel(file_name: str) -> pd.DataFrame:
    data = pd.read_excel(data_path / file_name)
    return data


def prepare_tax_data(data: pd.DataFrame) -> pd.DataFrame:
    data.rename(columns={c: c.replace('\n', ' ') for c in data.columns}, inplace=True)
    print(data.columns)
    data = data[data['Сумма налога, удержанного агентом'] < (data['Сумма до удержания налога']*0.15)]
    return data


def main():
    data = read_tax_data_from_excel('Vargin2021.xlsx')
    data = prepare_tax_data(data)
    selenium_stages.run_selenium(data)


if __name__ == '__main__':
    main()
