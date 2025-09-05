#!/usr/bin/env python3
from typing import List, Dict, Any

class CashRegister:
    def __init__(self, discount: int = 0):
        self._discount: int = 0
        self.discount = discount  # validates
        self.total: float = 0.0
        self.items: List[str] = []
        self.previous_transactions: List[Dict[str, Any]] = []

    # -------- properties --------
    @property
    def discount(self) -> int:
        return self._discount

    @discount.setter
    def discount(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or not (0 <= value <= 100):
            print("Not valid discount")
            return
        self._discount = value

    # -------- methods --------
    def add_item(self, item: str, price: float, quantity: int = 1) -> None:
        if not isinstance(item, str) or not item:
            raise ValueError("item must be a non-empty string")
        if not (isinstance(price, int) or isinstance(price, float)) or price < 0:
            raise ValueError("price must be a non-negative number")
        if not isinstance(quantity, int) or quantity < 1:
            raise ValueError("quantity must be a positive integer")

        line_total = price * quantity
        self.total += line_total
        self.items.extend([item] * quantity)

        self.previous_transactions.append({
            "type": "item",
            "amount": line_total,
            "meta": {"item": item, "price": price, "quantity": quantity}
        })

    def apply_discount(self) -> None:
        # If no discount or nothing to discount, print exactly as the test expects
        if self.discount <= 0 or self.total <= 0:
            print("There is no discount to apply.")
            return

        discount_amount = round(self.total * (self.discount / 100.0), 2)
        if discount_amount <= 0:
            print("There is no discount to apply.")
            return

        self.total = round(self.total - discount_amount, 2)

        # record the discount so it can be undone
        self.previous_transactions.append({
            "type": "discount",
            "amount": -discount_amount,
            "meta": {"discount_percent": self.discount}
        })

        # EXACT success message required by your test:
        # If total is an integer amount, show no cents; else show two decimals.
        if float(self.total).is_integer():
            amount_str = f"${int(self.total)}"
        else:
            amount_str = f"${self.total:.2f}"
        print(f"After the discount, the total comes to {amount_str}.")

    def void_last_transaction(self) -> None:
        if not self.previous_transactions:
            print("No transactions to void.")
            return

        last = self.previous_transactions.pop()
        ttype = last.get("type")
        amount = last.get("amount", 0.0)

        if ttype == "item":
            meta = last.get("meta", {})
            price = meta.get("price", 0.0)
            quantity = meta.get("quantity", 0)
            item = meta.get("item")

            self.total = round(self.total - (price * quantity), 2)

            removed = 0
            for i in range(len(self.items) - 1, -1, -1):
                if removed >= quantity:
                    break
                if self.items[i] == item:
                    self.items.pop(i)
                    removed += 1

        elif ttype == "discount":
            # discount amount stored negative; reversing means subtracting negative
            self.total = round(self.total - amount, 2)
        else:
            # put it back; unknown type
            self.previous_transactions.append(last)
            print("Unable to void last transaction: unknown type.")

    def __repr__(self) -> str:
        return (f"CashRegister(discount={self.discount}, total={self.total}, "
                f"items={len(self.items)} items, txns={len(self.previous_transactions)})")
