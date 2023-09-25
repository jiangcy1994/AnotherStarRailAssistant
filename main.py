import argparse

parser = argparse.ArgumentParser(
    prog='python main.py',
    description='Another hsr assistant with similar function')

parser.add_argument('--start_map', metavar='MAP',
                    default='auto', type=str,
                    help='choose a start map, e.g. {auto, 1.1.1, ...}')
parser.add_argument('--end_action', metavar='ACTION',
                    default='none', type=str, choices=['none', 'logout', 'shutdown'],
                    help='the action in the end, e.g. {none,logout,shutdown}')
args = parser.parse_args()

if __name__ == "__main__":
    pass
