import model
import datetime

today = datetime.date.today()

# dd/mm/YY

cycle = 26
new_sym = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

result = model.predict(new_sym, cycle)
print (result)
days = result["cycle_length_initial"] - result["current_day"]

d1 = today + datetime.timedelta(days=1)
print(d1.strftime("%d/%m/%Y"))
