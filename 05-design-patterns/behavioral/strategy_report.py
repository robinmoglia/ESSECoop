"""Strategy pattern: report generator with interchangeable formats"""

import json
from abc import ABC, abstractmethod


class FormatStrategy(ABC):
    extension = ""

    @abstractmethod
    def format(self, data: list) -> str:
        pass


class PDFFormatStrategy(FormatStrategy):
    extension = ".pdf"

    def format(self, data):
        lines = ["PDF REPORT", "=" * 50]
        lines += [f"| {item['name']:20} | {item['value']:10} |" for item in data]
        lines += ["=" * 50, "End of PDF Report"]
        return "\n".join(lines)


class ExcelFormatStrategy(FormatStrategy):
    extension = ".xlsx"

    def format(self, data):
        lines = ["EXCEL REPORT", "-" * 50, "Name\tValue"]
        lines += [f"{item['name']}\t{item['value']}" for item in data]
        lines.append("-" * 50)
        return "\n".join(lines)


class CSVFormatStrategy(FormatStrategy):
    extension = ".csv"

    def format(self, data):
        return "\n".join(["name,value"] + [f"{item['name']},{item['value']}" for item in data])


class JSONFormatStrategy(FormatStrategy):
    extension = ".json"

    def format(self, data):
        return json.dumps(data, indent=2)


class HTMLFormatStrategy(FormatStrategy):
    extension = ".html"

    def format(self, data):
        rows = "\n".join(f"  <tr><td>{item['name']}</td><td>{item['value']}</td></tr>" for item in data)
        return f"<table>\n  <tr><th>Name</th><th>Value</th></tr>\n{rows}\n</table>"


class ReportGenerator:
    def __init__(self, data, strategy: FormatStrategy = None):
        self.data = data
        self.strategy = strategy

    def set_strategy(self, strategy: FormatStrategy):
        self.strategy = strategy

    def generate_report(self) -> str:
        if self.strategy is None:
            raise ValueError("No format strategy set")
        return self.strategy.format(self.data)

    def save_report(self, filename):
        path = filename + self.strategy.extension
        with open(path, "w") as f:
            f.write(self.generate_report())
        return path


if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]
    generator = ReportGenerator(data)

    for title, strategy in [("PDF", PDFFormatStrategy()), ("CSV", CSVFormatStrategy()),
                            ("JSON", JSONFormatStrategy()), ("HTML (NEW!)", HTMLFormatStrategy())]:
        print(f"=== {title} FORMAT ===")
        generator.set_strategy(strategy)
        print(generator.generate_report())
        print("\n" + "=" * 60 + "\n")
