def totaler(cost_of_items, discount, credit_amount):
    sub_total = 0.00
    ticket_total = 0.00
    ticket_tax = 0.00
    # global total_tax
    if not cost_of_items:
        return ticket_total, ticket_tax, sub_total,
    if discount == 0:
        for cost in cost_of_items:
            cost_field = cost[1]
            item_total = float(cost_field)
            ticket_total = ticket_total + item_total
        if credit_amount == 0:
            ticket_tax = ticket_total * .07
            sub_total = ticket_tax + ticket_total
            return ticket_total, ticket_tax, sub_total
        elif credit_amount >= 1:
            ticket_after_credit = ticket_total - credit_amount
            ticket_tax = ticket_after_credit * .07
            sub_total = ticket_tax + ticket_after_credit
            return ticket_after_credit, ticket_tax, sub_total
        elif credit_amount != int or float:
            print('error')
            return ticket_total, ticket_tax, sub_total
    elif discount == 100:
        return ticket_total, ticket_tax, sub_total
    else:
        if credit_amount == 0:
            ticket_total, ticket_tax, sub_total = discount_order(cost_of_items, discount)
            return ticket_total, ticket_tax, sub_total
        else:
            ticket_total, ticket_tax, sub_total = discount_order_with_credit(cost_of_items, discount, credit_amount)
            return ticket_total, ticket_tax, sub_total

def taxer(cost_to_be_taxed):
    after_tax = cost_to_be_taxed * .07
    return after_tax

def discount_order(cost_of_items_listed, discount_amount):
    ticket_total = 0.00
    for cost_with_discount in cost_of_items_listed:
        cost_field = cost_with_discount[1]
        item_total = float(cost_field)
        ticket_total = ticket_total + item_total
    discount_float = float(discount_amount)
    discount_percentage = discount_float / 100
    decrease_by = ticket_total * discount_percentage
    new_total = ticket_total - decrease_by
    new_total_float = float(new_total)
    ticket_discounted_tax = ticket_total * .07
    ticket_sub_discounted = ticket_discounted_tax + new_total_float
    return new_total_float, ticket_discounted_tax, ticket_sub_discounted

def discount_order_with_credit(cost_of_items_listed, discount_amount, credit_appied):
    ticket_total = 0.00
    for cost_with_discount in cost_of_items_listed:
        cost_field = cost_with_discount[1]
        item_total = float(cost_field)
        ticket_total = ticket_total + item_total
    discount_float = float(discount_amount)
    discount_percentage = discount_float / 100
    decrease_by = ticket_total * discount_percentage
    total_credited = ticket_total - credit_appied
    new_total = total_credited - decrease_by
    new_total_float = float(new_total)
    ticket_discounted_tax = ticket_total * .07
    ticket_sub_discounted = ticket_discounted_tax + new_total_float
    return new_total_float, ticket_discounted_tax, ticket_sub_discounted

def discount_item(cost_of_list_item, discount_to_apply):
    cost_of_as_float = float(cost_of_list_item)
    discount_as_float = float(discount_to_apply)
    discount_as_percentage = discount_as_float / 100
    cost_deducted = discount_as_percentage * cost_of_as_float
    new_item_cost = cost_of_as_float - cost_deducted
    tax_after_discount = new_item_cost * .07
    new_item_cost = "{:.2f}".format(new_item_cost)
    tax_after_discount = "{:.2f}".format(tax_after_discount)
    new_cost_str = str(new_item_cost)
    tax_after_str = str(tax_after_discount)
    return new_cost_str, tax_after_str

