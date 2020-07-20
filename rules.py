

from models import ColorHat

str_rule = "The  rule : {} is not valided"
def sequ_bool(liste, message):
    if liste[0]:
        return all([r for r in liste[1:]]), message
    else :
        return True , message
def sequ_rules(liste):
    #print(liste)
    for m in liste :
        #print(m[0])
        if not(m[0]):
            #print(m[1])
            return False ,str_rule.format(m[1])
    return True , ""
def Chara_rules():
    '''
    Description :
        All rules to follow for data creation 
    '''
    
    
    def Age(char):
        
        r1 =  (int(char['Age']) > 0, " 'Age' > 0" )

        r21 = int(char['Weight']) > 80 
        r22 = int(char['Age']) > 10
        r2 = sequ_bool([r21, r22]," 'Weight' > 80  ->  'Age' > 10 " )

        rules =[r1,r2]
        return sequ_rules(rules)

    def Hat(char):
        
        r11 = not(char['Human'])
        r12 = char['Hat'] is None
        r1  = sequ_bool([r11,r12],"Only human have Hat" )

        r21 = 'p' in char['Name'].lower()
        r22 =  ColorHat['YELLOW'] is not char['Hat'].Color
        r2 = sequ_bool([r21,r22],"Patrick is not allowed to possess YELLOW hat" )

        r3 = ColorHat[char['Hat'].Color.value], " This Color is not available "

        rules =[r1,r2,r3]
        return sequ_rules(rules)


    local =locals()

    return { key : value    for key ,value in local.items() if (callable(value)) and (value.__module__ ==__name__)}
#print(rule())


Character_rules = Chara_rules()

