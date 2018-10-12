#!/usr/bin/env sh

# author: Pander
# license: https://github.com/PanderMusubi/klingon/blob/master/LICENSE
# description: package Klingon word list and dictionary for spell checking

set -ex

if [ ! -e ../build ]; then
	mkdir ../build
fi
cd ../build

prepare() {
	# get version number from control file
	VSN=`grep Version ../static/control-$PKG|sed -e 's/.* //'`

	# create empty build directory
	if [ -e $PKG\_$VSN\_all ]; then
	    rm -rf $PKG\_$VSN\_all
	fi

	# add documentation
	mkdir -p $PKG\_$VSN\_all/usr/share/doc/$PKG
	cp ../LICENSE $PKG\_$VSN\_all/usr/share/doc/$PKG/copyright
	cp ../README.md $PKG\_$VSN\_all/usr/share/doc/$PKG/
	gzip $PKG\_$VSN\_all/usr/share/doc/$PKG/README.md
}

package() {
	# create package
	mkdir -p $PKG\_$VSN\_all/DEBIAN
	cp ../static/control-$PKG $PKG\_$VSN\_all/DEBIAN/control
	rm -f $PKG\_$VSN\_all.deb
	dpkg-deb --build $PKG\_$VSN\_all
	# store package
	if [ ! -e ../packages ]; then
		mkdir ../packages
	fi
	mv -f $PKG\_$VSN\_all.deb ../packages
}

# WORD LIST

# prepare
PKG=wklingon
prepare

# add generated word lists
mkdir -p $PKG\_$VSN\_all/usr/share/dict
cp ../generated/klingon-latin $PKG\_$VSN\_all/usr/share/dict
cp ../generated/klingon $PKG\_$VSN\_all/usr/share/dict

# add man file
mkdir -p $PKG\_$VSN\_all/usr/share/man
cp ../static/klingon-latin.5 $PKG\_$VSN\_all/usr/share/man
gzip $PKG\_$VSN\_all/usr/share/man/klingon-latin.5
cp ../static/klingon.5 $PKG\_$VSN\_all/usr/share/man
gzip $PKG\_$VSN\_all/usr/share/man/klingon.5

# add wordlist metadata
mkdir -p $PKG\_$VSN\_all/var/lib/dictionaries-common/wordlist/
cp ../static/wklingon $PKG\_$VSN\_all/var/lib/dictionaries-common/wordlist/
cp ../static/klingon $PKG\_$VSN\_all/var/lib/dictionaries-common/wordlist/

# build
package

# SPELL CHECKING DICTIONARY

# prepare
PKG=hunspell-tlh
prepare

# add generated dictionary files
mkdir -p $PKG\_$VSN\_all/usr/share/hunspell
cp ../generated/tlh_Latn.aff $PKG\_$VSN\_all/usr/share/hunspell
cp ../generated/tlh_Latn.dic $PKG\_$VSN\_all/usr/share/hunspell
cp ../generated/tlh.aff $PKG\_$VSN\_all/usr/share/hunspell
cp ../generated/tlh.dic $PKG\_$VSN\_all/usr/share/hunspell

# build
package

cd ../scripts
