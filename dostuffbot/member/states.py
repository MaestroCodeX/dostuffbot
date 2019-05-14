STATE_INDEX = 0


def state():
    global STATE_INDEX
    STATE_INDEX += 1
    return STATE_INDEX


START_MENU = state()
SETTINGS = state()
COMMAND_MENU = state()
SEND_CALLER = state()
SEND_MESSAGE = state()
CHOOSE_COMMAND_OPTION = state()
DELETE_CONFIRM = state()
BACK = state()
