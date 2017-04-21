N=`export INFO_L10N=0; python -c "import info; print info.lower_name"`
M=`export INFO_L10N=0; python -c "import info; print info.file_filter_mime.replace('/', '-')"`
P=`export INFO_L10N=0; python -c "import info; print info.file_filter_patterns"`
activity.info:
	python makescripts/activity_luncher.py
activity: activity.info mimetypes.xml
	cp activity.info activity/
	if [ -f mimetypes.xml ]; then cp mimetypes.xml activity; fi
app-entry.desktop: app-icon
	python makescripts/desktop_luncher.py
install: app-entry.desktop mimetypes.xml
	python makescripts/systeminstall.py
	mv app-entry.desktop $N.desktop
	xdg-desktop-menu install $N.desktop
	if [ -f mimetypes.xml ]; then cp mimetypes.xml $M.xml; xdg-mime install $M.xml; python makescripts/svg2png.py activity/$M.svg ./mimetype.png; xdg-icon-resource install --context mimetypes --size 48 mimetype.png $M; fi
app-icon:
	python makescripts/svg2png.py data/appicon.svg $N.png
mimetypes.xml:
	if [ "$P" = "[]" ]; then echo "No mime types"; else python makescripts/mime_type.py; fi
xo_bundle:
	python setup.py build
	python makescripts/xobuild.py
dist_tarball:
	python setup.py build
	python makescripts/desktopbuild.py