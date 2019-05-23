from enum import Enum, EnumMeta, unique


class ChoicesEnumMeta(EnumMeta):
    def __iter__(self):
        return ((choice.name, choice.value) for choice in super().__iter__())


@unique
class ChoicesEnum(Enum, metaclass=ChoicesEnumMeta):
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def contains(cls, enum_name):
        return any(enum_name == value for name, value in cls)


class DeepCommand:
    COMMANDS = 'commands'
    NOTIFY = 'notify'


class CommandMessageType(ChoicesEnum):
    TEXT = 'TEXT'
    PHOTO = 'PHOTO'
    DOCUMENT = 'DOCUMENT'
    VIDEO = 'VIDEO'
    AUDIO = 'AUDIO'
    VOICE = 'VOICE'
    LOCATION = 'LOCATION'


class CommandStatus(ChoicesEnum):
    DONE = 'DONE'
    EDIT_CALLER = 'EDIT_CALLER'
    EDIT_ANSWER = 'EDIT_ANSWER'


class CommandMutationMode(ChoicesEnum):
    ADDING = 'ADDING'
    EDITING = 'EDITING'
