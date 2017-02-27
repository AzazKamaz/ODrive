#! /usr/bin/env python3

import argparse

def parse_args():
  parser = argparse.ArgumentParser(description='Talk to a ODrive board over USB bulk channel.')
  return parser.parse_args()

if __name__ == '__main__':
  # parse args before other imports
  args = parse_args()

import sys
import time
import threading
from odrive import usbbulk

running = True

def main(args):
  global running
  print("ODrive USB Bulk Communications")
  print("---------------------------------------------------------------------")
  print("USAGE:")
  print("\tPOSITION_CONTROL:\n\t\tp MOTOR_NUMBER POSITION VELOCITY CURRENT")
  print("\tVELOCITY_CONTROL:\n\t\tv MOTOR_NUMBER VELOCITY CURRENT")
  print("\tCURRENT_CONTROL:\n\t\tc MOTOR_NUMBER CURRENT")
  print("---------------------------------------------------------------------")
  # query device
  dev = usbbulk.poll_odrive_bulk_device(printer=print)
  print (dev.info())
  print (dev.init())
  # thread
  thread = threading.Thread(target=recieve_thread, args=[dev])
  thread.start()
  while running:
    try:
      command = input("Enter ODrive command:\n")
      print(command)
      dev.send(command)
    except:
      running = False

def recieve_thread(dev):
  while running:
    message = dev.recieve(dev.recieve_max())
    print(bytes(message).decode('ascii'), end='')
    time.sleep(1)

if __name__ == "__main__":
   main(args)