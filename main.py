import pandas as pd
from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

from funds import bes_funds
from portfolio_seek import TS

JS_DATES = "chartMainContent_FonFiyatGrafik.series[0].data.map(a => a.category)"
JS_VALUES = "chartMainContent_FonFiyatGrafik.series[0].data.map(a => a.config)"


def retrieve_funds(long_period=False):
    df = None
    failed_funds = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for idx, fund in enumerate(bes_funds):
            print(f"Processing fund {idx + 1}/{len(bes_funds)}: {fund}")

            try:
                page = browser.new_page()
                url = f"https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={fund}"
                page.goto(url, timeout=60000)

                # Wait for the chart JavaScript object to be available
                page.wait_for_function(
                    "typeof chartMainContent_FonFiyatGrafik !== 'undefined' && chartMainContent_FonFiyatGrafik !== null",
                    timeout=30000,
                )

                # click the 3-year radio button for fetching required funds data
                if long_period:
                    # Click the 3-year radio button
                    page.click("#MainContent_RadioButtonListPeriod_6")

                    # Wait for chart data to reload - be more lenient
                    try:
                        page.wait_for_function(
                            "chartMainContent_FonFiyatGrafik.series[0].data.length > 300",
                            timeout=15000,
                        )
                    except PlaywrightTimeout:
                        # Some funds might have less than 300 data points, that's OK
                        print(
                            f"  Warning: {fund} has less than 300 data points or slow to load"
                        )

                # execute only once - get dates from first fund
                if idx is None:
                    dates_array = page.evaluate(JS_DATES)
                    df = pd.DataFrame({"date": dates_array})

                values_array = page.evaluate(JS_VALUES)
                df[fund] = pd.Series(
                    values_array
                )  # put zero or NaN value for the empty fields
                print(f"  Success: {fund} - {len(values_array)} data points")

                page.close()

            except Exception as e:
                print(f"  Error processing {fund}: {e}")
                failed_funds.append(fund)
                try:
                    page.close()
                except:
                    pass

        browser.close()

    if df is not None:
        df.to_excel("output.xlsx", index=False)
        print(
            f"\nData saved to output.xlsx with {len(df)} rows and {len(df.columns)} columns"
        )

    if failed_funds:
        print(f"\nFailed funds: {failed_funds}")


def main():
    retrieve_funds(long_period=True)
    # tabu_trial = TS("training_tabu_data.xlsx", 2, 3, 0b1000001001010100110000, sector_sd=0.0128, risk_total=40)


if __name__ == "__main__":
    main()
