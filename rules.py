

from models import ColorHat
def Chara_rules():

    str_rule = "The  rule : {} is not valided"

    def Age(char):
        assert char['Age'] > 0 ,str_rule.format(" 'Age' > 0" )
        if char['Wheight'] > 80:
            assert char['Age'] > 10, str_rule.format(" 'Weight' > 80  ->  'Age' > 10 " ) 
        return True

    def Hat(char):
        if not char['Human']:
            assert char['Hat'] == 'null',str_rule.format("Only human have Hat")

        if 'p' in char['Name']:
            assert ColorHat('YELLOW') is not char['Hat'].Color , str_rule.format("Only human have Hat")
        return True

    #add new rule

    local =locals()

    return { key : value    for key ,value in local.items() if (callable(value)) and (value.__module__ ==__name__)}
#print(rule())


Character_rules = Chara_rules()
#from copy import copy
