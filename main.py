import streamlit as st
from deta import Deta
import time

st.set_page_config(
    page_title='Мировое господство',
    page_icon='🥭',
    layout='wide',
    initial_sidebar_state='collapsed',  # expanded/collapsed
    menu_items={
        'Get Help': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'Report a bug': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'About': '# Автор MangoVirus'
    })


class Country:
    def __init__(self, name, cities):
        self.name = name
        self.cities = cities


# GAME SETTINGS

basic_development = [60, 50, 50, 40]
basic_ecology = [72, 54, 54, 36]
up_multiplier = 10
debaf_multiplier = 20

sanctions_from_you_cost = 50
sanctions_for_you_cost = 100

improving_city_cost = 200
building_shield_cost = 350
building_rocket_cost = 500

all_countries = [
    Country('Китай', ['Пекин', 'Шанхай', 'Гуанчжоу', 'Гонконг']),
    Country('Япония', ['Йокогама', 'Токио', 'Киото', 'Осака']),
    Country('Северная Корея', ['Пхеньян', 'Расон', 'Хусан', 'Вонсан']),
    Country('Пакистан', ['Карачи', 'Лахор', 'Мултан', 'Кветта']),
    Country('Афганистан', ['Кабул', 'Герат', 'Кандагар', 'Кундуз']),
    Country('Сирия', ['Аллепо', 'Дамаск', 'Хама', 'Африн']),
]

# UNIQUE PARAMETERS

current_country_name_eng = 'Kitay'
current_country = all_countries[0]  # Китай
enemies = [x for x in all_countries if x != current_country]  # Страны-оппоненты с городами
enemies_names = [x.name for x in enemies]  # Страны-оппоненты

#

deta = Deta(st.secrets['deta_key'])
Global = deta.Base('Global')
db = deta.Base(current_country_name_eng)
Attak_Kitay = deta.Base('Attak_' + current_country_name_eng)
Graph = deta.Base('Photo_Url')
request = deta.Base('request')
request_money = deta.Base('request_money')
city = Global.get(current_country_name_eng)

money = city['money'] - ((city['sunks_of_you'] * sanctions_from_you_cost) +
                         (city['sunks_for_you'] * sanctions_for_you_cost))

st.sidebar.image('https://cdn.discordapp.com/attachments/890188503047077928/1070451124869533758/066443762463369c.png',
                 width=64)
menu = st.sidebar.selectbox('Меню',
                            ('Стартовая страница', 'Улучшения', 'Ракета', 'Посещения', 'Гуманитарная помощь', 'Авторы'))

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
            Attak_Kitay.put({enemies_names[i]: str(cities_under_attack[i].cities) for i in range(0, len(enemies))})
            db_content = Attak_Kitay.fetch().items
            st.write(db_content)
            with st.spinner('Wait for it...'):
                time.sleep(1)
            st.success('Данные обновлены!')
        else:
            st.error('Вы выпустили больше ракет чем у вас есть...')

if menu == 'Улучшения':
    masiv_up = [0] * len(current_country.cities)
    masiv_shit = [' '] * len(current_country.cities)

    st.write('Деньги:', money)

    st.write('Какие города вы хотите улучшить?')
    for i in range(0, len(current_country.cities)):
        up = st.checkbox(current_country.cities[i])
        if up:
            masiv_up[i] += 1
            money -= improving_city_cost

    st.write('На какие города установим щиты?')
    for i in range(0, len(current_country.cities)):
        shit = st.checkbox(current_country.cities[i] + ' ')
        if shit:
            masiv_shit[i] += '🛡️'
            money -= building_shield_cost

    number = st.number_input('Сколько ракет делаем?', 0)
    st.write('Вы получите в следующие количество ракет', number)
    money -= building_rocket_cost * number

    sunks_for_who = st.multiselect('На какие страны вы хотите наложить санкции?', enemies_names)
    money -= sanctions_from_you_cost * len(sunks_for_who)

    st.write('Ваш баланс после операции:', money)

    for i in range(0, len(current_country.cities)):
        current_up = masiv_up[i] * up_multiplier
        previous_up = city['up' + str(i + 1)] * up_multiplier + current_up
        previous_debaf = city['debaf' + str(i + 1)] * debaf_multiplier
        st.metric('🏠' + city['shit' + str(i + 1)] + masiv_shit[i] + current_country.cities[i],
                  '⚙️' + str(basic_development[i] + previous_up) + '% ' +
                  '🌳' + str(basic_ecology[i] + previous_up - previous_debaf) + '%',
                  current_up)

    if st.button('Отправить данные'):
        if money >= 0:
            db.put({'money': money, 'roket': number, 'shit': str(masiv_shit),
                    'up': str(masiv_up), 'sunks_for_who': str(sunks_for_who)})
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

    lst = st.columns(len(current_country.cities))
    for i in range(0, len(current_country.cities)):
        previous_up = city['up' + str(i + 1)] * up_multiplier
        previous_debaf = city['debaf' + str(i + 1)] * debaf_multiplier
        lst[i].metric('🏠' + city['shit' + str(i + 1)] + current_country.cities[i],
                  '⚙️' + str(basic_development[i] + previous_up) + '% ' +
                  '🌳' + str(basic_ecology[i] + previous_up - previous_debaf) + '%')
