from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


def catalog_selection():
    ru_catalog = ['Популярное', 'Наборы', 'Холодные', 'Роллы-Горячие', 'Роллы-Запечённые', 'Роллы-Онигири',
                  'Роллы-Сушки',
                  'Роллы-Мини',
                  'Пиццы',
                  'Fast food', 'Лапша', 'Салаты', 'Первые блюда', 'Вторые блюда', 'Гарниры', 'Чуду-слоенное',
                  'чуду-обычное', 'Кутабы',
                  'Манты и курзе',
                  'Хинкал', 'Десерты', 'Напитки-Компоты', 'Напитки-Денеб', 'Напитки-Кока-Кола']
    [print(n, v) for n, v in enumerate(ru_catalog, 1)]
    while True:
        n = int(input('\n<<< '))
        if -1 < n < 25:
            return n
        print('Данной категории нет, выберите другую')


def get_html(n):
    catalog = ['popular', 'nabory', 'rolly/holodnye', 'rolly/goryachie', 'rolly/zapechyonnye', 'rolly/onigiri',
               'rolly/sushki', 'rolly/mini',
               'piccy', 'fast_food', 'lapsha', 'salaty', 'pervye-blyuda', 'vtorye-blyuda', 'garniry',
               'chudu/iz-sloenogo-testa-chudu', 'chudu/iz-obychnogo-testa-chudu', 'kutaby', 'manty-i-kurze', 'hinkal',
               'deserty', 'napitki/compoty', 'napitki/deneb', 'napitki/koka-kola']
    url = "https://sloyka-izberbash.ru/izberbash/"
    headers = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36'

    options = webdriver.FirefoxOptions()
    options.add_argument(f'user-agent={headers}')
    driver = webdriver.Firefox(options=options)

    driver.get('https://sloyka-izberbash.ru/izberbash/' + catalog[n-1])
    driver.implicitly_wait(10)
    button1 = driver.find_element(By.XPATH,
                                  '/html/body/div[2]/div[2]/main/div/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[2]')
    button1.click()

    cards = driver.find_elements(By.CLASS_NAME, 'product-card')

    data = []
    for card in cards:
        name = card.find_element(By.CLASS_NAME, 'card-title').text
        description = card.find_element(By.CLASS_NAME, 'card-description').text
        weight = card.find_element(By.CLASS_NAME, 'parameters__single').text
        price = card.find_element(By.CLASS_NAME, 'price-value').text
        img = card.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/main/div/div[1]/div/div[2]/div/div[1]/div/div[2]'
        )

        data.append(
            {'name': name,
             'description': description,
             'weight': weight,
             'price': price,
             'img': img.get_attribute('style').split('"')[1]
             }
        )
    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv('parsed_data.csv', index=False)


def main():
    get_html(catalog_selection())


if __name__ == '__main__':
    main()
