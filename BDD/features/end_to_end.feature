Feature: Nykaa End-to-End Purchase Flow

  Scenario Outline: Complete navigation flow
  Given I am inside Nykaa homepage
  When I navigate to "<section>"
  And I go to "<category>" with href "<href>"
  Then I should land on <category> page

  When I apply filters
    | filter_type | filter_value        | validation |
    | Brand       | Beautywise          | text       |
    | Price       | Rs. 2000 - Rs. 3999 | range      |

  Then products should be filtered correctly
  And I select a product
    | product_concern |
    | body-shape      |

  And I add the product to cart
  And I verify the cart
  And I open the cart
  And I proceed to checkout
  And I continue as guest
  When I enter shipping details from "data.csv"
  And I click ship to this address
  Then I should be navigated to payment page if pincode is valid
  Then I select payment method
    | payment_method     |
    | Cash on delivery   |

Examples:
  | section | category         | href      |
  | men     | health-nutrition | wellness  |
