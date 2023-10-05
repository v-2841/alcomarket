from django.db import transaction

# Создаем пользователя, который будет связан с заказом
user = User.objects.get(username='your_username')  # Замените 'your_username' на имя пользователя

# Создаем или получаем товары, которые будут включены в заказ
goods_to_include = [
    {'good_id': 1, 'quantity': 2},  # Замените 1 на ID первого товара и установите нужное количество
    {'good_id': 2, 'quantity': 3},  # Замените 2 на ID второго товара и установите нужное количество
]

# Проверяем, что quantity меньше, чем stock для каждого товара
valid_quantity = all(
    Good.objects.filter(pk=item['good_id'], stock__gte=item['quantity']).exists()
    for item in goods_to_include
)

if valid_quantity:
    # Создаем заказ с использованием транзакции
    with transaction.atomic():
        order = Order.objects.create(user=user, total_price=0)  # Инициализируем total_price нулем

        # Добавляем товары в заказ
        for item in goods_to_include:
            good = Good.objects.get(pk=item['good_id'])
            quantity = item['quantity']
            price = good.price
            OrderGood.objects.create(order=order, good=good, quantity=quantity, price=price)

        # Вычисляем и устанавливаем итоговую цену заказа
        order.total_price = sum(item['quantity'] * item['price'] for item in goods_to_include)
        order.save()
else:
    # Обработка случая, когда quantity больше или равно stock для какого-либо товара
    # Можете выбрать соответствующий способ обработки ошибки или вывести сообщение пользователю.
    pass