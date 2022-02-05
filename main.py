import argon2
from argon2 import PasswordHasher


def load_user_passwords_and_write_hashed_passwords(file_to_read, file_to_write):
    argon = PasswordHasher()

    read_file = open(file_to_read, 'r')
    write_file = open(file_to_write, 'w')

    for file_line in read_file.readlines():
        split = file_line.replace('\n', '').split(' ')
        write_file.write('{} {}\n'.format(split[0], argon.hash(split[1])))

    read_file.close()
    write_file.close()


def argon_verify_by(input_hash, pwd_to_hash, argon):
    if not pwd_to_hash:
        return False

    try:
        if argon.verify(input_hash, pwd_to_hash):
            return True
    except argon2.exceptions.VerifyMismatchError:
        return False

    return False


if __name__ == '__main__':
    argon_ph = PasswordHasher()

    load_user_passwords_and_write_hashed_passwords('user-plain-text-password.txt', 'user-hashed-password.txt')
    leaked_passwords = open('leaked-passwords.txt', 'r')
    hashed_passwords = open('user-hashed-password.txt', 'r')

    common_passwords = []

    for line in leaked_passwords.readlines():
        common_passwords.append(line.replace('\n', ''))

    leaked_passwords.close()

    for user_lines in hashed_passwords.readlines():
        for pwd in common_passwords:
            tokens = user_lines.replace('\n', '').split(' ')

            if argon_verify_by(tokens[1], pwd, argon_ph):
                print('Password leaked!!! Hackers revealed password: {} for User: {}'.format(pwd, tokens[0]))

    hashed_passwords.close()
