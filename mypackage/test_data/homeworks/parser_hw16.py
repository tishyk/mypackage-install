import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path', help="Path to json file to print")
parser.add_argument('zone', help="Zone mode for Plant")
parser.add_argument('-c', dest='common', default='', help="Common")
parser.add_argument('-p', dest='price', default=int, help="PRICE")
parser.add_argument('-a', dest='availability', default=int, help="AVAILABILITY")

args = parser.parse_args()