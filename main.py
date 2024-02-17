from model import Data
from ui import FamilyTreeUI

def main():
    data = Data()
    family_tree_ui = FamilyTreeUI(data)
    family_tree_ui.run()
    

if __name__ == '__main__':
    main()