import streamlit as st
from deta import Deta
import time

deta = Deta(st.secrets["deta_key"])
Global = deta.Base("Global")
db = deta.Base('Kitay')
Attak_Kitay = deta.Base('Attak_Kitay')
Graph = deta.Base('Photo_Url')
request = deta.Base('request')
request_money = deta.Base('request_money')

city = Global.get('Kitay')

Global.put({'money': '1000', 'sunks_of_you': '0', 'sunks_for_you': '0', 'roket': '0', 'shit1': '0', 'shit2': '0',
          'shit3': '0', 'shit4': '0', 'up1': '0', 'up2': '0', 'up3': '0', 'up4': '0', 'debaf1': '0', 'debaf2': '0',
          'debaf3': '0', 'debaf4': '0'})

db_content = Attak_Kitay.fetch().items
st.write(db_content)

money = city['money'] - ((city['sunks_of_you'] * 50) + (city['sunks_for_you'] * 100))
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
st.sidebar.image('https://cdn.discordapp.com/attachments/890188503047077928/1070451124869533758/066443762463369c.png',
                 width=64)
menu = st.sidebar.selectbox('Меню',
                            ('Стартовая страница', 'Улучшения', 'Ракета', 'Посещения', 'Гуманитарная помощь', 'Авторы'))

masiv_up = [0, 0, 0, 0]
masiv_shit = [' ', ' ', ' ', ' ']
attak = []
attak1 = []
attak2 = []
attak3 = []
attak4 = []

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
    visit_money = st.selectbox('Кому вы хотите перевести деньги?',
                               ('Япония', 'Северная Корея', 'Пакистан', 'Афганистан', 'Сирия'))
    how_money = st.number_input('Сумма перевода?', 0)
    if st.button('Перевести'):
        request_money.put({'who': 'Kitay', 'come': visit_money, 'price': how_money})
        st.success('Запрос на перевод отправлен.(Деньги придут в течение 5 минут)')

if menu == 'Посещения':
    visit = st.selectbox('Какую старану вы хотите посетить?',
                         ('Япония', 'Северная Корея', 'Пакистан', 'Афганистан', 'Сирия'))
    if st.button('Отправить запрос'):
        request.put({'who': 'Kitay', 'come': visit})
        st.success('Запрос на посещение отправлен')

if menu == 'Ракета':
    final_roket = -1
    st.write('Количество ваших ракет:', city['roket'])

    country = st.multiselect('Какие страны атакуем?', ['Япония', 'Северная Корея', 'Пакистан', 'Афганистан', 'Сирия'])
    attak_dict = dict.fromkeys(['Япония', 'Северная Корея', 'Пакистан', 'Афганистан', 'Сирия'], [])

    for i in range(0, len(country)):
        if country[i] == 'Япония':
            attak_dict['Япония'] = st.multiselect('Какие города атакуем в Японии?',
                                                  ['Йокогама', 'Токио', 'Киото', 'Осака', ])
        if country[i] == 'Северная Корея':
            attak_dict['Северная Корея'] = st.multiselect('Какие города атакуем в Северной-Корее?',
                                                          ['Пхеньян', 'Расон', 'Хусан', 'Вонсан', ])
        if country[i] == 'Пакистан':
            attak_dict['Пакистан'] = st.multiselect('Какие города атакуем в Пакистане?',
                                                    ['Карачи', 'Лахор', 'Мултан', 'Кветта', ])
        if country[i] == 'Афганистан':
            attak_dict['Афганистан'] = st.multiselect('Какие города атакуем в Афганистане?',
                                                      ['Кабул', 'Герат', 'Кандагар', 'Кундуз', ])
        if country[i] == 'Сирия':
            attak_dict['Сирия'] = st.multiselect('Какие города атакуем в Сирии?',
                                                 ['Аллепо', 'Дамаск', 'Хама', 'Африн', ])
        final_roket = city['roket'] - (sum(list(map(len, attak_dict.values()))))
        st.write('У вас останеться ракет:', final_roket)

    if st.button('Отправить данные'):
        if final_roket >= 0:
            Attak_Kitay.put({'Япония': str(attak_dict['Япония']),
                             'Северная Корея': str(attak_dict['Северная Корея']),
                             'Пакистан': str(attak_dict['Пакистан']),
                             'Афганистан': str(attak_dict['Афганистан']),
                             'Сирия': str(attak_dict['Сирия'])
                             })
            db_content = Attak_Kitay.fetch().items
            st.write(db_content)
            with st.spinner('Wait for it...'):
                time.sleep(1)
            st.success('Данные обновлены!')
        else:
            st.error('Вы выпустили больше ракет чем у вас есть...')

if menu == 'Улучшения':
    time1 = 0
    st.write('Деньги:', money)

    st.write('Какие города вы хотите улучшить?')
    up = st.checkbox('Пекин')
    if up:
        masiv_up[0] += 1
        money -= 200
    up1 = st.checkbox('Шанхай')
    if up1:
        masiv_up[1] += 1
        money -= 200
    up2 = st.checkbox('Гуанчжоу')
    if up2:
        masiv_up[2] += 1
        money -= 200
    up3 = st.checkbox('Гонконг')
    if up3:
        masiv_up[3] += 1
        money -= 200

    st.write('На какие города установим щиты?')
    shit = st.checkbox('Пекин ')
    if shit:
        masiv_shit[0] += '🛡️'
        money -= 400
    shit1 = st.checkbox('Шанхай ')
    if shit1:
        masiv_shit[1] += '🛡️'
        money -= 400
    shit2 = st.checkbox('Гуанчжоу ')
    if shit2:
        masiv_shit[2] += '🛡️'
        money -= 400
    shit3 = st.checkbox('Гонконг ')
    if shit3:
        masiv_shit[3] += '🛡️'
        money -= 400

    number = st.number_input('Сколько ракет делаем?', 0)
    st.write('Вы получите в следующие количество ракет', number)
    money -= 500 * number

    sunks_for_who = st.multiselect('На какие страны вы хотите наложить санкции?',
                                   ['Япония', 'Северная Корея', 'Пакистан', 'Афганистан', 'Сирия'])
    money -= 50 * len(sunks_for_who)

    st.write('Ваш баланс после операции:', money)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('🏠' + city['shit1'] + masiv_shit[0] + 'Пекин',
                '⚙️' + str(60 + 10 * city['up1'] + 10 * masiv_up[0]) + '%' + ' 🌳 ' + str(
                    72 + (10 * city['up1'] + 10 * masiv_up[0]) - (city['debaf1'] * 20)) + '%', masiv_up[0] * 10)
    col2.metric('🏠' + city['shit2'] + masiv_shit[1] + 'Шанхай',
                '⚙️' + str(50 + 10 * city['up2'] + 10 * masiv_up[1]) + '%' + ' 🌳 ' + str(
                    54 + (10 * city['up2'] + 10 * masiv_up[1]) - - (city['debaf2'] * 20)) + '%', masiv_up[1] * 10)
    col3.metric('🏠' + city['shit3'] + masiv_shit[2] + 'Гуанчжоу',
                '⚙️' + str(50 + 10 * city['up3'] + 10 * masiv_up[2]) + '%' + ' 🌳 ' + str(
                    54 + (10 * city['up3'] + 10 * masiv_up[2]) - (city['debaf3'] * 20)) + '%', masiv_up[2] * 10)
    col4.metric('🏠' + city['shit4'] + masiv_shit[3] + 'Гонконг',
                '⚙️' + str(40 + 10 * city['up4'] + 10 * masiv_up[3]) + '%' + ' 🌳 ' + str(
                    36 + (10 * city['up4'] + 10 * masiv_up[3]) - (city['debaf4'] * 20)) + '%', masiv_up[3] * 10)

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
    st.title('Вы играете за Китай')

    st.write('Деньги:', money)
    st.write('Ракеты:', city['roket'])
    st.write('Санкции наложеные вами:', city['sunks_of_you'])
    st.write('Санкции наложеные на вас:', city['sunks_for_you'])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('🏠' + city['shit1'] + 'Пекин', '⚙️' + str(60 + 10 * city['up1']) + '%' + ' 🌳 ' + str(
        72 + 10 * city['up1'] - (city['debaf1'] * 20)) + '%')
    col2.metric('🏠' + city['shit2'] + 'Шанхай', '⚙️' + str(50 + 10 * city['up2']) + '%' + ' 🌳 ' + str(
        54 + 10 * city['up2'] - (city['debaf2'] * 20)) + '%')
    col3.metric('🏠' + city['shit3'] + 'Гуанчжоу', '⚙️' + str(50 + 10 * city['up3']) + '%' + ' 🌳 ' + str(
        54 + 10 * city['up3'] - (city['debaf3'] * 20)) + '%')
    col4.metric('🏠' + city['shit4'] + 'Гонконг', '⚙️' + str(40 + 10 * city['up4']) + '%' + ' 🌳 ' + str(
        36 + 10 * city['up4'] - (city['debaf4'] * 20)) + '%')
    photo = deta.Base('Photo_Url')
    pp = photo.get('bb6a5172diyj')
    st.image(pp['Graph1'])
    st.image(pp['Graph2'])
    st.image(pp['Graph3'])
    st.image(pp['Graph4'])
    st.caption('Автор MangoVirus')
