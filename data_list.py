# codes of the variables used in main file

# IP address of the pepper
PEPPER_IP = '192.168.1.188'

# the width and the height of the screen
FRAME_WIDTH = 1280
FRAME_HEIGHT = 800
DEFAULT_VOLUME = 100

# dictionary of the boundaries
TOUCH_LIST = dict()
TOUCH_LIST['RIGHT_SIDE'] = {"x": [FRAME_WIDTH / 2, FRAME_WIDTH], "y": [0, FRAME_HEIGHT], "name": "RIGHT_SIDE"}
TOUCH_LIST['LEFT_SIDE'] = {"x": [0, FRAME_WIDTH], "y": [0, FRAME_HEIGHT], "name": "LEFT_SIDE"}
TOUCH_LIST['JESNK_SIDE'] = {"x": [0, 200], "y": [0, 200], "name": "JESNK_SIDE"}
TOUCH_LIST['BUTTON_LEFT'] = {"x": [75, 600], "y": [233, 593], "name": "BUTTON_LEFT"}
TOUCH_LIST['BUTTON_RIGHT'] = {"x": [669, 1192], "y": [227, 598], "name": "BUTTON_RIGHT"}
TOUCH_LIST['BUTTON_MIDDLE_DOWN'] = {"x": [485, 800], "y": [632, 705], "name": "BUTTON_MIDDLE_DOWN"}
TOUCH_LIST['BUTTON_RIGHT_DOWN'] = {"x": [930, 1156], "y": [641, 707], "name": "BUTTON_RIGHT_DOWN"}
TOUCH_LIST['BUTTON_LEFT_DOWN'] = {"x": [150, 390], "y": [621, 707], "name": "BUTTON_LEFT_DOWN"}

# dictionary of the data of the scene
SCENES = dict()
SCENES['init'] = ['init', ['RIGHT_SIDE', 'LEFT_SIDE'], ['bye', 'next', 'first']]
SCENES['1'] = ['1', ['RIGHT_SIDE', 'LEFT_SIDE'], ['bye', 'next', 'first']]
SCENES['exit'] = ['exit', [], []]

SCENES['home'] = ['home', ['BUTTON_MIDDLE_DOWN', 'JESNK_SIDE'], ['start', 'cheese', 'pepper', 'hello']]

SCENES['first_menu'] = ['first_menu', \
                            ['JESNK_SIDE', 'BUTTON_RIGHT', 'BUTTON_LEFT', \
                             'BUTTON_MIDDLE_DOWN', 'BUTTON_RIGHT_DOWN'], ['bye', 'next', 'first']]

SCENES['tour'] = ['tour', \
                      ['JESNK_SIDE', 'BUTTON_RIGHT', 'BUTTON_LEFT', \
                       'BUTTON_LEFT_DOWN', 'BUTTON_MIDDLE_DOWN', 'BUTTON_RIGHT_DOWN'], \
                      ['bye', 'next', 'first']]

SCENES['entertain'] = ['entertain', \
                           ['JESNK_SIDE', 'BUTTON_RIGHT', 'BUTTON_LEFT', \
                            'BUTTON_LEFT_DOWN', 'BUTTON_MIDDLE_DOWN', 'BUTTON_RIGHT_DOWN'], \
                           ['bye', 'next', 'first']]

SCENES['entertain2'] = ['entertain2', \
                            ['JESNK_SIDE', 'BUTTON_RIGHT', 'BUTTON_LEFT', \
                             'BUTTON_LEFT_DOWN', 'BUTTON_MIDDLE_DOWN', 'BUTTON_RIGHT_DOWN'], \
                            ['bye', 'next', 'first']]

SCENES['tour_hsr1'] = ['tour_hsr1', \
                           ['JESNK_SIDE', 'BUTTON_RIGHT', 'BUTTON_LEFT', \
                            'BUTTON_LEFT_DOWN', 'BUTTON_MIDDLE_DOWN', 'BUTTON_RIGHT_DOWN'], \
                           ['bye', 'next', 'first']]

SCENES['tour_hsr2'] = ['tour_hsr2', \
                           ['JESNK_SIDE', 'BUTTON_RIGHT', 'BUTTON_LEFT', \
                            'BUTTON_LEFT_DOWN', 'BUTTON_MIDDLE_DOWN', 'BUTTON_RIGHT_DOWN'], \
                           ['bye', 'next', 'first']]
