"""Singleton pattern: configuration manager"""

import json
import os


class ConfigManager:
    _instance = None

    def __init__(self, path):
        if ConfigManager._instance is not None:
            raise RuntimeError("Use ConfigManager.get_instance()")
        with open(path, "r") as f:
            self._config = json.load(f)
        self.loads = 1

    @classmethod
    def get_instance(cls, path=None):
        if cls._instance is None:
            path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            cls._instance = cls(path)
        return cls._instance

    def get(self, key, default=None):
        value = self._config
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value


def start_application():
    config = ConfigManager.get_instance()
    print(f"Starting {config.get('app.name')} (debug={config.get('app.debug')})")


def connect_database():
    config = ConfigManager.get_instance()
    print(f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}")


def send_email(to, subject):
    config = ConfigManager.get_instance()
    print(f"Sending email from {config.get('email.sender')} via {config.get('email.smtp_host')}")


def process_payment(amount):
    config = ConfigManager.get_instance()
    print(f"Processing {amount}€ in {config.get('payment.environment')} mode")


if __name__ == "__main__":
    start_application()
    connect_database()
    send_email("user@test.com", "Welcome")
    process_payment(99.99)

    a = ConfigManager.get_instance()
    b = ConfigManager.get_instance()
    print(a is b, a.loads)
