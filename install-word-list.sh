if [ ! -e /usr/share/dict/ ]; then
	mkdir -p /usr/share/dict/
fi
sudo cp -f klingon-latin /usr/share/dict/
sudo ln -sf /usr/share/dict/klingon-latin /usr/share/dict/tlhingan-latin
