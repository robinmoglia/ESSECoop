"""Adapter pattern: legacy XML reports for a JSON dashboard"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


class AnalyticsDashboard:
    def display(self, json_data: str):
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        pass


class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy: LegacyReportGenerator):
        self.legacy = legacy

    def generate(self, data: dict) -> str:
        xml_report = self.legacy.generate_report(data)
        root = ET.fromstring(xml_report)
        return json.dumps({child.tag: self._parse(child.text) for child in root})

    @staticmethod
    def _parse(text):
        for cast in (int, float):
            try:
                return cast(text)
            except ValueError:
                pass
        return text


def show_report(generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard, data: dict):
    dashboard.display(generator.generate(data))


if __name__ == "__main__":
    report_generator = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()

    show_report(report_generator, dashboard, {"total_sales": 150000, "orders": 1234, "avg_order": 121.55})
    show_report(report_generator, dashboard, {"total_items": 5000, "low_stock": 45, "out_of_stock": 12})
