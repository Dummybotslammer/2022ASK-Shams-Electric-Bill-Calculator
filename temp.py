def ask(answers):
 answer = input()
 if str(answer).lower() in answers:
  return answer
 else:
  temp = ask(answers)
  return temp
  
def get_kwh():
 answer = input("Enter Kwh for the appliance: ")
 try:
  answer =  float(answer)
  return answer
 except:
  print("Input must be a number. Press Enter to continue.")
  input()
  temp = get_kwh()
  return temp
  
def get_hours():
 answer = input("Enter Hours used for the appliance: ")
 try:
  answer =  float(answer)
  return answer
 except:
  print("Input must be a number. Press Enter to continue.")
  input()
  temp = get_kwh()
  return temp
  
def edit():
 global bill
 name = input("Enter the name of the appliance you want to edit, or type 'Q_u' to cancel: ")
 if name == "Q_u":
  return 0
 elif name in bill.invoice:
  new_name = input("Enter the new name for the appliance: ")
  kwh = get_kwh()
  hours = get_hours()
  bill.invoice[new_name] = [kwh, hours]
  if not name == new_name:
   del bill.invoice[name]
 else:
  print("Sorry, the name you entered was not found. Press Enter to continue. ")
  input()
  edit()
  
def add_item():
 global bill
 name = input("Enter the name for the appliance, or type 'Q_u' to cancel: ")
 if name == "Q_u":
  return 0
 else:
  if name not in bill.invoice:
   kwh = get_kwh()
   hours = get_hours()
   bill.invoice[name] = [kwh, hours]
  else:
   print("This name is already taken. Please use another one. Press Enter to continue.")
   input()
   add_item()

def remove_item():
 global bill
 name = input("Enter the name of the device you want to remove, or type 'Q_u' to cancel: ")
 if name == "Q_u":
  return 0
 else:
  if name in bill.invoice:
   del bill.invoice[name]
  else:
   print("Sorry, the name you entered was not found. Press Enter to continue. ")
   input()
   remove_item()
   
class ElectricalBill():
 def __init__(self):
  self.invoice = {}
  
 def add_to(self, lst, val):
  lst.append(val)
  
 def change(self, lst, idx, val):
  lst[idx] = val.copy()
  
 def remove(self, lst, idx):
  lst.pop(idx)
   
def run():
  global bill
  bill = ElectricalBill()
    
  while True:
   print("Enter A to add new appliance, E to edit appliances, C to check appliances, R to remove appliances, and P to checkout: ")
   ans = ask(["a", "c", "r", "e", "p"])
   
   if ans.lower() == "a":
    add_item()
    
   elif ans.lower() == "e":
    if bill.invoice:
     edit()
    else:
     print("The bill is empty. Press Enter to continue.")
     input()
     
   elif ans.lower() == "c":
    if bill.invoice:
     for key in bill.invoice:
      print(f"{key}: {bill.invoice[key][0]} kwh, {bill.invoice[key][1]} hours used;")
    else:
     print("The bill is empty. Press Enter to continue.")
     input()
     
   elif ans.lower() == "r":
    if bill.invoice:
     remove_item()
    else:
     print("The bill is empty. Press Enter to continue.")
     input()
     
   elif ans.lower() == "p":
    if bill.invoice:
     
     total = 0
     for item in bill.invoice:
      less = bill.invoice[item][0] * bill.invoice[item][1]
      more = less - 200
      if more > 0:
        total += more * 0.492
      total += less * 0.218
     total = format(total, "f")
     print(f"The total is: RM{total}. Thank you for checking out.")
     break
    else:
     print("The bill is empty. Press Enter to continue.")
     input()