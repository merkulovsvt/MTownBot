start_text_old = '''
*Стоимость расчета через бот носит справочный характер.


В стоимость включен следующий состав услуг:

- Проверка автомобиля перед покупкой в Европе
- Перевод денег
- Оплата автомобиля
- Оформление экспортных документов
- Возврат немецкого НДС (вы покупаете автомобиль сразу по цене НЕТТО, вам не нужно ждать пока вернут немецкий НДС)
- Доставка автомобиля автовозом
- Страхование автомобиля на время перевозки
- Оплата таможенной пошлины
- Финальная проверка авто после доставки
- Предпродажная подготовка перед выдачей автомобиля


Оформление СБКТС и ЭПТС, списание утильсбора - являются отдельной услугой и не включены в стоимость расчета.


Осуществить заказ и узнать об автомобиле подробнее : @i1kuch'''

start_text = '''
Привет! 
Это телеграм бот для расчета импорта автомобиля из Германии, выберите автомобиль на mobile.de/ru и мы посчитаем предварительную стоимость доставки и таможни автомобиля.'''

parser_text = '''
**{car_name}** стоит **{car_price}** евро (без НДС) 

Таможня:
На белоруссию - **{bel_price}** руб
На россию - **{rus_price}** руб

В стоимость включен следующий состав услуг:

- Проверка автомобиля перед покупкой в Европе
- Перевод и конвертация денег
- Оплата автомобиля с юридического лица в Европе
- Оформление экспортных документов
- Возврат немецкого НДС (вы покупаете автомобиль без НДС)
- Доставка автомобиля автовозом
- Страхование автомобиля на время перевозки
- Оплата таможенной пошлины
- Финальная проверка авто после доставки
- Предпродажная подготовка перед выдачей автомобиля

Оформление СБКТС и ЭПТС, списание утильсбора - являются отдельной услугой и не включены в стоимость расчета.

---

Это предварительный расчет, для более подробного оставьте заявку.   
'''