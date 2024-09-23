BIN_DIR = /usr/bin
LIB_DIR = /usr/lib
INSTALL = install -m 0755 -o root -g root


bin/Absinthe.exe: core/Absinthe.Core.dll wx/Absinthe.exe
	cp -rf core/Absinthe.Core.dll bin
	cp -rf wx/Absinthe.exe bin
	cp -rf plugins/*.dll bin/plugins

wx/Absinthe.exe: core/Absinthe.Core.dll
	$(MAKE) -C plugins
	$(MAKE) -C wx

core/Absinthe.Core.dll: 
	$(MAKE) -C core

install: bin/Absinthe.exe
	./install.sh

clean:
	rm -f gtkAbsinthe.exe Absinthe.Core.dll cli_test.exe Absinthe.exe 
	rm -rf bin/Absinthe.exe bin/Absinthe.Core.dll bin/plugins/*.dll
	$(MAKE) -C core clean
	$(MAKE) -C plugins clean
	$(MAKE) -C wx clean
