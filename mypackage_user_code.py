import mypackage as mp

mp.print(dir(mp))
print(mp.ManagedCreator.manager)
# print(mp.Creator.manager)           # AttributeError: type object 'Creator' has no attribute 'manager'
# print(mp.Manager.Creator.manager)   # AttributeError: type object 'Creator' has no attribute 'manager'


