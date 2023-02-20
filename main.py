from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from funds import bes_funds


JS_DATES = f"return chartMainContent_FonFiyatGrafik.series[0].data.map(a => a.category)"
JS_VALUES = f"return chartMainContent_FonFiyatGrafik.series[0].data.map(a => a.config)"


def main():
    options = Options()
    options.add_argument("--headless=new")

    df = None

    for idx, fund in enumerate(bes_funds):
        driver = webdriver.Chrome(options=options)
        url = f"https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={fund}"
        driver.get(url)

        WebDriverWait(driver, timeout=10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        if idx == 0:
            dates_array = driver.execute_script(JS_DATES)
            df = pd.DataFrame({"date": dates_array})

        values_array = driver.execute_script(JS_VALUES)

        df.insert(len(df.columns), fund, values_array)

        driver.close()

    df.to_excel("output.xlsx", index=False)


if __name__ == "__main__":
    main()
