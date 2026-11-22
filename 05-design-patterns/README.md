# 05-design-patterns (slide 84)

Refactoring exercises from the course pages: each "spaghetti" script is rewritten with a design pattern. Every file runs on its own with `python3 <file>.py`.

| Family | Pattern | File | Problem it solves |
|---|---|---|---|
| Creational | Factory | [`creational/factory_payment.py`](creational/factory_payment.py) | `if/elif` chain on the payment type |
| Creational | Builder | [`creational/builder_employee.py`](creational/builder_employee.py) | constructor with 17 positional parameters |
| Creational | Singleton | [`creational/singleton_config.py`](creational/singleton_config.py) | config file read again in every module |
| Structural | Adapter | [`structural/adapter_report.py`](structural/adapter_report.py) | legacy XML output, dashboard expects JSON |
| Structural | Decorator | [`structural/decorator_order.py`](structural/decorator_order.py) | explosion of boolean pricing options |
| Behavioral | Strategy | [`behavioral/strategy_report.py`](behavioral/strategy_report.py) | `if/elif` chain on the report format |
| Behavioral | Template method | [`behavioral/template_method_etl.py`](behavioral/template_method_etl.py) | three ETL pipelines duplicating the same workflow |

## Factory

A new payment method is one new class registered in the factory: `process_payment` is never reopened (open/closed principle).

```mermaid
classDiagram
    class PaymentProcessor {
        <<abstract>>
        +validate(details)* bool
        +fee(amount)* float
        +process(amount, details) dict
    }
    class PaymentFactory {
        -_processors: dict
        +get_processor(payment_type) PaymentProcessor
        +register(payment_type, processor_class)
    }
    PaymentProcessor <|-- CreditCardProcessor
    PaymentProcessor <|-- BankTransferProcessor
    PaymentProcessor <|-- PayPalProcessor
    PaymentFactory ..> PaymentProcessor : creates
```

## Builder

Chainable methods each return `self`, validation happens once in `build()`, and presets (`DeveloperBuilder`, `InternBuilder`) encode business rules such as "a senior developer gets admin rights".

```mermaid
classDiagram
    class Employee {
        <<dataclass>>
        first_name, last_name, email
        department, position, salary
        has_laptop, has_vpn_access, has_admin_rights
        contract_type
    }
    class EmployeeBuilder {
        -_data: dict
        +with_name(first, last) EmployeeBuilder
        +with_email(email) EmployeeBuilder
        +with_job(department, position, salary) EmployeeBuilder
        +with_equipment(laptop, parking) EmployeeBuilder
        +with_access(vpn, admin) EmployeeBuilder
        +build() Employee
    }
    EmployeeBuilder <|-- DeveloperBuilder
    EmployeeBuilder <|-- InternBuilder
    EmployeeBuilder ..> Employee : builds
```

## Singleton

`get_instance()` loads `config.json` on the first call and returns the same object afterwards; `get("database.host")` reads nested keys.

```mermaid
classDiagram
    class ConfigManager {
        -_instance: ConfigManager$
        -_config: dict
        +get_instance()$ ConfigManager
        +get(key, default) any
    }
    ConfigManager --> ConfigManager : single instance
```

## Adapter

The legacy library is not modified: the adapter wraps it, converts its XML to JSON and exposes the interface the dashboard expects.

```mermaid
classDiagram
    class ReportGeneratorInterface {
        <<interface>>
        +generate(data)* str
    }
    class LegacyReportAdapter {
        -legacy: LegacyReportGenerator
        +generate(data) str
    }
    class LegacyReportGenerator {
        +generate_report(data) str
    }
    ReportGeneratorInterface <|.. LegacyReportAdapter
    LegacyReportAdapter o-- LegacyReportGenerator : wraps
    AnalyticsDashboard ..> ReportGeneratorInterface : uses
```

## Decorator

Each option wraps the order and adds its own cost and description, so options can be combined freely and new ones added without touching `BaseOrder`.

```mermaid
classDiagram
    class OrderComponent {
        <<interface>>
        +get_cost()* float
        +get_description()* str
    }
    class OrderDecorator {
        -_order: OrderComponent
    }
    OrderComponent <|.. BaseOrder
    OrderComponent <|.. OrderDecorator
    OrderDecorator o-- OrderComponent : wraps
    OrderDecorator <|-- ExpressShippingDecorator
    OrderDecorator <|-- InsuranceDecorator
    OrderDecorator <|-- GiftWrapDecorator
    OrderDecorator <|-- DiscountDecorator
    OrderDecorator <|-- PremiumMemberDecorator
```

## Strategy

The report generator delegates formatting to a strategy object that can be swapped at runtime. HTML was added without modifying any existing class.

```mermaid
classDiagram
    class FormatStrategy {
        <<interface>>
        +format(data)* str
    }
    class ReportGenerator {
        -data: list
        -strategy: FormatStrategy
        +set_strategy(strategy)
        +generate_report() str
        +save_report(filename) str
    }
    ReportGenerator o-- FormatStrategy
    FormatStrategy <|.. PDFFormatStrategy
    FormatStrategy <|.. ExcelFormatStrategy
    FormatStrategy <|.. CSVFormatStrategy
    FormatStrategy <|.. JSONFormatStrategy
    FormatStrategy <|.. HTMLFormatStrategy
```

## Template method

`run()` fixes the workflow once (connect, extract, transform, validate, load, cleanup). Subclasses only implement `extract` and `transform`, and may override the `before_load` hook. The XML pipeline was added the same way.

```mermaid
classDiagram
    class DataPipeline {
        <<abstract>>
        +run() str
        +connect()
        +extract()* list
        +transform(record)* dict
        +validate()
        +before_load()
        +load()
        +cleanup()
    }
    DataPipeline <|-- CSVPipeline
    DataPipeline <|-- APIPipeline
    DataPipeline <|-- DatabasePipeline
    DataPipeline <|-- XMLPipeline
```
