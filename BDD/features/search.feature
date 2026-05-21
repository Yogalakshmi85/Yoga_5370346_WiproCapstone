Feature: Product search and cart validation

  Scenario Outline: Search for a product
    Given I am inside Nykaa homepage
    When I search for product "<search_text>"
    Then <expected_result>

    Examples:
      | search_text | expected_result                          |
      | @@@@        | I should see an error message for invalid search |
      | serums      | I should see product results displayed   |

  Scenario: Validate empty cart
    Given I am inside Nykaa homepage
    Then I validate empty cart
