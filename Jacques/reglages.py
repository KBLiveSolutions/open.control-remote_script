compensation = 0.04

""" Reglage des valeurs min et max du tempo """

tempo={
    "min": 60,
    "max":180
    }


""" Reglage des pattern de preset du Silencer 
1 = Step jouee
0 = Step mutee"""

pattern1 = [1, 1, 1, 1, 1, 1, 1, 1]
pattern2 = [1, 0, 1, 0, 1, 0, 1, 0]
pattern3 = [1, 1, 1, 1, 0, 0, 0, 0]
pattern4 = [1, 1, 0, 0, 0, 0, 0, 0]
pattern5 = [1, 1, 0, 0, 1, 1, 0, 0]
pattern6 = [1, 0, 0, 0, 1, 0, 0, 0]
pattern7 = [0, 0, 0, 0, 0, 0, 0, 0]

""" reglage des valeurs par defaut des 4 pedales, en temps (4 = 1Bar)"""

rec_length = [4, 8, 16, 32]

""" 
Reglage des valeurs de Xbar possible a partir des boutons de Rec des Loop (gros carres de 1 à 14) quand CHUT + Silencer Preset est actif
1/16 | 1/8 | 1/4 | 1/2 | 1 Bar | 2 Bars | 3 Bars | 4 Bars | 6 Bars | 8 Bars | 12 Bars | 16 Bars | 24 Bars | 32 Bars 
pour changer les valeurs possibles, le faire dans la liste ci-dessous """

Xbar_values = [4* 1/16, 4* 1/8, 4* 1/4, 4* 1/2, 4* 1, 4* 2, 4* 3, 4* 4, 4* 6, 4* 8, 4* 12, 4* 16, 4* 24, 4* 32]


""" CONTROLEURS SENDS [CC, Canal] """
sends_groups = {
    "GroupA": {
    "sendA": [1, 2],
    "sendB": [3, 2],
    "sendC": [5, 2],
    "sendD": [7, 2],
    "sendE": [9, 2],
    "sendF": [1, 7],
    "sendG": [1, 7],
    "sendH": [1, 7],
    "sendI": [1, 7],
    "sendJ": [1, 7],
    "sendK": [1, 7],
    "sendL": [1, 7]
    },

    "GroupB": {
    "sendA": [15, 7],
    "sendB": [17, 7],
    "sendC": [19, 7],
    "sendD": [21, 7],
    "sendE": [23, 7],
    "sendF": [25, 7],
    "sendG": [1, 7],
    "sendH": [1, 7],
    "sendI": [1, 7],
    "sendJ": [1, 7],
    "sendK": [1, 7],
    "sendL": [1, 7]
    },

    "GroupC":{
    "sendA": [29, 7],
    "sendB": [31, 7],
    "sendC": [33, 7],
    "sendD": [35, 7],
    "sendE": [37, 7],
    "sendF": [39, 7],
    "sendG": [1, 7],
    "sendH": [1, 7],
    "sendI": [1, 7],
    "sendJ": [1, 7],
    "sendK": [1, 7],
    "sendL": [1, 7]
    }
}

""" ARMEMENT PISTE INPUT [CC, Canal] """

inputs_arm = {
1: [74, 2],
2: [76, 2],
3: [78, 2],
4: [80, 2],
5: [82, 2],
6: [84, 2],
7: [86, 2],
8: [88, 2],
}

""" MACROS PISTE INPUT GROUPE [CC, Canal] """

macros_inputs = {
1: [73, 2],
2: [75, 2],
3: [77, 2],
4: [79, 2],
5: [81, 2],
6: [83, 2],
7: [85, 2],
8: [87, 2],
}

""" PIERRADE INSTRU 1 MACROS [CC, Canal]
entrer ici les CCs des macros et des selecteurs de chain. syntaxe:

instrus = {
"numero instru":{numero_macro: [CC, Canal],
numero_macro: [CC, Canal],
numero_macro: [CC, Canal],
etc...

ne changer QUE CC et Canal

""" 
instrus = {
"1": {1: [1, 8],
    2: [2, 8],
    3: [3, 8],
    4: [4, 8],
    5: [5, 8],
    6: [6, 8],
    7: [7, 8],
    8: [8, 8],
    9: [9, 8],
    10: [10, 8],
    11: [11, 8],
    12: [12, 8],
    13: [13, 8],
    14: [14, 8],
    15: [15, 8],
    16: [16, 8], 
    "chain_selector_notes": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 , 15],
    "chain_selector_channel": 8
    }, 
"2": {1: [1, 9],
    2: [2, 9],
    3: [3, 9],
    4: [4, 9],
    5: [5, 9],
    6: [6, 9],
    7: [7, 9],
    8: [8, 9],
    9: [9, 9],
    10: [10, 9],
    11: [11, 9],
    12: [12, 9],
    13: [13, 9],
    14: [14, 9],
    15: [15, 9],
    16: [16, 9], 
    "chain_selector_notes": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 , 15],
    "chain_selector_channel": 9
    },  
"3": {1: [1, 10],
    2: [2, 10],
    3: [3, 10],
    4: [4, 10],
    5: [5, 10],
    6: [6, 10],
    7: [7, 10],
    8: [8, 10],
    9: [9, 10],
    10: [10, 10],
    11: [11, 10],
    12: [12, 10],
    13: [13, 10],
    14: [14, 10],
    15: [15, 10],
    16: [16, 10], 
    "chain_selector_notes": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 , 15],
    "chain_selector_channel": 10
    },   
"4": {1: [1, 11],
    2: [2, 11],
    3: [3, 11],
    4: [4, 11],
    5: [5, 11],
    6: [6, 11],
    7: [7, 11],
    8: [8, 11],
    9: [9, 11],
    10: [10, 11],
    11: [11, 11],
    12: [12, 11],
    13: [13, 11],
    14: [14, 11],
    15: [15, 11],
    16: [16, 11], 
    "chain_selector_notes": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 , 15],
    "chain_selector_channel": 11
    }   
}

