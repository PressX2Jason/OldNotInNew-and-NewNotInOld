from typing import Dict


def getOldFiles() -> Dict[str, str]:
    files = {
        '1111111111111111111111111111111111111111': 'file 1.txt',
        '2222222222222222222222222222222222222222': 'file 2.txt'
    }
    return files


def getNewFiles() -> Dict[str, str]:
    files = {
        '1111111111111111111111111111111111111111': 'file 4.txt',
        '7777777777777777777777777777777777777777': 'file 2.txt',
        '3333333333333333333333333333333333333333': 'file 3.txt'
    }
    return files


def getSymmetricDifference(left: Dict[str, str], right: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    for key in left.copy().keys():
        if key in right:
            del right[key]
            del left[key]
    return {'old': left, 'new': right}


def main():
    oldFiles = getOldFiles()
    newFiles = getNewFiles()
    symmetricDiffFiles = getSymmetricDifference(oldFiles, newFiles)

    print('old')
    for oldFiles in symmetricDiffFiles['old']:
        print(oldFiles)

    print('new')
    for newFiles in symmetricDiffFiles['new']:
        print(newFiles)


if __name__ == "__main__":
    main()
