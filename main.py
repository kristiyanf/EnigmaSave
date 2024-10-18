import configparser
import rotor
import save

Rotor = rotor.Rotor
config = configparser.ConfigParser()
alphabet= rotor.alphabet

print("EnigmaSave")
print("----------")

save.input_settings()

rotor_greek, rotor_left, rotor_middle, rotor_right, reflector, plugboard = save.read_config()

# ENCRYPTION

def encrypt(letter):
    letter = letter.upper()

    if letter in alphabet:

        # PLUGBOARD ENCRYPTION

        def encrypt_plugboard(letter):
            for i in plugboard:
                if letter == i[0]:
                    letter = i[1]
                elif letter == i[1]:
                    letter = i[0]
            return letter

        # ROTOR ROTATION

        if rotor_middle.alphabet[0] in rotor_middle.turnover:
            rotor_middle.rotate()
            rotor_left.rotate()
        if rotor_right.alphabet[0] in rotor_right.turnover:
            rotor_middle.rotate()
        rotor_right.rotate()

        # CIRCUIT

        def encrypt_wiring(letter, input, output):
            return output[input.index(letter)]

        letter = encrypt_plugboard(letter)
        letter = encrypt_wiring(letter, alphabet, rotor_right.encoding)
        letter = encrypt_wiring(letter, rotor_right.alphabet, rotor_middle.encoding)
        letter = encrypt_wiring(letter, rotor_middle.alphabet, rotor_left.encoding)
        letter = encrypt_wiring(letter, rotor_left.alphabet, rotor_greek.encoding)
        letter = encrypt_wiring(letter, rotor_greek.alphabet, reflector)
        letter = encrypt_wiring(letter, alphabet, reflector)
        letter = encrypt_wiring(letter, reflector, rotor_greek.alphabet)
        letter = encrypt_wiring(letter, rotor_greek.encoding, rotor_left.alphabet)
        letter = encrypt_wiring(letter, rotor_left.encoding, rotor_middle.alphabet)
        letter = encrypt_wiring(letter, rotor_middle.encoding, rotor_right.alphabet)
        letter = encrypt_wiring(letter, rotor_right.encoding, alphabet)
        letter = encrypt_plugboard(letter) 
        return letter

# RESULT

letter_count = 0
grouping_length = input("Set grouping length (1-n): ")

while(True):
    result = ""
    for i in input("Enter message: "):
        encrypted_letter = encrypt(i)
        if encrypted_letter:
            result = result + encrypted_letter
            letter_count = letter_count + 1
            if grouping_length != "n":
                if letter_count % int(grouping_length) == 0:
                    result = result + " "
    input("Result: " + result)

    # CHANGE ROTOR POSITIONS

    if input("Do you want to change the rotor positions? Yes or no (y/n): ").lower() == "y":
        save.input_configure_rotors("position")
        save.write_config()
        rotor_greek, rotor_left, rotor_middle, rotor_right, reflector, plugboard = save.read_config()
