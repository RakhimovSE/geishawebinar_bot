from scripts.warehouse import Warehouse

wh = Warehouse()

print(wh._get_df())
print(wh.get_payment())
print(wh.get_if_not_pay())
print(wh.get_next_day_first())
print(wh.get_next_day_second())