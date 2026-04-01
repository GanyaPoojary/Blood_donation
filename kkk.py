def update_dict(d):
    print("Original dictionary:", d)
    # Correct usage of update() method with a dictionary
    d.update({'phone': 123456})
    print("Updated dictionary:", d)

my_dict = {'name': 'Bob', 'age': 30}
update_dict(my_dict)
