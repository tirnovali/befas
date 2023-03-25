from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from funds import bes_funds
from portfolio_seek import TS


JS_DATES = f"return chartMainContent_FonFiyatGrafik.series[0].data.map(a => a.category)"
JS_VALUES = f"return chartMainContent_FonFiyatGrafik.series[0].data.map(a => a.config)"


def main():

    tabu_trial = TS("training_tabu_data.xlsx", 2, 2, 0b1000000000000000111111, sector_sd=0.0128, risk_total=40)
    print("best solution {:022b}".format(tabu_trial.best_solution))
    print(tabu_trial.best_objvalue)

    # options = Options()
    # options.add_argument("--headless=new")

    # df = None

    # for idx, fund in enumerate(bes_funds):
    #     driver = webdriver.Chrome(options=options)
    #     url = f"https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={fund}"
    #     driver.get(url)

    #     WebDriverWait(driver, timeout=10).until(
    #         lambda d: d.execute_script("return document.readyState") == "complete"
    #     )

    #     if idx == 0:
    #         dates_array = driver.execute_script(JS_DATES)
    #         df = pd.DataFrame({"date": dates_array})

    #     values_array = driver.execute_script(JS_VALUES)

    #     df.insert(len(df.columns), fund, values_array)

    #     driver.close()

    # df.to_excel("output.xlsx", index=False)


if __name__ == "__main__":
    main()
