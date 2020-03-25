# encoding=ascii
"""Demonstrate the use of a slice object in __getitem__.

If the `start` or `stop` members of a slice are strings, then look for
those strings within the phrase and make a substring using the offsets.
If `stop` is a string, include it in the returned substring.

This code is for demonstration purposes only.
It is not 100% correct.
For example, it does not support negative steps in a "natural" way.
"""


class Phrase:
    """Demonstrate custom __getitem__ taking a slice argument."""

    def __init__(my, phrase: str):
        """Initialise with a string phrase."""
        my.phrase = phrase

    def __getitem__(my, item):
        """Get an item or a slice."""
        if isinstance(item, slice):
            return my._getslice(item)
        return my.phrase[item]

    def _getslice(my, sli):
        start, stop, step = sli.start, sli.stop, sli.step
        try:
            # if start is a string, slice from there
            if isinstance(start, str):
                start = my.phrase.index(start)
            # if stop is a string, slice to the end of it
            if isinstance(stop, str):
                stop = my.phrase.index(stop) + len(stop)
        except ValueError:
            return ''
        return my.phrase[start:stop:step]


def main():
    """Demonstrate the Phrase class."""
    phrase = Phrase('Now is the winter of our discontent.')

    print(f'Integer subscription: [8]={phrase[8]} [-1]={phrase[-1]}')
    print(f'Integer slicing: [7,10]={phrase[7:10]}')

    print('Slicing using strings ...')
    print(f"| from 'the' to 'of': ({phrase['the':'of']})")
    print(f"| from 'the' to 'unfound': ({phrase['the':'unfound']})")
    print(f"| upto the word 'winter': ({phrase[:'winter']})")
    print(f"| from the word 'winter' onwards: ({phrase['winter':]})")


if __name__ == '__main__':
    main()
