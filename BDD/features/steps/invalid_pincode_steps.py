from behave import when, then

from utils.logger import LogGen

logger = LogGen.loggen()


@then("I should remain on address page due to invalid pincode")
def step_validate_invalid_pincode(context):
    current_url = context.driver.current_url.lower()

    assert "address" in current_url, f"Expected to stay on address page, but navigated to {current_url}"

    logger.info("Invalid pincode validation successful")

@when('I use invalid pincode "{pincode}"')
def step_set_invalid_pincode(context, pincode):
    context.override_pincode = pincode