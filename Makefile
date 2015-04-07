#OSX 
OPEN = open
#LINUX
#OPEN = xdg-open
#WINDOWS
#OPEN = start 

coverage:
	nosetests --with-coverage --cover-package=weatherpy --cover-html
	$(OPEN) cover/index.html 
test:
	nosetests 
clean:
	rm -rf *.pyc
	rm -rf tests/*.pyc
	rm -rf cover
