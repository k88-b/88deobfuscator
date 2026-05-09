#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import App


if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        print("\nExiting.")
