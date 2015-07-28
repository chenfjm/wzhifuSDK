# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

from pay import view

URLS = [
    ('/wap$', view.Wap),
    ('/prepay$', view.PrePay),
    ('/notify$', view.CallBack),
]

