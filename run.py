import model
import datetime

# Change the values below to query the model
cycle = 26
new_sym = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

result = model.predict(new_sym, cycle)
days = result["cycle_length_initial"] - result["current_day"]
today = datetime.date.today()
d1 = today + datetime.timedelta(days=1)
print(d1.strftime("%d/%m/%Y"))


# Uncomment this to test the model
# model.test()