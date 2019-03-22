from typing import Dict
import argparse
from sys import exit


def parserSetup():
    parser = argparse.ArgumentParser(
        description='Find old files not in new, and new files not in old.')
    parser.add_argument(
        'inputOld',
        help='Input file of old file names (default: Old.sha1.txt).',
        type=str,
        nargs='?',
        default='Old.sha1.txt'
    )
    parser.add_argument(
        'inputNew',
        help='Input file of new file names (default: New.sha1.txt).',
        type=str,
        nargs='?',
        default='New.sha1.txt'
    )
    parser.add_argument(
        'outputOld',
        help='Output file of  old file names (default: OldNotInNew.txt).',
        type=str,
        nargs='?',
        default='OldNotInNew.txt'
    )
    parser.add_argument(
        'outputNew',
        help='Output file of  new file names (default: NewNotInOld.txt).',
        type=str,
        nargs='?',
        default='NewNotInOld.txt'
    )
    return parser.parse_args()


def getSha1FileNames(inputFilePath: str) -> Dict[str, str]:
    res = {}
    endOfSha1 = 40
    try:
        with open(inputFilePath) as f:
            for line in f.readlines():
                sha1 = line[:endOfSha1]
                fileName = line[endOfSha1 + 1:]
                res[sha1] = fileName
    except IOError:
        print(
            f'Could not open file at \'{inputFilePath}\' please check that it exists')
        exit(-1)
    return res


def writeSha1FileNames(outputFileName: str, sha1FileNames: Dict[str, str]):
    try:
        with open(outputFileName, 'w') as f:
            for sha1, fileName in sha1FileNames.items():
                f.writelines(f'{sha1} {fileName}')
    except IOError:
        print(
            f'Could not create file at \'{outputFileName}\' please check that it exists')
        exit(-1)


def getSymmetricDifference(left: Dict[str, str], right: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    for key in left.copy().keys():
        if key in right:
            del right[key]
            del left[key]
    return {'old': left, 'new': right}


def main(args):
    oldFiles = getSha1FileNames(args.inputOld)
    newFiles = getSha1FileNames(args.inputNew)

    symmetricDiffFiles = getSymmetricDifference(oldFiles, newFiles)

    writeSha1FileNames(args.outputOld, symmetricDiffFiles['old'])
    writeSha1FileNames(args.outputNew, symmetricDiffFiles['new'])


if __name__ == "__main__":
    args = parserSetup()
    main(args)
