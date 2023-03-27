from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from funds import bes_funds
from portfolio_seek import TS


JS_DATES = f"return chartMainContent_FonFiyatGrafik.series[0].data.map(a => a.category)"
JS_VALUES = f"return chartMainContent_FonFiyatGrafik.series[0].data.map(a => a.config)"


"""
buttonid need to be clicked for gather 3 years data MainContent_RadioButtonListPeriod_6

"""

def retrieve_funds(long_period=False):

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

        # click the 3-year radio button for fetching required funds data
        if long_period:
            driver.find_element(By.ID, "MainContent_RadioButtonListPeriod_6").click()

            WebDriverWait(driver, timeout=10).until(
                lambda d: d.execute_script("return chartMainContent_FonFiyatGrafik.series[0].data.map(a => a.category).length > 300") == True
            )

        # execute only once 
        if idx == 0:
            dates_array = driver.execute_script(JS_DATES)
            df = pd.DataFrame({"date": dates_array})

        values_array = driver.execute_script(JS_VALUES)
        df[fund] = pd.Series(values_array) # put zero or NaN value for the empty fields

        driver.close()

    df.to_excel("output.xlsx", index=False)


def main():

    retrieve_funds(long_period=True)
    # tabu_trial = TS("training_tabu_data.xlsx", 2, 3, 0b1000001001010100110000, sector_sd=0.0128, risk_total=40)
    
   
if __name__ == "__main__":
    main()
