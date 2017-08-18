''' Generate truly random numbers with the 
random.org API (https://www.random.org/clients/http/)'''

import requests
import json

base_url = "https://www.random.org/"

    
def rand_int(num, min, max, base=10, format="plain", rnd="new"):
    """A function to generate a truly random integer.

    Args:
        num (int): The number of random numbers to generate
        min (int): The minimum value of the random number
        max (int): The maximum value of the random number
        base (int): The base of the number when printing
        format (String): The format to prin the number in, html | plain
        rnd (String): What seed to use to generate rand number, new | id.identifier | date.iso-date

    Returns:
        list: A list of random integers in unicode text format
        None: None if there was a failure

    TODO: Handle all response codes
    """

    # Always set num columns to 1, we can parse out the values
    col = 1
    url = '{}integers/?num={}&min={}&max={}&col={}&base={}&format={}&rnd={}'.format(base_url, num, min, max, col, base, format, rnd)
    print(url)
    r = requests.get(url)
    if r.status_code != 200:    # TODO: Handle all error codes
        print("{}".format(r.text))
        return None

    text = r.text
    return [int(s.strip()) for s in text.splitlines()]


def main():
    print(rand_int(1,1,100, 1))
    print(rand_int(3,1,100))

if __name__ == "__main__": main()







