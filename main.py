from typing import Dict
import argparse


def parserSetup():
    parser = argparse.ArgumentParser(
        description='Find old files not in new, and new files not in old.')
    parser.add_argument(
        'inputOldFileName',
        help='the name of the file containing old file names (default: Old.sha1.txt).',
        type=str,
        nargs='?',
        default='Old.sha1.txt'
    )
    parser.add_argument(
        'inputNewFileName',
        help='the name of the file containing new file names (default: New.sha1.txt).',
        type=str,
        nargs='?',
        default='New.sha1.txt'
    )
    parser.add_argument(
        'outputOldFileName',
        help='the name of the file containing old file names (default: OldNotInNew.txt).',
        type=str,
        nargs='?',
        default='OldNotInNew.txt'
    )
    parser.add_argument(
        'outputNewFileName',
        help='the name of the file containing new file names (default: NewNotInOld.txt).',
        type=str,
        nargs='?',
        default='NewNotInOld.txt'
    )
    return parser.parse_args()


def getSha1FileNames(filePath: str) -> Dict[str, str]:
    res = {}
    endOfSha1 = 40
    with open(filePath) as f:
        for line in f.readlines():
            sha1 = line[:endOfSha1]
            fileName = line[endOfSha1 + 1:]
            res[sha1] = fileName
    return res


def writeSha1FileNames(outputFileName: str, sha1FileNames: Dict[str, str]):
    with open(outputFileName, 'w') as f:
        for sha1, fileName in sha1FileNames.items():
            f.writelines(f'{sha1} {fileName}')


def getSymmetricDifference(left: Dict[str, str], right: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    for key in left.copy().keys():
        if key in right:
            del right[key]
            del left[key]
    return {'old': left, 'new': right}


def main(args):
    oldFiles = getSha1FileNames(args.inputOldFileName)
    newFiles = getSha1FileNames(args.inputNewFileName)

    symmetricDiffFiles = getSymmetricDifference(oldFiles, newFiles)

    writeSha1FileNames(args.outputOldFileName, symmetricDiffFiles['old'])
    writeSha1FileNames(args.outputNewFileName, symmetricDiffFiles['new'])


if __name__ == "__main__":
    args = parserSetup()
    main(args)
