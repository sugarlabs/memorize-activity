SUBDIRS = images sounds osc csserver

activitydir = $(datadir)/sugar/activities/memosono
activity_PYTHON =	\
	__init__.py		\
	memosono.py

EXTRA_DIST = memosono.activity

install-data-local:
	sugar-setup-activity $(srcdir)/memosono.activity
