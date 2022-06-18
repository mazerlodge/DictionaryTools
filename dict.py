#!/usr/bin/python3

# Version: 20220423-1458

# Opens dictionary and checks for a word, pattern, substitution encrypted word,
#   jumble, or wordle.

"""
Usage: python dict.py
    -os [mac | win] -action [search | genmask | jumblept2 | maint ] {-debug}

About searches:
    Find a word, pattern (like ABBC), substitution encoded word (like GBRRCB),
      or jumbled word (like ISFH, returns fish).
    Params for -action search:
      -searchtype [word | pattern | encword | jumble]
      -target targetPhrase
    Params for -action jumblept2:
      -target letterList
      -windowsize n
    Params for -action genmask:
      -target targetPhrase
    Params for -action maint:
      -mainttype [ gensortcolumn | addword ]
      -target word_to_add
    Params for -action addword:
      -target word_to_add
    Params for -action wordle:
      -include letterList
      -require letterList
      -omit letterList
    Note: For -action wordle, include list must contain all letters in the
      require list.
    Note: search for word or encword returns first match, pattern returns
      all matches.

"""

import sys
from DictionaryTools import DictionaryEngine

# ### EXECUTION Starts Here ###

de = DictionaryEngine(sys.argv)

# If startup parameters are OK do action specified.
if (not de.bInitOK):
    de.showUsage()
else:
    de.doAction()
