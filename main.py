from typing import Dict
import argparse
from sys import exit
import logging


def parserSetup() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='find old files not in new, and new files not in old'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='shows all logging',
        action='store_true',
    )
    parser.add_argument(
        '-s', '--silent',
        help='hides all logging',
        action='store_true'
    )
    parser.add_argument(
        '-d', '--debug',
        help='shows debugging logging',
        action='store_true'
    )
    parser.add_argument(
        'inputOld',
        help='input file of old file names (default: Old.sha1.txt)',
        type=str,
        nargs='?',
        default='Old.sha1.txt'
    )
    parser.add_argument(
        'inputNew',
        help='input file of new file names (default: New.sha1.txt)',
        type=str,
        nargs='?',
        default='New.sha1.txt'
    )
    parser.add_argument(
        'outputOld',
        help='output file of  old file names (default: OldNotInNew.txt)',
        type=str,
        nargs='?',
        default='OldNotInNew.txt'
    )
    parser.add_argument(
        'outputNew',
        help='output file of  new file names (default: NewNotInOld.txt)',
        type=str,
        nargs='?',
        default='NewNotInOld.txt'
    )
    return parser.parse_args()


def loggerSetup(args: argparse.Namespace):
    logger = logging.getLogger(__name__)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug(f'logger level set to {logger.level}')

    elif args.verbose:
        logging.basicConfig(level=logging.INFO)
        logger.debug(f'logger level set to {logger.level}')

    elif args.silent:
        logging.basicConfig(level=logging.NOTSET)
        logger.debug(f'logger level set to {logger.level}')


def getSha1FileNames(inputFilePath: str) -> Dict[str, str]:
    logger = logging.getLogger(__name__)

    res = {}
    endOfSha1 = 40
    try:
        logger.debug(f'trying to open file [{inputFilePath}]')

        with open(inputFilePath) as f:
            logger.debug(f'successfully opened f{inputFilePath}')
            logger.info(f'reading from {inputFilePath}')

            for line in f.readlines():
                logger.debug(f'\tread line {line}')
                sha1 = line[:endOfSha1]
                fileName = line[endOfSha1 + 1:]
                logger.debug(f'\tparsed file {fileName} {sha1}')
                res[sha1] = fileName

    except IOError:
        print(
            f'Could not open file at \'{inputFilePath}\' please check that it exists')
        exit(-1)

    logger.info(f'finished reading file[{inputFilePath}]')
    logger.info(f'parsed {len(res)} line(s)')
    return res


def writeSha1FileNames(outputFileName: str, sha1FileNames: Dict[str, str]):
    logger = logging.getLogger(__name__)
    try:
        logger.debug(f'trying to create file {outputFileName}')

        with open(outputFileName, 'w') as f:
            logger.debug('file creation successful')
            logger.info(f'writing to f{outputFileName}')

            for sha1, fileName in sha1FileNames.items():
                logger.debug(f'\twrote {sha1} {fileName}')
                f.writelines(f'{sha1} {fileName}')

        logger.info(f'finished writing file[{outputFileName}]')
        logger.info(f'wrote {len(sha1FileNames)} line(s)')
    except IOError:
        print(
            f'Could not create file at \'{outputFileName}\' please check that it exists')
        exit(-1)


def getSymmetricDifference(left: Dict[str, str], right: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    logger = logging.getLogger(__name__)

    # make a copy of the keys so we can modify the collection 
    logger.debug('starting symmetric difference')
    removed = 0
    for key in left.copy().keys():
        logger.debug(f'\tprocessing {key} {left[key]}')
        if key in right:
            logger.debug(
                f'\t\t {key} {left[key]} found in both sides, removing from both')
            del right[key]
            del left[key]
            removed += 1
    logger.debug('symmetric difference calucation complete')
    logger.info(
        f'{len(left)} old files, {len(right)} new files {removed} removed')
    return {'old': left, 'new': right}


def main(args):
    logger = logging.getLogger(__name__)

    logger.debug('starting main()')

    oldFiles = getSha1FileNames(args.inputOld)
    newFiles = getSha1FileNames(args.inputNew)

    symmetricDiffFiles = getSymmetricDifference(oldFiles, newFiles)

    writeSha1FileNames(args.outputOld, symmetricDiffFiles['old'])
    writeSha1FileNames(args.outputNew, symmetricDiffFiles['new'])

    logger.debug('finished')


if __name__ == "__main__":
    args = parserSetup()
    loggerSetup(args)
    main(args)
