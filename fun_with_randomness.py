''' Generate truly random numbers with the 
random.org API (https://www.random.org/clients/http/)'''

import requests
import json
import time

from PIL import Image

import pyaudio
import math
import array
import wave

base_url = "https://www.random.org/"
max_request_size = 10000
max_failed_requests = 10

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
    rand_vals = rand_int(num_pixels, 0, 255)
    if rand_vals == None: return None

    # Create tuples of (r,g,b) values to create our image
    pixel_vals = [(rand_vals[i], rand_vals[i+1], rand_vals[i+2]) for i in range(0, num_pixels, 3)]

    # Create a black image with proper dimensions
    img = Image.new('RGB', (width, height))

    # Change pixel values to our randomly generated pixel intensities
    pixels = img.load()
    for i in range(img.size[0]):    
        for j in range(img.size[1]): 
            pixels[i,j] = pixel_vals[width*i + j]

    return img

def create_white_noise(min_freq=400.0, max_freq=1200.0, duration=3, sampling_rate=44100):
    """A function to generate a truly random integer.

    Args:
        min_freq (int): The minimum range of frequencies to randomly generate
        max_freq (int): The minimum range of frequencies to randomly generate
        duration (int): The duration in seconds of the wav file.
        Sampling Rate (int): The sampling rate, standard is 44100

    Returns:
        None: Creates a WhiteNoise.wav file in cwd
    
    Source: Inspired from http://code.activestate.com/recipes/578168-sound-generator-using-wav-file/
    """

    volume = 50
    data = array.array('h')
    num_chan = 1
    numSamples = sampling_rate * duration

    # Limit so we don't go over our maximum allowance
    rand_freqs = rand_int(numSamples//duration, min_freq, max_freq)

    for i in range(numSamples):
        freq = rand_freqs[i%len(rand_freqs)]
        numSamplesPerCyc = int(sampling_rate / freq)
        sample = 32767 * float(volume) / 100
        sample *= math.sin(math.pi * 2 * (i % numSamplesPerCyc) / numSamplesPerCyc)
        data.append(int(sample))

    f = wave.open('WhiteNoise.wav', 'w')
    f.setparams((num_chan, data.itemsize, sampling_rate, numSamples, "NONE", "Uncompressed"))
    f.writeframes(data.tostring())
    f.close()

def rand_int(num_to_generate, min, max, base=10, format="plain", rnd="new"):
    """A function to generate a truly random integer.

    Args:
        num_to_generate (int): The number of random numbers to generate
        min (int): The minimum value of the random number
        max (int): The maximum value of the random number
        base (int): The base of the number when printing
        format (String): The format to prin the number in, html | plain
        rnd (String): What seed to use to generate rand number, new | id.identifier | date.iso-date

    Returns:
        list: A list of random integers in unicode text format
        None: None if we exceed the max number of failed attempts

    TODO: Handle all response codes
    """

    rand_vals = []
    num_generated = 0
    failed_attempts = 0

    # Pull in chunks of the max request size until we have enough random vals
    while num_generated < num_to_generate:

        # Check if we've exceeded our max number of attempts
        if failed_attempts > max_failed_requests:
            print("Exceeded max number of requests.")
            return None

        if (num_to_generate - num_generated < max_request_size):
            cur_req_size = num_to_generate - num_generated
        else:
            cur_req_size = max_request_size

        # Make a request
        url = '{}integers/?num={}&min={}&max={}&col={}&base={}&format={}&rnd={}'.format(base_url, cur_req_size, min, max, 1, base, format, rnd)
        r = requests.get(url)
        if r.status_code != 200:    # TODO: Handle all error codes
            print("{}".format(r.text))
            failed_attempts += 1
        else:
            num_generated += cur_req_size
            text = r.text
            rand_vals += [int(s.strip()) for s in text.splitlines()]

        # Add short delay between requests -- don't want to overload server
        time.sleep(1) 

    return rand_vals

def main():
    # Demo: Print out 10 random numbers
    rand_numbers = rand_int(10,1,100)
    print(rand_numbers)

    # Demo: Create a 128x128 bitmap with randomly generated pixel values
    img = create_rgb_bitmap(128, 128)
    img.show()

    # Demo: Create a .wav file with white noise
    create_white_noise(min_freq=400, max_freq=800,duration=3)

if __name__ == "__main__": main()







