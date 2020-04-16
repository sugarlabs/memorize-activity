What is this?
=============

Memorize is about finding matching pairs.  A pair can be images, sounds and text and this could be extended to animations or movie snippets as well.  Which pairs match is up to the creator of the game.  Memorize is more than a predefined game you can play, it allows you to create new games yourself as well.

How to use?
===========

Memorize is not part of the Sugar desktop, but can be added.  Please refer to;

* [How to Get Sugar on sugarlabs.org](https://sugarlabs.org/),
* [How to use Sugar](https://help.sugarlabs.org/),
* [Download Memorize using Browse](https://activities.sugarlabs.org/), search for `Memorize`, then download, and;
* [How to use Memorize](https://help.sugarlabs.org/memorize.html)

How to upgrade?
===============

On Sugar desktop systems;
* use [My Settings](https://help.sugarlabs.org/my_settings.html), [Software Update](https://help.sugarlabs.org/my_settings.html#software-update), or;
* use Browse to open [activities.sugarlabs.org](https://activities.sugarlabs.org/), search for `Memorize`, then download.

How to integrate?
=================

On Debian and Ubuntu systems;

```
apt install sugar-memorize-activity
```

On Fedora systems;

```
dnf install sugar-memorize
```

Memorize depends on Python, the Sugar Toolkit, and PyGObject bindings for GTK+ 3, GStreamer, and the [GStreamer espeak plugin](https://github.com/sugarlabs/gst-plugins-espeak).

Memorize is started by [Sugar](https://github.com/sugarlabs/sugar).

How to develop?
===============

* main program is `activity.py`,
* directory `demos` contains predefined games, as ZIP bundles of XML, with document type definition `memorize.dtd`,

Opportunities?
==============

See _Issues_ in the repository.

Several long term bugs have yet to be resolved;

* [Save the game state](https://bugs.sugarlabs.org/ticket/4373),
* [Arabic text is smaller](https://bugs.sugarlabs.org/ticket/1881),
* [Discard does not discard game](https://bugs.sugarlabs.org/ticket/3154),
* [Forgets game size in journal](https://bugs.sugarlabs.org/ticket/3754),
* [Cannot restart shared activity](https://bugs.sugarlabs.org/ticket/4453),
* [Collaboration broken with more than two users](https://bugs.sugarlabs.org/ticket/4719).

Icon
====

Memorize icon is a [Glider pattern](https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life)) from Conway's Game of Life, a cellular automaton.  John Conway (FRS) passed away in 2020.
