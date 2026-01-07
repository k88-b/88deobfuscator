#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.menu import Menu

def main():
    menu = Menu()
    menu.run()
        
if __name__ == "__main__":  
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")
        
        
