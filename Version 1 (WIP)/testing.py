def _printlist(list):
    if list == None:
        print("None")
        return
    for i in list:
        print(i)



import effect_modules.simple_effects.api as simple_effects


effects_file = open("effects_test.txt", 'r')
x = simple_effects.get_segment_blueprints_list(effects_file)
effects_file.close()
_printlist(x)

