class Subscriber:

    def subscribe(self, subscriptions):
        for event_class, handler in subscriptions:
            event_class.connect_signal(handler)
