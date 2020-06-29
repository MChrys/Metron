


def rule():

    str_rule = "The  rule : {} is not valid"

    def Age(char):
        assert char['Age'] > 0 ,str_rule.format(" 'Age' > 0" )
        if char['Wheight'] > 80:
            assert Age > 10, str_rule.format(" 'Weight' > 80  ->  'Age' > 10 " ) 
        return True

    def Hat(char):
        if not char['Human']:
            assert char['Hat'] == 'null',str_rule.format("Only human have Hat is not valid")

        if 'p' in char['Name']:
            assert 'YELLOW' not in char['Hat']['Color'] , str_rule.format("Only human have Hat")
        return True

    #add new rule

    local =locals()

    return { key : value    for key ,value in local.items() if (callable(value)) and (value.__module__ ==__name__)}
#print(rule())


RULES = rule()
#from copy import copy
