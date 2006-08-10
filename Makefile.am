SUBDIRS = pics audio

activitydir = $(datadir)/sugar/activities/memorygame
activity_PYTHON =	\
	__init__.py		\
	memory.py

EXTRA_DIST = memorygame.activity

install-data-local:
	sugar-setup-activity $(srcdir)/memorygame.activity
