# Klingon

![Klingon logo](images/logo.png?raw=true)

Word lists and spell checking for Klingon (tlh), a constructed language from the
Star Trek universe.


## Source

The source for the word list and spell checking, with permission and under the
same license, is {[boQwI'](https://github.com/De7vID/klingon-assistant)}.


## Installation

Install the word list and spell checker packages from the `packages` directory
with the command `sudo dpkg -i` followed by the filenames of the packages that
need to be installed.

Command-line spell checkers such as Hunspell and Nuspell as well as GUI
applications such as LibreOffice and Mozilla's Firefox are able to use the
Klingon spell checker.


## Word List

The word list in Latin script is in the ASCII file
[`generated/klingon-latin`](generated/klingon-latin). The same list
transliterated in Klingon script is in the file
[`generated/klingon`](generated/klingon). Note that the encoding has private-use
characters. To display these properly, a font supporting Klingon characters need
to be installed.

See the section on installation to make the word lists available as
`/usr/share/dict/klingon-latin` and `/usr/share/dict/klingon`


## Spell checker

Spell checker support has been made for Hunspell and
[Nuspell](https://nuspell.github.io/). It can be found in the files
[`generated/tlh_Latn.dic`](generated/tlh_Latn.dic) and
[`generated/tlh_Latn.aff`](generated/tlh_Latn.aff) for Latin script. For Klingon
script, see [`generated/tlh.dic`](generated/tlh.dic) and
[`generated/tlh.aff`](generated/tlh.aff).

See the section on installation to make the spell checker directly available in
Hunspell and Nuspell. It will install the `.aff` and `.dic` files in
`/usr/share/hunspell`. Example usage then is:

    hunspell -d tlh_Latn -a /usr/share/dict/klingon-latin
    hunspell -d tlh -a /usr/share/dict/klingon
    nuspell -d tlh_Latn /usr/share/dict/klingon-latin
    nuspell -d tlh /usr/share/dict/klingon

See the test script on how to use the spell checker without installing the
packages. Simply use absolute or relative paths.


## Building

To build, tast and package all the files, simply run the scripts in the
`scripts` directory in their order:
1. `./1-download-word-list.sh`
2. `./2-extract-words.sh`
3. `./3-generate-files.sh` (which calls `3-generate-files.py`)
4. `./4-transliterate.py` (see the result in directory `generated`)
5. `./5-test-spell-checking.sh` (see the result in directory `test`)
6. `./6-package.sh` (see the result in directory `packages`)


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
* https://nuspell.github.io
