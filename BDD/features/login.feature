Feature: Login functionality
  Scenario: Verify OTP page load
    Given I am on the Nykaa homepage
    When I click Sign in
    And I enter phone number "6369887216"
    And I click Send OTP
    And I re-enter phone number "6369887216" on Auth page
    And I click Get OTP
    Then OTP verification page should be displayed
