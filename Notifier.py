from win10toast import ToastNotifier

def notify(header, body):
    notifier = ToastNotifier()
    notifier.show_toast(header,body, duration=10)