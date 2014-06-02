#!/usr/bin/env python
import os
from app import create_app

app = create_app(os.getenv('BLOG_CONFIG') or 'default')

if __name__ == '__main__':
    manager.run()
