# ABCD Records

A mail-order company sells CDs and tapes. Only members can order: non-members receive a membership application. Royal members get discounts and priority and can order unavailable items; regular members cannot. Members pay by cash, check or bank draft. An order processing clerk verifies and processes orders, a collection department clerk handles payments, and every order is saved to a daily records file.

## Use case diagram

```mermaid
flowchart LR
    M([Member])
    RM([Royal member])
    NM([Non-member])
    OPC([Order processing clerk])
    CDC([Collection department clerk])

    subgraph sys [ABCD Records system]
        PO((Place order))
        VM((Verify membership))
        VA((Verify item availability))
        AD((Apply discount))
        OU((Order unavailable items))
        PR((Process order))
        PI((Print invoice))
        PS((Print shipping list))
        SR((Save to daily records))
        MP((Make payment))
        SA((Send membership application))
    end

    RM -->|is a| M
    M --- PO
    M --- MP
    NM --- SA
    OPC --- PR
    OPC --- SA
    CDC --- MP

    PO -. "«include»" .-> VM
    PO -. "«include»" .-> VA
    PR -. "«include»" .-> PI
    PR -. "«include»" .-> PS
    PR -. "«include»" .-> SR
    AD -. "«extend»" .-> PO
    OU -. "«extend»" .-> PO
    SA -. "«extend»" .-> VM
```

- **Include** (always happens): placing an order always verifies membership and availability; processing an order always prints the invoice and the shipping list and saves the order.
- **Extend** (happens only sometimes): the discount and ordering unavailable items only apply to royal members; the membership application is only sent when the membership check fails. The arrow points from the optional use case to the base one.
- **Actor generalization**: a royal member is a member, so it can do everything a member does.

## Class diagram

```mermaid
classDiagram
    class Member {
        <<abstract>>
        -member_id: int
        -name: str
        -address: str
        +discount_rate()* float
        +can_order_unavailable() bool
        +place_order(order_id) Order
    }
    class RegularMember
    class RoyalMember
    class MembershipApplication {
        -applicant_name: str
        -address: str
        -sent_on: date
    }
    class Order {
        -order_id: int
        -order_date: date
        -status: str
        +add_item(item, quantity)
        +total() float
    }
    class OrderLine {
        -quantity: int
        -backordered: bool
        +subtotal() float
    }
    class Item {
        <<abstract>>
        -code: str
        -title: str
        -price: float
        -stock: int
        +is_available(quantity) bool
    }
    class CD
    class Tape
    class Invoice {
        -amount: float
        +print()
    }
    class ShippingList {
        -items: list~str~
        +print()
    }
    class Payment {
        <<abstract>>
        -amount: float
        +describe()*
    }
    class Cash
    class Check {
        -check_number: str
    }
    class BankDraft {
        -bank: str
    }
    class OrderProcessingClerk {
        +verify_membership(person_id) bool
        +send_membership_application(name, address)
        +process_order(order)
    }
    class CollectionDepartmentClerk {
        +collect_payment(order, payment)
    }
    class DailyRecordsFile {
        +save(order)
    }

    Member <|-- RegularMember
    Member <|-- RoyalMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft

    Member "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "0..*" --> "1" Item : refers to
    Order "1" *-- "1" Invoice
    Order "1" *-- "1" ShippingList
    Order "1" --> "0..1" Payment : paid by
    DailyRecordsFile "1" o-- "0..*" Order : stores
    OrderProcessingClerk "1" --> "0..*" Order : processes
    OrderProcessingClerk ..> MembershipApplication : sends
    CollectionDepartmentClerk "1" --> "0..*" Payment : collects
```

## Design choices

- **Composition**: order lines, the invoice and the shipping list do not exist without their order.
- **Aggregation**: the daily records file stores orders, but an order exists on its own.
- **OrderLine** sits between `Order` and `Item` because one order holds several items, each with its own quantity, and the same item appears in many orders.
- **Inheritance + polymorphism**: `RoyalMember` overrides `discount_rate()` and `can_order_unavailable()`, so the clerk never needs an `if member is royal` test.

## Scenario: a royal member orders two CDs (one unavailable) and pays by check

```mermaid
sequenceDiagram
    actor RM as Royal member
    participant OPC as Order processing clerk
    participant O as Order
    participant DR as Daily records file
    participant CDC as Collection department clerk
    RM->>O: place_order() + add_item(CD x2)
    RM->>OPC: submit order
    OPC->>OPC: verify_membership()
    OPC->>O: process_order()
    Note over OPC,O: CD 2 unavailable, royal member, so it is backordered
    OPC->>DR: save(order)
    OPC-->>RM: invoice + shipping list
    RM->>CDC: pay by check
    CDC->>O: collect_payment(Check)
```

## Run

```bash
python3 abcd_records.py
```
