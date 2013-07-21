from django import dispatch

transaction_new = dispatch.Signal(providing_args=['is_pdt'])
