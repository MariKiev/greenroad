# -*- coding: utf-8 -*-
from app import db, Track, Role, User


def main():
    db.session.add(Track(u'Полонина Боржава', 45, 3, u'низкая', u'''Полони́на Боржа́ва — горный массив на Полонинском хребте Украинских Карпат, между реками Латорицей и Рикой в пределах Закарпатской области (Украина). Длина свыше 50 км, ширина 34 км, высота до 1681 м (гора Стой). Южный склон полонины пологий, он удлинён и расчленён, северный — круто обрывается к долине реки Рипинки. К Боржавской полонине примыкает полонина Кук которую часто считают отдельным горным массивом. К этой полонине относится также хребет Паленый Грун. Дальний гребень полонины находится на расстоянии 44 км, поэтому Боржава представляет собой самую длинную полонину Закарпатья.

	Пригребневые поверхности выравнены, с отдельными конусообразными вершинами:
	Стой (1681 м),
	Темнатик (1343 м),
	Большой Верх (1598 м),
	Магура-Жиде (1505 м),
	Граб (1374 м),
	Гемба (1498 м)
	Кук (1361 м) и другие.
	Состоит из флиша (в слоях преобладают песчаники). Склоны расчленены притоками рек Боржавы, Латорицы и Рики. На высоте 1200—1450 м находится пояс буковых лесов, выше — горные долины. На склонах горы Стой — заказник государственного значения Росошный. Полонина Боржава в прошлом была районом отгонного овцеводства, в современности — район туризма.
	''', u'''Воловец - водопад Шипот - гора Гемба - гора Великий Верх - гора Стой - хребет Полонина Боржава - гора Темнатик - Воловец''', '/static/borjava.jpg'))

    db.session.add(Track(u'Озеро Синевир', 75, 6, u'средняя', u'''Синеви́р — самое известное и большое озеро в Украинских Карпатах[1], расположенное в верховьях реки Теребли. Площадь его водного зеркала около 4-5 гектаров. Питают озеро ручьи. Отток воды преграждает горный обвал, в основании которого просачивается вода, образуя поток, впадающий в Тереблю.
		В озере Синевир водится большое количество форели, но лов рыбы запрещен, а вот раков, которых здесь тоже большое количество, ловить можно. 
		Синевир находится на высоте 989 метров над уровнем моря, средняя глубина озера — 10—12 метров, максимальная — 24 метра. Озеро образовалось в послеледниковый период. В 1989 году на территориях, окружающих озеро, создан Национальный парк Синевир. ''', 
		u'''Ивано-Франковск – с.Осмолода – г.Грофа – г.Попадья (1740м.) – г.Верх Черной Горы - гора Канч - гора Погар – оз.Синевир - гора Озерна – хребет Камянка - река Озерянка - Дикое Озеро - хребет Пишконя - Колочава - Ивано-Франковск.''', '/static/sinevir.jpg'))

    db.session.add(Track(u'Черногорский хребет', 55, 6, u'средняя', u'''Черногорский хребет - наиболее популярный экскурсионный объект Украинских Карпат, который посещают тысячи туристов, альпинистов и ученых из множества стран мира. Черногора — самый высокий горный хребет в украинских Карпатах, находится в восточной части Полонинского Бескида; главный хребет простирается в длину около 40 км между Чёрной Тисой на западе и Чёрным Черемошем на востоке.
		Многие века по Черногорскому хребту проходила граница государств, которым принадлежали Галичина и Закарпатье. Высота Черногорского хребта около 2000 м (Петрос - 2020м, Говерла — 2061м, Шпицы — 1997м, Гутен Темнатек — 2018м, Поп Иван — 2022м). На внешний вид с больше, чем в других частях Карпат, повлияло обледенение (в долине Прута ледник достигал высоты 1000 м и составлял в длину 6,5 км). Следами бывшего обледенения являются поледниковые котлы с отвесными, часто скальными склонами и широким дном, иногда наполненными озёрами (наибольшее под Темнатеком), боковые и концевые морены, кары, цирки. 
		Оледенение было и на соседнем к западу хребте Свидовец. Склоны Черногоры покрыты лесами. На северных склонах обычно растёт бук (до высоты 1300м), выше — ель (исключительно до 1600 м); на южном склоне также распространен бук, который образует горную границу леса. Выше — до 1800 м находится полоса полонин.''', 
		u'''с. Ясыня — г.Петрос(2022м) — г.Говерла(2061м) — оз. Несамовытое (1750 м) — г. Ребра (2001 м) — г. Бребенескул (2036 м) — г. Менчул (1998 м) — г.Поп-Иван (2026м) — с. Дземброня''', '/static/beskid.jpg'))

    db.session.add(Role('Admin_role'))

    db.session.add(Role('User_role'))
    admin = User('Marina', 'iam.marik@gmail.com', 'test', True, 1)
    admin.confirmed = True
    db.session.add(admin)

    db.session.commit()

if __name__ == '__main__':
    main()