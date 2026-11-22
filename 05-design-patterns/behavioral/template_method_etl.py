"""Template method pattern: data ETL pipeline"""

from abc import ABC, abstractmethod


class DataPipeline(ABC):
    name = "Generic"
    required_fields = ()

    def __init__(self, source):
        self.source = source
        self.data = None

    def run(self):
        self.connect()
        self.data = self.extract()
        print(f"Extracted {len(self.data)} records")
        print(f"Transforming {self.name} data...")
        self.data = [self.transform(record) for record in self.data]
        self.validate()
        self.before_load()
        self.load()
        self.cleanup()
        return f"{self.name} Pipeline finished"

    def connect(self):
        print(f"Connecting to {self.name}: {self.source}")
        print(f"{self.name} connection established")

    @abstractmethod
    def extract(self) -> list:
        pass

    @abstractmethod
    def transform(self, record: dict) -> dict:
        pass

    def validate(self):
        print("Validating data...")
        for record in self.data:
            if any(field not in record for field in self.required_fields):
                raise ValueError("Invalid record structure")
        print("Validation passed")

    def before_load(self):
        pass

    def load(self):
        print("Loading data to destination...")
        print(f"Loaded {len(self.data)} records successfully")

    def cleanup(self):
        print("Cleaning up resources...")
        self.data = None
        print("Cleanup complete")


class CSVPipeline(DataPipeline):
    name = "CSV"
    required_fields = ("id", "name")

    def extract(self):
        return [{"id": 1, "name": "Alice", "age": "30"}, {"id": 2, "name": "Bob", "age": "25"}]

    def transform(self, record):
        return {**record, "age": int(record["age"]), "name": record["name"].upper()}


class APIPipeline(DataPipeline):
    name = "API"
    required_fields = ("user_id", "username")

    def extract(self):
        return [{"user_id": 101, "username": "Charlie", "score": "85"},
                {"user_id": 102, "username": "Diana", "score": "92"}]

    def transform(self, record):
        score = int(record["score"])
        return {**record, "score": score, "username": record["username"].lower(),
                "grade": "A" if score >= 90 else "B"}


class DatabasePipeline(DataPipeline):
    name = "Database"
    required_fields = ("product_id", "price")

    def extract(self):
        return [{"product_id": 501, "product_name": "laptop", "price": 1200},
                {"product_id": 502, "product_name": "mouse", "price": 25}]

    def transform(self, record):
        price = float(record["price"])
        return {**record, "price": price, "product_name": record["product_name"].title(), "tax": price * 0.2}

    def before_load(self):
        print("Opening database transaction")


class XMLPipeline(DataPipeline):
    name = "XML"
    required_fields = ("order_id", "total")

    def extract(self):
        return [{"order_id": "A1", "total": "49.90"}, {"order_id": "A2", "total": "120.00"}]

    def transform(self, record):
        return {**record, "total": float(record["total"])}


if __name__ == "__main__":
    for pipeline in [CSVPipeline("data/users.csv"), APIPipeline("https://api.example.com/users"),
                     DatabasePipeline("postgresql://localhost/mydb"), XMLPipeline("data/orders.xml")]:
        print(f"RUNNING {pipeline.name.upper()} PIPELINE")
        print("=" * 70)
        print(f"\n{pipeline.run()}\n")
