class Lookup:
    def __init__(self) -> None:
        self.dictionary = dict()
    
    def register(self, key, data):
        #>todo check effect_data is right type
        self.dictionary[key] = data

    def unregister(self, key):
        self.dictionary.pop(key)
    
    def lookup(self, key):
        return self.dictionary[key]
    
    def get_keys(self):
        return self.dictionary.keys()

   
class EffectDataHotkeyLookup(Lookup):
    pass
