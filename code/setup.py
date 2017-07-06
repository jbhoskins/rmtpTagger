#!/usr/bin/env python3

from distutils.core import setup

setup(name="RMTP Tagger",
      version="0.5",
      description="Application for interactin with transcribing interviews\
              in conjunction with an index of keywords that need to be \
              tagged with specific xml tags.",
      author="John Hoskins and Margaret Swift",
      author_email="jbhoskins@email.wm.edu, meswift@email.wm.edu",
      url="https://github.com/jbhoskins/rmtpTagger",
      packages=["app", "app.gui", "app.backend"],
      requires=["bs4"])
