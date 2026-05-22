Feature: Filter validation in Nykaa

  Scenario Outline: Apply filters and validate results
    Given I am inside Nykaa homepage
    When I navigate to "<section>"
    And I go to "<category>" with href "<href>"
    Then I should land on <category> page
    When I apply filter "<filter_type>" with value "<filter_value>"
    Then products should be shown "<expected>"

    Examples:
      | section | category        | href                 | filter_type | filter_value        | expected |
      | men     | hair            | hair-care            | Brand       | Dove                | True     |
      | men     | hair            | hair-care            | Brand       | InvalidBrand        | False    |