import abc

# 1. Abstract Base Class for Payment Providers
class PaymentProvider(abc.ABC):
    """Abstract base class defining the interface for payment providers."""

    @abc.abstractmethod
    def process_payment(self, amount: float) -> str:
        """Processes a payment and returns a transaction ID."""
        pass

    @abc.abstractmethod
    def refund_payment(self, transaction_id: str) -> bool:
        """Refunds a payment and returns success status."""
        pass

    @abc.abstractmethod
    def get_provider_name(self) -> str:
        """Returns the name of the payment provider."""
        pass

    @abc.abstractmethod
    def get_transaction_fee(self, amount: float) -> float:
        """Returns the transaction fee for a given amount."""
        pass

# 2. Concrete Implementations of Payment Providers
class StripeProvider(PaymentProvider):
    """Concrete implementation for a hypothetical Stripe payment provider."""
    def get_provider_name(self) -> str:
        return "Stripe"

    def process_payment(self, amount: float) -> str:
        print(f"[{self.get_provider_name()}] Processing payment of ${amount:.2f}...")
        # Simulate API call to Stripe
        transaction_id = f"STRIPE_TXN_{hash(amount)}"
        print(f"[{self.get_provider_name()}] Payment successful. Transaction ID: {transaction_id}")
        return transaction_id

    def refund_payment(self, transaction_id: str) -> bool:
        print(f"[{self.get_provider_name()}] Initiating refund for transaction ID: {transaction_id}...")
        # Simulate API call to Stripe
        print(f"[{self.get_provider_name()}] Refund successful for {transaction_id}.")
        return True

    def get_transaction_fee(self, amount: float) -> float:
        # Simulate Stripe's fee structure
        return amount * 0.029 + 0.30 # 2.9% + 30 cents

class PayPalProvider(PaymentProvider):
    """Concrete implementation for a hypothetical PayPal payment provider."""
    def get_provider_name(self) -> str:
        return "PayPal"

    def process_payment(self, amount: float) -> str:
        print(f"[{self.get_provider_name()}] Processing payment of ${amount:.2f}...")
        # Simulate API call to PayPal
        transaction_id = f"PAYPAL_TXN_{hash(amount)}"
        print(f"[{self.get_provider_name()}] Payment successful. Transaction ID: {transaction_id}")
        return transaction_id

    def refund_payment(self, transaction_id: str) -> bool:
        print(f"[{self.get_provider_name()}] Initiating refund for transaction ID: {transaction_id}...")
        # Simulate API call to PayPal
        print(f"[{self.get_provider_name()}] Refund successful for {transaction_id}.")
        return True

    def get_transaction_fee(self, amount: float) -> float:
        # Simulate PayPal's fee structure
        return amount * 0.0349 + 0.49 # 3.49% + 49 cents

class CustomGatewayProvider(PaymentProvider):
    """Another concrete implementation for a hypothetical custom gateway provider."""
    def get_provider_name(self) -> str:
        return "CustomGateway"

    def process_payment(self, amount: float) -> str:
        print(f"[{self.get_provider_name()}] Processing payment of ${amount:.2f}...")
        transaction_id = f"CUSTOM_TXN_{hash(amount)}"
        print(f"[{self.get_provider_name()}] Payment successful. Transaction ID: {transaction_id}")
        return transaction_id

    def refund_payment(self, transaction_id: str) -> bool:
        print(f"[{self.get_provider_name()}] Initiating refund for transaction ID: {transaction_id}...")
        print(f"[{self.get_provider_name()}] Refund successful for {transaction_id}.")
        return True

    def get_transaction_fee(self, amount: float) -> float:
        # Simulate a potentially cheaper custom gateway fee
        return amount * 0.015 + 0.10 # 1.5% + 10 cents

# 3. Payment Service (Client) that uses a PaymentProvider
class PaymentService:
    """
    Manages payment operations using an injected payment provider.
    This class is decoupled from specific provider implementations.
    """
    def __init__(self, provider: PaymentProvider):
        # The PaymentService depends on the abstract PaymentProvider interface,
        # not a concrete implementation. This is key for flexibility and avoiding vendor lock-in.
        self._provider = provider
        print(f"\nPaymentService initialized with {self._provider.get_provider_name()}.")

    def set_provider(self, new_provider: PaymentProvider):
        """Allows changing the payment provider at runtime, demonstrating seamless transition."""
        # This method illustrates how the application can switch providers
        # without modifying its core business logic, supporting seamless transitions.
        print(f"\nSwitching payment provider from {self._provider.get_provider_name()} to {new_provider.get_provider_name()}.")
        self._provider = new_provider

    def charge(self, amount: float) -> str:
        """Performs a payment using the currently configured provider."""
        print(f"Attempting to charge ${amount:.2f} via {self._provider.get_provider_name()}...")
        transaction_id = self._provider.process_payment(amount)
        return transaction_id

    def process_refund(self, transaction_id: str) -> bool:
        """Initiates a refund using the currently configured provider."""
        print(f"Attempting to refund transaction {transaction_id} via {self._provider.get_provider_name()}...")
        return self._provider.refund_payment(transaction_id)

    def get_current_provider_fees(self, amount: float) -> float:
        """Gets transaction fees for a given amount from the current provider."""
        return self._provider.get_transaction_fee(amount)

# 4. Main application logic to demonstrate switching providers
if __name__ == "__main__":
    # Initialize with a default provider (e.g., Stripe)
    print("--- Scenario 1: Initial setup with Stripe ---")
    stripe_provider = StripeProvider()
    payment_app = PaymentService(stripe_provider)

    # Process a payment
    payment_amount = 100.00
    txn_id_1 = payment_app.charge(payment_amount)
    print(f"Fee for ${payment_amount:.2f} with {stripe_provider.get_provider_name()}: ${payment_app.get_current_provider_fees(payment_amount):.2f}")

    # Refund a payment
    payment_app.process_refund(txn_id_1)

    # --- Scenario 2: Switching to PayPal for different reasons (e.g., customer preference, lower fees for specific regions) ---
    print("\n--- Scenario 2: Switching to PayPal ---")
    paypal_provider = PayPalProvider()
    # The application can switch providers seamlessly without changing the PaymentService's core logic.
    payment_app.set_provider(paypal_provider)

    # Process another payment with PayPal
    payment_amount_2 = 50.00
    txn_id_2 = payment_app.charge(payment_amount_2)
    print(f"Fee for ${payment_amount_2:.2f} with {paypal_provider.get_provider_name()}: ${payment_app.get_current_provider_fees(payment_amount_2):.2f}")

    # --- Scenario 3: Introducing a new, potentially cheaper provider (CustomGateway) ---
    print("\n--- Scenario 3: Introducing a new, cheaper provider (CustomGateway) ---")
    custom_provider = CustomGatewayProvider()
    # A new provider can be integrated by simply implementing the PaymentProvider interface.
    # No changes are needed in PaymentService or other parts of the application, mitigating vendor lock-in.
    payment_app.set_provider(custom_provider)

    # Process a payment with CustomGateway
    payment_amount_3 = 200.00
    txn_id_3 = payment_app.charge(payment_amount_3)
    print(f"Fee for ${payment_amount_3:.2f} with {custom_provider.get_provider_name()}: ${payment_app.get_current_provider_fees(payment_amount_3):.2f}")

    # Compare fees for a fixed amount across providers
    print("\n--- Fee Comparison for a $100 transaction ---")
    test_amount = 100.00
    print(f"Stripe fee: ${StripeProvider().get_transaction_fee(test_amount):.2f}")
    print(f"PayPal fee: ${PayPalProvider().get_transaction_fee(test_amount):.2f}")
    print(f"CustomGateway fee: ${CustomGatewayProvider().get_transaction_fee(test_amount):.2f}")
    print("\nThis comparison highlights how different providers offer different cost structures, "
          "making provider switching a strategic decision for cost optimization.")

    print("\n--- Demonstrating vendor lock-in mitigation ---")
    print("The application's core payment logic (PaymentService) remains unchanged "
          "even when new providers are added or existing ones are swapped out. "
          "This design reduces the risk of vendor lock-in and allows for seamless transitions.")
