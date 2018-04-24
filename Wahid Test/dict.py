import pickle as p
person = {"lvl": 1,
		  "Coords": [0,0],
		  "Inventory": []}
print(person)
p.dump(person, open("people.txt", "wb"))
people = p.load(open("people.txt", 'rb'))
people["Inventory"].append("HI")
print(people["Inventory"])