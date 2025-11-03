# type Person = dict[str, str | int | dict[str, str]]


# person: Person = {
#     "name": "John",
#     "age": 30,
#     "city": "New York",
#     "address": {
#         "street": "123 Main St",
#         "city": "New York",
#         "state": "NY"
#     }
# }

# print(person)
# print(person["name"])
# print(person["age"])
# print(person["city"])
# print(person["address"])
# print(person["address"]["street"])
# print(person["address"]["city"])
# print(person["address"]["state"])
from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int | str
    city: str
    address: dict[str, str]

person: Person = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY"
    }
}

print(person)
print(person["name"])
print(person["age"])
print(person["city"])
print(person["address"])
print(person["address"]["street"])
print(person["address"]["city"])
print(person["address"]["state"])