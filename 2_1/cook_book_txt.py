def get_shop_list_by_dishes(dishes, person_count):
	cook_book = read_book()
	shop_list = {}
	for dish in dishes:
		for ingridient in cook_book[dish]:
			new_shop_list_item = dict(ingridient)
			new_shop_list_item['quantity'] *= person_count
			if new_shop_list_item['ingridient_name'] not in shop_list:
				shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
			else:
				shop_list[new_shop_list_item['ingridient_name']]['quantity'] +=\
						new_shop_list_item['quantity']
	return shop_list


def print_shop_list(shop_list):
	for shop_list_item in shop_list.values():
		print('{} {} {}'.format(shop_list_item['ingridient_name'], shop_list_item['quantity'],
			shop_list_item['measure']))


def create_shop_list():
	person_count = int(input('Введите количество человек: '))
	dishes = input('Введите блюда в расчете на одного человека (через запятую): ') \
		.lower().split(', ')
	shop_list = get_shop_list_by_dishes(dishes, person_count)
	print_shop_list(shop_list)


def read_book():
	title = ['ingridient_name', 'quantity', 'measure']
	dishes = list()
	ingridients_lists = list()
	with open('cookBook.txt') as book_file:
		for line in book_file:
			dish = line.strip()
			if not dish:
				continue
			ingridients_list = list()
			for i in range(int(book_file.readline())):
				ingridient_value = book_file.readline().strip().split('|')
				ingridient_value[1] = int(ingridient_value[1])
				ingridients_list.append(dict(zip(title, ingridient_value)))
			dishes.append(dish)
			ingridients_lists.append(ingridients_list)
	return dict(zip(dishes, ingridients_lists))


create_shop_list()


