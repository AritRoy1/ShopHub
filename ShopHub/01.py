# Implement a group_by_owners function that:
# Accepts a dictionary containing the file owner name for each file name.
# Returns a dictionary containing a list of file names for each owner name, in any order.

# For example, for dictionary 
# {'Input.txt': 'Randy', 'Code.py': 'Stan', 'Output.txt': 'Randy'}
# the group_by_owners function should return 
# {'Randy': ['Input.txt', 'Output.txt'], 'Stan': ['Code.py']}.



def group_by_owners(dict_file):
    
    demo_dict = {}
    for key, value in dict_file.items():
        if value in demo_dict:
            demo_dict[value] = demo_dict[value]+[key]
        else:
            demo_dict[value] = [key]
    
    return demo_dict
    
    
dict_file = {'Input.txt': 'Randy', 'Code.py': 'Stan', 
             'Output.txt': 'Randy', 'test1.py': 'athar', 'test2': 'arit', 'test3':'athar'}
print(group_by_owners(dict_file))
