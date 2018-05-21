
"""
Start-stop training wrapper for Sockeye

"""

import argparse

def main():
    print("Newspaper!")

    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="source corpus")
    parser.add_argument("target", help="target corpus")
    parser.add_argument("scores", help="corpus scores")
    parser.add_argument("db", help="sqlite db name")
    parser.parse_args()

if __name__ == "__main__":
    main()


