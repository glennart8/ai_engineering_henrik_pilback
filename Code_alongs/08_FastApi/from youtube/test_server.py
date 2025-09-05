import requests

# Se alla items
# print(requests.get("http://127.0.0.1:8000/").json())

# ------------

# r1 = requests.get("http://127.0.0.1:8000/items/0")
# print(r1.status_code, r1.json())  # Fungerar

# r2 = requests.get("http://127.0.0.1:8000/items/?name=Nails")
# print(r2.status_code)
# print(r2.text)   # skriv ut rådata istället för .json()

# ------------

# LÄGG TILL ETT ITEM - funkar

# print("Adding an item:")
# print(
#     requests.post(
#         "http://127.0.0.1:8000/",
#         json={"name": "Screwdriver", "price": 3.99, "count": 10, "id": 4, "category": "tools"},
#     ).json()
# )

# print(requests.get("http://127.0.0.1:8000/").json())
# print()

# ------------

# Ta bort ett item FUNKAR

# print("Deleting an item:")
# print(requests.delete("http://127.0.0.1:8000/items/0").json())
# print(requests.get("http://127.0.0.1:8000/").json())

# UPPDATERA ITEM

r = requests.put(
    "http://127.0.0.1:8000/update/0?name=NewHammer&price=12.99&count=25"
)
print(r.status_code)
print(r.json())

print(requests.get("http://127.0.0.1:8000/").json())