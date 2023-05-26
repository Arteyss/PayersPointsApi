from django.db.models import Sum

from .models import Transaction


def get_balance() -> dict:
    balance = Transaction.objects.values('payer') \
        .annotate(total_points=Sum('points')) \
        .values('payer', 'total_points')
    return {item['payer']: item['total_points'] for item in balance}


def point_counter(transactions, points_to_spend):
    balance_dict = get_balance()
    new_balance = balance_dict.copy()
    spent_points_list = []

    for transaction in transactions:
        payer = transaction.payer
        points = min(points_to_spend, transaction.points)
        new_balance[payer] -= points
        points_to_spend -= points

        if points_to_spend == 0:
            break

    for i in new_balance:
        payer = i
        points = new_balance[i] - balance_dict[i]
        transaction = Transaction(payer=payer, points=points)
        spent_points_list.append({'payer': payer, 'points': points})
        transaction.save()
    return spent_points_list