# js_script = "return chartMainContent_FonFiyatGrafik.series[0].data.map(a => { return {'VGF': a.config,'date': a.category } })"

# scripts = driver.find_elements(By.XPATH, "//script[@type='text/javascript']")

# for script in scripts:

#     jsText = driver.execute_script("return arguments[0].innerHTML", script)
#     if "chartMainContent_FonFiyatGrafik" in jsText:
#         print(jsText)

# js_script = f"return chartMainContent_FonFiyatGrafik.series[0].data.map(a => {{ return {{ {fund}: a.config,'date': a.category }} }})"

bes_funds = [
    "VGA",
    "VGD",
    "VGF",
    "VEH",
    "HHE",
    "HHB",
    "VEO",
    "ZHB",
    "VGC",
    "VEY",
    "VGH",
    "VEV",
    "HHN",
    "VEE",
    "ZHE",
    "VEI",
    "VGP",
    "TBJ",
    "HHY",
    "HHG",
    "VEG",
    "ZHD",
    "VET",
    "VYB",
    "VGE",
    "VEK",
    "VGY",
    "VGT",
    "HHM",
    "VEB",
    "VGG",
    "VGK",
    "VGZ",
    "ZHF",
    "ZHG",
    "VES",
    "VER",
    "VGB",
    "VEP",
    "TML",
    "VED",
    "VEU",
    "VKE",
    "VKJ",
    "VEL",
    "TJY",
    "TYJ",
]

bes_funds_test = ["VGA"]


