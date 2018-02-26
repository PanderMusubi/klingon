# Klingon

![Klingon logo](images/logo.png?raw=true)

Word lists and spell checking for Klingon, a language constructed language from
the Star Trek universe.


## Source

The source for the word list and spell checking, with permission and under the
same license, is {[boQwI'](https://github.com/De7vID/klingon-assistant)}.


## Word List

The word list is in the ASCII file `klingon-latin`.


## Spell checker

Spell checker support has been made for Hunspell. It can be found in the files
`tlh_Latn.dic` and `tlh_Latn.aff`. These files can be used with the command to
check the spelling of thes in the file `klingon-latin`:

    hunspell -d tlh_Latn -a klingon-latin

Note that this must be run in the directory where the files `tlh_Latn.dic` and
`tlh_Latn.aff` are located. Otherwise, add a relative or absoulte path to the
parameter `tlh_Latn` in the command above.


## Building

Simply run the following scripts in their order to download the source,
preprocess the data, generate the files and test the spell checker:
1. `./1-download-word-list.sh`
2. `./2-extract-words.sh`
3. `./3-generate-spell-checking-and-test-set.sh`
4. `./4-test-spell-checking.sh`


## Installation

To install the build files, which are also shipped in ready-to-install form,
run the scripts:
* `./install-word-list.sh`.
* `./install-support-hunspell.sh`.


## See also

The following sources are relevant:
* https://en.wikipedia.org/wiki/Klingon_language
* https://en.wikipedia.org/wiki/Klingon_grammar
* https://en.wikipedia.org/wiki/Klingon_Language_Institute
* https://kli.org
* https://github.com/De7vID/klingon-assistant
* http://evertype.com/standards/csur/klingon.html
* http://klingonska.org
* http://klingonwiki.net
