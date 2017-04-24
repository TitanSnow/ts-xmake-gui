# prefix
prefix:=$(if $(prefix),$(prefix),$(if $(findstring /usr/local/bin,$(PATH)),/usr/local,/usr))

tip:
	@$(MAKE) -C bundle-xmake-src --no-print-directory tip

build:
	@$(MAKE) -C bundle-xmake-src --no-print-directory build

install:
	@$(MAKE) -C bundle-xmake-src --no-print-directory install
	@mkdir -p $(prefix)/share/ts-xmake-gui
	@cp -r . $(prefix)/share/ts-xmake-gui
	@mkdir -p $(prefix)/bin
	-@ln -s $(prefix)/share/ts-xmake-gui/ts-xmake-gui.py $(prefix)/bin/ts-xmake-gui
	-@ln -s $(prefix)/share/ts-xmake-gui/ts-xmake-gui.py $(prefix)/bin/xmake-gui

uninstall:
	@$(MAKE) -C bundle-xmake-src --no-print-directory uninstall
	@rm -rf $(prefix)/share/ts-xmake-gui
	-@rm $(prefix)/bin/ts-xmake-gui
	-@rm $(prefix)/bin/xmake-gui

.PHONY: tip build install uninstall
