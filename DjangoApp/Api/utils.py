from django.db.models import Sum

from .models import Transaction


def get_balance() -> dict:
    balance = Transaction.objects.values('payer') \
        .annotate(total_points=Sum('points')) \
        .values('payer', 'total_points')
    return {item['payer']: item['total_points'] for item in balance}


def point_counter(transactions, points_to_spend) -> list:
    balance_dict = get_balance()
    new_balance = balance_dict.copy()
    spent_points_list = []

    for transaction in transactions:
        payer = transaction.payer
        points = min(points_to_spend, transaction.points)

        if new_balance[payer] != 0:
            new_balance[payer] -= points
            if new_balance[payer] < 0:
                points_to_spend -= abs(new_balance[payer])
                new_balance[payer] = 0
            else:
                points_to_spend -= points

        if points_to_spend == 0:
            break

    for i in new_balance:
        payer = i
        points = new_balance[i] - balance_dict[i]
        transaction = Transaction(payer=payer, points=points)
        spent_points_list.append({'payer': payer, 'points': points})
        if points != 0:
            transaction.save()
    return spent_points_list
