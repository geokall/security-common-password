import nacl.pwhash
import nacl.hash
from argon2 import PasswordHasher


# def test_hashing():
#
# password = b'stronk-password'
# hashed = nacl.pwhash.str(password)
# print(hashed)
#
# wrong_password = b'qwerty123'
#
# try:
#     res = nacl.pwhash.verify(hashed, wrong_password)
#     print(res)
# except:
#     print('false')

# def hash_examples(password):
#     ph = PasswordHasher()
#     hashed = ph.hash(password)
#     print(hashed)


def load_user_passwords(file_to_read, file_to_write):
    ph = PasswordHasher()
    file_r = open(file_to_read, 'r')
    file_w = open(file_to_write, 'w')
    for line in file_r.readlines():
        tokens = line.replace('\n', '').split(' ')
        # file_w.write('{} {}\n'.format(tokens[0], nacl.pwhash.str(tokens[1].encode('utf-8'))))
        file_w.write('{} {}\n'.format(tokens[0], ph.hash(tokens[1].encode('utf-8'))))
    file_r.close()
    file_w.close()

def compare_hashes(input_hash, pwd_to_hash):
    if not pwd_to_hash:
        return False
    sha256 = nacl.hash.sha512(pwd_to_hash.encode('utf-8')).decode('utf-8')
    if input_hash == sha256:
        return True
    sha512 = nacl.hash.sha512(pwd_to_hash.encode('utf-8')).decode('utf-8')
    if input_hash == sha512:
        return True
    blake2b = nacl.hash.blake2b(pwd_to_hash.encode('utf-8')).decode('utf-8')
    if input_hash == blake2b:
        return True
    return False

def hash(input_hash, pwd_to_hash):
    ph = PasswordHasher()
    hashed = ph.hash(pwd_to_hash.encode('utf-8').decode('utf-8'))
    print(hashed)
    print(input_hash)
    if input_hash == hashed:
        return True


if __name__ == '__main__':
    load_user_passwords('user-base.txt', 'user-hashes.txt')
    file_bob = open('user-hashes.txt', 'r')
    file_eve = open('common-passwords.txt', 'r')
    common_passwords = []
    for line in file_eve.readlines():
        common_passwords.append(line.replace('\n', ''))
    file_eve.close()
    for user_lines in file_bob.readlines():
        for pwd in common_passwords:
            tokens = user_lines.replace('\n', '').split(' ')
            if hash(tokens[1], pwd):
                print('User {} has password {}'.format(tokens[0], pwd))
    file_bob.close()
