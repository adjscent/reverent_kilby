print ("Loading Models...")
import model
import datetime

# Change the values below to query the model
# cycle = 26
# new_sym = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
# 26
# 50 50 0 12 20 32 40 50 60 50

print ("Enter your Cycle Length:")
cycle = int(input())
print ("Enter your pain levels for today from 0 to 100 for the 10 symptoms, seperated by spaces")
new_sym = [int(x) for x in input().split(" ")]

result = model.predict(new_sym, cycle)
days = result["cycle_length_initial"] - result["current_day"]
today = datetime.date.today()
d1 = today + datetime.timedelta(days=1)
print("Your next cycle will be at " + d1.strftime("%d/%m/%Y"))

# Uncomment this to test the model
# model.test()