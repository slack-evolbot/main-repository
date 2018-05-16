#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

def main():
    app = wx.App()
    frame = wx.Frame(None, -1, u'日本語でこんにちわ')
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
