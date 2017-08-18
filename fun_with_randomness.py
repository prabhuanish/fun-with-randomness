''' Generate truly random numbers with the 
random.org API (https://www.random.org/clients/http/)'''

import requests
import json
from PIL import Image
import time

base_url = "https://www.random.org/"
max_request_size = 10000

def create_rgb_bitmap(width, height):
    """A function to randomly generate a rgb bitmap using PIL for easy visualization.

    Args:
        width (int): The width in pixels of the rgb bitmap
        height (int): The height in pixels of the rgb bitmap

    Returns:
        Image: A PIL Image of the generated rgb bitmap if success
    """   
    assert (width > 0 and height > 0)

    # Generate random values for all pixel intensities
    num_pixels, num_generated = 3 * width * height, 0
    rand_vals = []

    # Pull in chunks of the max request size until we have enough pixel vals
    while num_generated < num_pixels:
        if (num_pixels - num_generated < max_request_size):
            to_add = rand_int(num_pixels - num_generated, 0, 255)
        else:
            to_add = rand_int(max_request_size, 0, 255)

        # Ensure that the request was successfull
        if (to_add != None):
            num_generated += len(to_add)
            rand_vals += to_add
        
        # Add short delay between requests -- don't want to overload server
        time.sleep(1) 


    pixel_vals = [(rand_vals[i], rand_vals[i+1], rand_vals[i+2]) for i in range(0, num_pixels, 3)]

    # Create a black image with proper dimensions
    img = Image.new('RGB', (width, height))
    pixels = img.load()

    # Change pixel values to our randomly generated pixel intensities
    for i in range(img.size[0]):    
        for j in range(img.size[1]): 
            pixels[i,j] = pixel_vals[width*i + j]

    return img

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
    r = requests.get(url)
    if r.status_code != 200:    # TODO: Handle all error codes
        print("{}".format(r.text))
        return None

    text = r.text
    return [int(s.strip()) for s in text.splitlines()]



def main():
    # Demo: Print out 10 with random numbers
    rand_numbers = rand_int(10,1,100)
    print(rand_numbers)

    # Demo: Create a 128x128 bitmap with randomly generated pixel values
    img = create_rgb_bitmap(128, 128)
    img.show()

if __name__ == "__main__": main()







