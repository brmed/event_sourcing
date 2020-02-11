class Publisher:

    def publish(self, *events):
        for e in events:
            e.notify()
