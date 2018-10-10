#!/usr/bin/env sh

# author: Pander
# license: https://github.com/PanderMusubi/klingon/blob/master/LICENSE
# description: package Klingon word list and dictionary for spell checking

set -ex

prepare() {
	# get version number from control file
	VSN=`grep Version control-$PKG|sed -e 's/.* //'`

	# create empty build directory
	if [ -e $PKG\_$VSN\_all ]; then
	    rm -rf $PKG\_$VSN\_all
	fi

	# add documentation
	mkdir -p $PKG\_$VSN\_all/usr/share/doc/$PKG
	cp LICENSE $PKG\_$VSN\_all/usr/share/doc/$PKG/copyright
	cp README.md $PKG\_$VSN\_all/usr/share/doc/$PKG/
	gzip $PKG\_$VSN\_all/usr/share/doc/$PKG/README.md
}

package() {
	# create package
	mkdir -p $PKG\_$VSN\_all/DEBIAN
	cp control-$PKG $PKG\_$VSN\_all/DEBIAN/control
	rm -f $PKG\_$VSN\_all.deb
	dpkg-deb --build $PKG\_$VSN\_all
	#remove build tree
	rm -rf $PKG\_$VSN\_all
	# store package
	if [ ! -e packages ]; then
		mkdir packages
	fi
	mv -f $PKG\_$VSN\_all.deb packages
}

# WORD LIST

# prepare
PKG=wklingon
prepare

# add word list
mkdir -p $PKG\_$VSN\_all/usr/share/dict
cp klingon-latin $PKG\_$VSN\_all/usr/share/dict

# add man file
mkdir -p $PKG\_$VSN\_all/usr/share/man
cp klingon-latin.5 $PKG\_$VSN\_all/usr/share/man
gzip $PKG\_$VSN\_all/usr/share/man/klingon-latin.5

# add wordlist metadata
mkdir -p $PKG\_$VSN\_all/var/lib/dictionaries-common/wordlist/
cp wklingon $PKG\_$VSN\_all/var/lib/dictionaries-common/wordlist/

# build
package

# SPELL CHECKING DICTIONARY

# prepare
PKG=hunspell-tlh
prepare

# add dictionary files
mkdir -p $PKG\_$VSN\_all/usr/share/hunspell
cp tlh_Latn.aff tlh_Latn.dic $PKG\_$VSN\_all/usr/share/hunspell

# build
package
