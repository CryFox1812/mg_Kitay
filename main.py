import streamlit as st
from deta import Deta
import time

st.set_page_config(
    page_title="Мировое господство",
    page_icon="🥭",
    layout="wide",
    initial_sidebar_state="collapsed",  # expanded/collapsed
    menu_items={
        'Get Help': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'Report a bug': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        'About': "# Автор MangoVirus"
    })

# GLOBAL CONSTANTS


class Country:
    def __init__(self, name, cities):
        self.name = name
        self.cities = cities


all_countries = [
    Country('Китай', ['Пекин', 'Шанхай', 'Гуанчжоу', 'Гонконг']),
    Country('Япония', ['Йокогама', 'Токио', 'Киото', 'Осака']),
    Country('Северная Корея', ['Пхеньян', 'Расон', 'Хусан', 'Вонсан']),
    Country('Пакистан', ['Карачи', 'Лахор', 'Мултан', 'Кветта']),
    Country('Афганистан', ['Кабул', 'Герат', 'Кандагар', 'Кундуз']),
    Country('Сирия', ['Аллепо', 'Дамаск', 'Хама', 'Африн']),
]
current_country = all_countries[0]  # Китай
enemies = [x for x in all_countries if x != current_country]  # Страны-оппоненты с городами
enemies_names = [x.name for x in enemies]  # Страны-оппоненты

# LOCAL CONSTANTS

# LOCAL DATA

#

deta = Deta(st.secrets["deta_key"])
Global = deta.Base("Global")
db = deta.Base('Kitay')
Attak_Kitay = deta.Base('Attak_Kitay')
Graph = deta.Base('Photo_Url')
request = deta.Base('request')
request_money = deta.Base('request_money')
city = Global.get('Kitay')

money = city['money'] - ((city['sunks_of_you'] * 50) + (city['sunks_for_you'] * 100))

st.sidebar.image('https://cdn.discordapp.com/attachments/890188503047077928/1070451124869533758/066443762463369c.png',
                 width=64)
menu = st.sidebar.selectbox('Меню',
                            ('Стартовая страница', 'Улучшения', 'Ракета', 'Посещения', 'Гуманитарная помощь', 'Авторы'))

masiv_up = [0, 0, 0, 0]
masiv_shit = [' ', ' ', ' ', ' ']

if menu == 'Авторы':
    '''# Над данным проектом работали'''
    st.subheader('MangoVirus')
    '''Разработчик сайта, создатель DataBase.'''
    st.subheader('Турба')
    '''Проектный руководитель, дизайнер.'''
    st.subheader(
        'Если вы хотите поддержать нас и в будущем видеть более маштабные нововедения вы '
        'можете скинуть нам пару тугриков по номеру телефона 8(977)382-41-17')

if menu == 'Гуманитарная помощь':
    st.write('Деньги:', money)
    visit_money = st.selectbox('Кому вы хотите перевести деньги?', enemies_names)
    how_money = st.number_input('Сумма перевода?', 0)
    if st.button('Перевести'):
        request_money.put({'who': current_country.name, 'come': visit_money, 'price': how_money})
        st.success('Запрос на перевод отправлен.(Деньги придут в течение 5 минут)')

if menu == 'Посещения':
    visit = st.selectbox('Какую старану вы хотите посетить?', enemies_names)
    if st.button('Отправить запрос'):
        request.put({'who': current_country.name, 'come': visit})
        st.success('Запрос на посещение отправлен')

if menu == 'Ракета':
    final_roket = -1
    st.write('Количество ваших ракет:', city['roket'])

    selected_countries = st.multiselect('Какие страны атакуем?', enemies_names)
    cities_under_attack = [Country(country_name, []) for country_name in enemies_names]

    for country in selected_countries:
        for i in range(0, len(enemies)):
            if country == enemies[i].name:
                cities_under_attack[i].cities = st.multiselect('Какие города атакуем в стране ' + country + '?',
                                                               enemies[i].cities)
        final_roket = city['roket'] - (sum(len(country_cities.cities) for country_cities in cities_under_attack))
        st.write('У вас останеться ракет:', final_roket)

    if st.button('Отправить данные'):
        if final_roket >= 0:
            Attak_Kitay.put({enemies_names[i]: cities_under_attack[i].cities for i in range(0, len(enemies))})
            db_content = Attak_Kitay.fetch().items
            st.write(db_content)
            with st.spinner('Wait for it...'):
                time.sleep(1)
            st.success('Данные обновлены!')
        else:
            st.error('Вы выпустили больше ракет чем у вас есть...')

if menu == 'Улучшения':
    st.write('Деньги:', money)

    st.write('Какие города вы хотите улучшить?')
    for i in range(0, len(current_country.cities)):
        up = st.checkbox(current_country.cities[i])
        if up:
            masiv_up[i] += 1
            money -= 200

    st.write('На какие города установим щиты?')
    for i in range(0, len(current_country.cities)):
        shit = st.checkbox(current_country.cities[i] + ' ')
        if shit:
            masiv_shit[i] += '🛡️'
            money -= 350

    number = st.number_input('Сколько ракет делаем?', 0)
    st.write('Вы получите в следующие количество ракет', number)
    money -= 500 * number

    sunks_for_who = st.multiselect('На какие страны вы хотите наложить санкции?', enemies_names)
    money -= 50 * len(sunks_for_who)

    st.write('Ваш баланс после операции:', money)

    for i in range(0, len(current_country.cities)):
        st.metric('🏠' + city['shit' + str(i + 1)] + masiv_shit[i] + current_country.cities[i],
                  '⚙️' + str(60 + 10 * city['up' + str(i + 1)] + 10 * masiv_up[i]) + '%' +
                  ' 🌳 ' + str(72 + (10 * city['up' + str(i + 1)] + 10 * masiv_up[i]) - (city['debaf' + str(i + 1)] * 20)) + '%',
                  masiv_up[i] * 10)

    if st.button('Отправить данные'):
        if money >= 0:
            db.put({"money": money, "roket": number, "shit": str(masiv_shit), "up": str(masiv_up),
                    'sunks_for_who': str(sunks_for_who)})
            db_content = db.fetch().items
            st.write(db_content)
            with st.spinner('Wait for it...'):
                time.sleep(1)
            st.success('Данные обновлены!')
        else:
            st.error('Вы потратили больше денег чем у вас есть...')

if menu == 'Стартовая страница':
    st.title('Вы играете за ' + current_country.name)

    st.write('Деньги:', money)
    st.write('Ракеты:', city['roket'])
    st.write('Санкции наложеные вами:', city['sunks_of_you'])
    st.write('Санкции наложеные на вас:', city['sunks_for_you'])

    for i in range(0, len(current_country.cities)):
        st.metric('🏠' + city['shit' + str(i + 1)] + current_country.cities[i],
                  '⚙️' + str(60 + 10 * city['up' + str(i + 1)]) + '%' +
                  ' 🌳 ' + str(72 + 10 * city['up' + str(i + 1)] - (city['debaf' + str(i + 1)] * 20)) + '%')
