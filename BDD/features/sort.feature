Feature: Handle Sorting

  Scenario Outline: Sorting testing
  Given I am inside Nykaa homepage
  When I navigate to "<section>"
  And I go to "<category>" with href "<href>"
  Then I should land on <category> page

  When I apply filters
    | filter_type | filter_value        | validation |
    | Brand       | Beautywise          | text       |
    | Price       | Rs. 2000 - Rs. 3999 | range      |

  Then products should be filtered correctly
  Then I sort the products

Examples:
  | section | category         | href      |
  | men     | health-nutrition | wellness  |
