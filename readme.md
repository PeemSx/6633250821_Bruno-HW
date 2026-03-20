# 🍜 API Testing Lab: Auntie Som’s Noodle Stall

## Bugs Discovered and How My Tests Detect Them

### 1. Incorrect total price calculation on valid orders
- **Bug summary:** The API subtracts `5` from the correct total price when creating an order. For example, if an order should cost `100`, the API returns `95`.
- **How the test detects it:** The Bruno request `order/orders-valid` checks that `totalPrice` matches `price × quantity`. The test fails because the response returns `95` instead of `100`.

### 2. Orders can be created even when the requested quantity is greater than available stock
- **Bug summary:** The API only checks whether stock is already `0` or below before subtracting the requested quantity. Because of that, it still allows orders that exceed the remaining stock and can make stock go negative.
- **How the test detects it:** The Bruno request `order/orders-over amount in stock` expects the API to reject the order with `400 Bad Request`. The test fails because the API returns `200 OK` and creates the order anyway.

### 3. Requesting a non-existent order returns the wrong status code
- **Bug summary:** When an order ID does not exist, the API returns `200 OK` with an error message instead of returning `404 Not Found`.
- **How the test detects it:** The Bruno request `order/orders-invalid get order` expects `404 Not Found` for an invalid order ID. The test fails because the API responds with `200 OK`.

### Additional validations covered by the test suite
- `order/orders-item not found` confirms the API correctly returns `404 Not Found` when the item ID does not exist.
- `order/orders-out of stock` confirms the API correctly returns `400 Bad Request` when an item has no stock left.
- `order/orders-without token` confirms the API correctly returns `401 Unauthorized` when the request has no access token.
- `order/orders-valid get order` confirms a successfully created order can be retrieved by its order ID.

