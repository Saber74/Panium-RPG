import pickle as p
person = {"John": [15, "Murderer"], "Sally": 16}
print(person)
p.dump(person, open("people.txt", "wb"))
people = p.load(open("people.txt", 'rb'))
print(people)