from __future__ import absolute_import, print_function, unicode_literals


############################################
######## Launchpad MK2
############################################
# CHANNEL = 13
#
# UP_BUTTON = ('MIDI_CC_TYPE', 104)
# UP_BUTTON_COLOR = {'off': 'black', 'half': 'half_yellow', 'on': 'yellow', 'white': 'white'}
# DOWN_BUTTON = ('MIDI_CC_TYPE', 105)
# DOWN_BUTTON_COLOR = {'off': 'black', 'half': 'half_yellow', 'on': 'yellow', 'white': 'white'}
# LEFT_BUTTON = ('MIDI_CC_TYPE', 106)
# RIGHT_BUTTON = ('MIDI_CC_TYPE', 107)
# SELECT_BUTTON = ('MIDI_NOTE_TYPE', 19)
# SELECT_BUTTON_COLOR = {'off': 'black', 'half': 'half_yellow', 'on': 'yellow'}
# STOP_ALL_CLIPS_BUTTON = ('MIDI_NOTE_TYPE', 49)
# STOP_ALL_CLIPS_BUTTON_COLOR = {'off': 'black', 'half': 'half_red', 'on': 'red'}
# PLAY_BUTTON = ('MIDI_NOTE_TYPE', 39)
# PLAY_BUTTON_COLOR = {'off': 'black', 'half': 'half_green', 'on': 'green'}
# RESTART_BUTTON = ('MIDI_NOTE_TYPE', 29)
# RESTART_BUTTON_COLOR = {'off': 'black', 'half': 'marine', 'on': 'marine'}
# DELETE_BUTTON = ('MIDI_NOTE_TYPE', 79)
# DELETE_BUTTON_COLOR = {'off': 'black', 'half': 'half_orange', 'on': 'orange'}
# NEW_BUTTON = ('MIDI_NOTE_TYPE', 89)
# NEW_BUTTON_COLOR = {'off': 'black', 'half': 'half_blue', 'on': 'blue'}
# MODE_BUTTON = ('MIDI_NOTE_TYPE', 69)
# MODE_BUTTON_COLOR = {'off': 'black', 'half': 25, 'on': 66}

############################################
######## Launchpad X
############################################
CHANNEL = 0
LP_sysex = 12
MODEL = 'X'

############################################
######## Launchpad Mini MK3
############################################
# CHANNEL = 0
# MODEL = 'MiniMK3'
# LP_sysex = 13


UP_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 91, 'COLOR': {'off': 'black', 'half': 'half_yellow', 'on': 'yellow', 'white': 'white'}}
DOWN_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 92, 'COLOR': {'off': 'black', 'half': 'half_yellow', 'on': 'yellow', 'white': 'white'}}
LEFT_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM':  93}
RIGHT_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 94}
SHIFT_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 19, 'COLOR': {'off': 'black', 'half': 'half_white', 'on': 'white'}}
STOP_ALL_CLIPS_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 49, 'COLOR': {'off': 'black', 'half': 'half_red', 'on': 'red'}}
PLAY_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 39, 'COLOR': {'off': 'black', 'half': 'half_green', 'on': 'green'}}
RESTART_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 29, 'COLOR': {'off': 'black', 'half': 'half_marine', 'on': 'marine'}}
MODE_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 89, 'COLOR': {'off': 'black', 'session': 66, 'arrangement': 25, 'looper':'yellow'}}
NEW_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 79, 'COLOR': {'off': 'black', 'half': 'half_blue', 'on': 'blue'}}
DELETE_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 69, 'COLOR': {'off': 'black', 'half': 'half_orange', 'on': 'orange'}}
RECORD_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 98, 'COLOR': {'off': 'black', 'half': 'half_red', 'on': 'red'}}
LOOP_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 59, 'COLOR': {'off': 'black', 'half': 'half_yellow', 'on': 'yellow'}}
NOTE_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 50, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
SESSION_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': -1, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
UNDO_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': -1, 'COLOR': {'off': 'black', 'half': 'high', 'on': 'high'}}
NEXT_SCENE_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': -1, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
PREV_SCENE_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': -1, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
LAYOUT_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': -1, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}

############################################
######## Launchpad
############################################

PAD_MATRIX = [81, 82, 83, 84, 85, 86, 87, 88,\
71, 72, 73, 74, 75, 76, 77, 78,\
61, 62, 63, 64, 65, 66, 67, 68,\
51, 52, 53, 54, 55, 56, 57, 58,\
41, 42, 43, 44, 45, 46, 47, 48,\
31, 32, 33, 34, 35, 36, 37, 38,\
21, 22, 23, 24, 25, 26, 27, 28,\
11, 12, 13, 14, 15, 16, 17, 18]

############################################
######## Common Launchpad
############################################

CONTROLLER = 'LP'

COLOR_INDEX_L10 = {0	:	107	, 1	:	96	, 2	:	100	, 3	:	13	, 4	:	86	, 5	:	87	, 6	:	25	, 7	:	33	, 8	:	36	, 9	:	79	, 10	:	92	,
11	:	94	, 12	:	57	, 13	:	3	, 14	:	5	, 15	:	84	, 16	:	15	, 17	:	97	, 18	:	16	, 19	:	76	, 20	:	77	,
21	:	90	, 22	:	78	, 23	:	43	, 24	:	80	, 25	:	55	, 26	:	95	, 27	:	117	, 28	:	10	, 29	:	108	, 30	:	14	,
31	:	8	, 32	:	110	, 33	:	111	, 34	:	88	, 35	:	28	, 36	:	114	, 37	:	115	, 38	:	116	, 39	:	44	, 40	:	119	,
41	:	112	, 42	:	4	, 43	:	11	, 44	:	105	, 45	:	73	, 46	:	74	, 47	:	18	, 48	:	102	, 49	:	104	, 50	:	103	,
51	:	66	, 52	:	93	, 53	:	48	, 54	:	59	, 55	:	70	, 56	:	121	, 57	:	127	, 58	:	126	, 59	:	99	, 60	:	19	,
61	:	64	, 62	:	65	, 63	:	39	, 64	:	47	, 65	:	46	, 66	:	69	, 67	:	81	, 68	:	58	, 69	:	71	,
'half_green': 123,
'green': 122,
'dim_white': 112, #or 71
'dim_white2': 71, #103
'light_white': 117,
'half_white': 117,
'white': 115, #3
'half_orange': 127, #127,
'orange': 10, #126,
'yellow': 124,
'half_yellow': 125,
'blue': 46, #67,
'half_blue': 47, #66,
'black': 0,
'half_red': 121,
'red': 120,
'purple': 44,
'half_purple': 92,
'half_marine': 35,
'marine': 90}

COLOR_INDEX_L9 = {0	:	107	, 1	:	126	, 2	:	97	, 3	:	19	, 4	:	64	, 5	:	65	, 6	:	92	, 7	:	45	, 8	:	46	, 9	:	69	, 10	:	70	,
11	:	71	, 12	:	5	, 13	:	73	, 14	:	74	, 15	:	111	, 16	:	76	, 17	:	77	, 18	:	78	, 19	:	79	, 20	:	80	,
21	:	81	, 22	:	82	, 23	:	99	, 24	:	84	, 25	:	86	, 26	:	16	, 27	:	87	, 28	:	25	, 29	:	90	, 30	:	90	,
31	:	36	, 32	:	81	, 33	:	115	, 34	:	94	, 35	:	95	, 36	:	96	, 37	:	97	, 38	:	13	, 39	:	99	, 40	:	8	,
41	:	2	, 42	:	102	, 43	:	104	, 44	:	103	, 45	:	2	, 46	:	56	, 47	:	107	, 48	:	108	, 49	:	113	, 50	:	110	,
51	:	111	, 52	:	112	, 53	:	28	, 54	:	114	, 55	:	115	, 56	:	96	, 57	:	116	, 58	:	117	, 59	:	119	,
'half_green': 123,
'green': 122,
'dim_white': 112, #117, #or 71
'light_white': 118,
'white': 120,
'half_orange': 127,
'orange': 126,
'yellow': 124,
'half_yellow': 125,
'blue': 67,
'half_blue': 69,
'red': 120,
'half_red': 121,
'black': 0,
'purple': 17,
'half_pruple': 18 }

############################################
######## Common ALL
############################################


zero = [0, 0, 0, 0, 0, 0, 0, 0,\
        0, 0, 1, 1, 1, 0, 0, 0,\
        0, 1, 0, 0, 1, 1, 0, 0,\
        0, 1, 0, 1, 0, 1, 0, 0,\
        0, 1, 0, 1, 0, 1, 0, 0,\
        0, 1, 1, 0, 0, 1, 0, 0,\
        0, 0, 1, 1, 1, 0, 0, 0,\
        0, 0, 0, 0, 0, 0, 0, 0,\
        ]

COLOR_GRID =   ['black',  'black',  'black',  'black',  'black',  'black',  'black', 'black',\
                'black',  'black',  'black',  'black',  'black',  'black',  'black', 'black',\
                'black', 56, 64, 19, 58, 27, 25, 'black',\
                'black', 14,  9,  6, 15, 13, 67, 'black',\
                'black', 12, 10, 47,  1, 55, 68, 'black',\
                'black',  0, 62, 18,  3, 37, 66, 'black',\
                'black',  'black',  'black',  'black',  'black',  'black',  'black', 'black',\
                'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black',\
                ]
############################################
######## Push2
############################################
#
# CONTROLLER = 'Push2'
# CHANNEL = 0
#
# PAD_MATRIX = [92, 93, 94, 95, 96, 97, 98, 99,\
# 84, 85, 86, 87, 88, 89, 90, 91,\
# 76, 77, 78, 79, 80, 81, 82, 83,\
# 68, 69, 70, 71, 72, 73, 74, 75,\
# 60, 61, 62, 63, 64, 65, 66, 67,\
# 52, 53, 54, 55, 56, 57, 58, 59,\
# 44, 45, 46, 47, 48, 49, 50, 51,\
# 36, 37, 38, 39, 40, 41, 42, 43]
#
# UP_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 44, 'COLOR': {'off': 'black', 'half': 'low', 'white': 'high'}}
# DOWN_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 45, 'COLOR': {'off': 'black', 'half': 'low', 'white': 'high'}}
# LEFT_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM':  62}
# RIGHT_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 63}
# SHIFT_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 49, 'COLOR': {'off': 'black', 'half': 'high', 'on': 'high'}}
# STOP_ALL_CLIPS_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 29, 'COLOR': {'off': 'black', 'half': 'half_red', 'on': 'red'}}
# PLAY_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 85, 'COLOR': {'off': 'white', 'half': 'white', 'on': 'green'}}
# RESTART_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 56, 'COLOR': {'off': 'black', 'half': 'high', 'on': 'high'}}
# NEW_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 87, 'COLOR': {'off': 'black', 'half': 'high', 'on': 'high'}}
# DELETE_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 118, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
# RECORD_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 86, 'COLOR': {'off': 'white', 'half': 'white', 'on': 'red'}}
# LOOP_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 117, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
# NOTE_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 50, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
# SESSION_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 51, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
# UNDO_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 119, 'COLOR': {'off': 'black', 'half': 'high', 'on': 'high'}}
# NEXT_SCENE_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 47, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
# PREV_SCENE_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 46, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
# LAYOUT_BUTTON = {'TYPE': 'MIDI_CC_TYPE', 'NUM': 31, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
# MODE_BUTTON =  {'TYPE': 'MIDI_CC_TYPE', 'NUM': -1, 'COLOR': {'off': 'black', 'half': 'low', 'on': 'high'}}
#
#
#
# COLOR_INDEX_L10 = {0	:	1	,
# 1	:	3	,
# 2	:	5	,
# 3	:	7	,
# 4	:	9	,
# 5	:	11	,
# 6	:	13	,
# 7	:	15	,
# 8	:	17	,
# 9	:	19	,
# 10	:	21	,
# 11	:	23	,
# 12	:	25	,
# 13	:	120	,
# 14	:	2	,
# 15	:	4	,
# 16	:	6	,
# 17	:	8	,
# 18	:	10	,
# 19	:	12	,
# 20	:	14	,
# 21	:	16	,
# 22	:	18	,
# 23	:	20	,
# 24	:	22	,
# 25	:	24	,
# 26	:	26	,
# 27	:	42	,
# 28	:	27	,
# 29	:	28	,
# 30	:	5	,
# 31	:	7	,
# 32	:	9	,
# 33	:	10	,
# 34	:	13	,
# 35	:	44	,
# 36	:	46	,
# 37	:	49	,
# 38	:	50	,
# 39	:	34	,
# 40	:	36	,
# 41	:	45	,
# 42	:	28	,
# 43	:	6	,
# 44	:	5	,
# 45	:	7	,
# 46	:	9	,
# 47	:	11	,
# 48	:	13	,
# 49	:	44	,
# 50	:	17	,
# 51	:	21	,
# 52	:	34	,
# 53	:	35	,
# 54	:	24	,
# 55	:	54	,
# 56	:	67	,
# 57	:	69	,
# 58	:	75	,
# 59	:	8	,
# 60	:	12	,
# 61	:	11	,
# 62	:	15	,
# 63	:	20	,
# 64	:	125	,
# 65	:	103	,
# 66	:	107	,
# 67	:	23	,
# 68	:	113	,
# 69	:	121	,
# 'half_green': 23,
# 'green': 126,
# 'dim_white': 119,
# 'light_white': 121,
# 'white': 122,
# 'orange': 4,
# 'yellow': 8,
# 'half_yellow': 19,
# 'black': 0,
# 'half_red': 67,
# 'red': 127,
# 'blue': 18,
# 'low': 10,
# 'high': 127,
#
# 'dim_white2': 112, #103
# 'half_blue': 47, #66,
# 'purple': 44,
# 'half_purple': 92,
# 'half_marine': 39,
# 'marine': 90}
#
#
# COLOR_INDEX_L9 = {0	:	1	,
# 1	:	4	,
# 2	:	4	,
# 3	:	10	,
# 4	:	9	,
# 5	:	13	,
# 6	:	17	,
# 7	:	16	,
# 8	:	17	,
# 9	:	18	,
# 10	:	123	,
# 11	:	118	,
# 12	:	1	,
# 13	:	5	,
# 14	:	10	,
# 15	:	10	,
# 16	:	9	,
# 17	:	12	,
# 18	:	15	,
# 19	:	16	,
# 20	:	20	,
# 21	:	22	,
# 22	:	24	,
# 23	:	4	,
# 24	:	3	,
# 25	:	7	,
# 26	:	8	,
# 27	:	8	,
# 28	:	11	,
# 29	:	14	,
# 30	:	14	,
# 31	:	15	,
# 32	:	19	,
# 33	:	20	,
# 34	:	21	,
# 35	:	25	,
# 36	:	3	,
# 37	:	6	,
# 38	:	6	,
# 39	:	6	,
# 40	:	4	,
# 41	:	9	,
# 42	:	12	,
# 43	:	15	,
# 44	:	17	,
# 45	:	2	,
# 46	:	23	,
# 47	:	2	,
# 48	:	2	,
# 49	:	5	,
# 50	:	7	,
# 51	:	10	,
# 52	:	121	,
# 53	:	11	,
# 54	:	48	,
# 55	:	49	,
# 56	:	26	,
# 57	:	45	,
# 58	:	122	,
# 59	:	120	,
# 'half_green': 23,
# 'green': 126,
# 'dim_white': 119, #or 71
# 'light_white': 118,
# 'white': 120,
# 'orange': 4,
# 'yellow': 13,
# 'half_yellow': 19,
# 'black': 0,
# 'half_red': 121,
# 'red': 120,
# 'low': 10,
# 'high': 127   }
