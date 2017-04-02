tip:
	@$(MAKE) -C bundle-xmake-src --no-print-directory tip

build:
	@$(MAKE) -C bundle-xmake-src --no-print-directory build

install:
	@$(MAKE) -C bundle-xmake-src --no-print-directory install

uninstall:
	@$(MAKE) -C bundle-xmake-src --no-print-directory uninstall

.PHONY: tip build install uninstall
