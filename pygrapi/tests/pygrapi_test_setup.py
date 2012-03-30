import sys, os

# assume the path the package is in is three segements below current full path (including filename)
sys.path.insert(0, os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0])


