alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

class Rotor:
    def __init__(self, encoding, turnover=[]):
        self.alphabet = alphabet.copy()
        self.encoding = list(encoding)
        self.turnover = turnover

    def rotate_list(self, list, counterclockwise):
        if counterclockwise:
            list.append(list[0])
            list.pop(0)
        else:
            list.insert(0, list[25])
            list.pop(26)
        return list

    def rotate(self, counterclockwise=True):
        self.encoding = self.rotate_list(self.encoding, counterclockwise)
        self.alphabet = self.rotate_list(self.alphabet, counterclockwise)

    def rotor_position(self, setting:str, counterclockwise=True):
        if not setting.isnumeric():
            setting = alphabet.index(setting.upper()) + 1
        for i in range(int(setting) - 1):
            self.rotate(counterclockwise)

    def ring_setting(self, setting:str):
        self.rotor_position(setting, False)
        for i in range(len(self.turnover)):
            offset = alphabet.index(self.turnover[i]) - (int(setting) - 1)
            offset = offset - (int(offset/26)) * 26
            self.turnover[i] = alphabet[offset]