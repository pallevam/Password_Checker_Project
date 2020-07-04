import requests, sys
import hashlib

def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fetching: {res.status_code}, check the api and try again')
    return res

request_api_data("password123")

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.splitlines)
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    # check password if it exists in API response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print(response)
    return read_res(response)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times, you should probably change your password.')
        else:
            print(f'{password} was not found, you can carry on with you password, as it is safe.')
    return 'Completed!'

if __name__ == '__main__':    
    sys.exit(main(sys.argv[1:]))