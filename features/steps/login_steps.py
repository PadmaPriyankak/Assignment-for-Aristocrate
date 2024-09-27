from behave import given, when, then

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC



@given('I am on the Demo Login Page')

def step_navigate_to_login_page(context):

    context.driver.get("https://www.saucedemo.com/")



@when('I fill the account information for account {account_type} into the Username field and the Password field')

def step_fill_account_information(context, account_type):

    account_credentials = {

        "StandardUser": {"username": "standard_user", "password": "secret_sauce"},

        "LockedOutUser": {"username": "locked_out_user", "password": "secret_sauce"}

    }

    credentials = account_credentials.get(account_type)

    if credentials:

        fill_login_fields(context, credentials["username"], credentials["password"])



def fill_login_fields(context, username, password):

    context.driver.find_element(By.ID, "user-name").send_keys(username)

    context.driver.find_element(By.ID, "password").send_keys(password)



@when('I click the Login Button')

def step_click_login_button(context):

    context.driver.find_element(By.ID, "login-button").click()



@then('I am redirected to the Demo Main Page')

def step_verify_redirection(context):

    expected_url = "https://www.saucedemo.com/inventory.html"

    assert context.driver.current_url == expected_url, f"Expected {expected_url}, but got {context.driver.current_url}"



@then('I verify the App Logo exists')

def step_verify_app_logo(context):

    app_logo = context.driver.find_element(By.CLASS_NAME, "app_logo")

    assert app_logo.is_displayed(), "App Logo is not displayed"



@given('I am on the inventory page')

def step_navigate_to_inventory_page(context):

    step_navigate_to_login_page(context)

    fill_login_fields(context, "standard_user", "secret_sauce")

    step_click_login_button(context)





@then(u'I verify the Error Message contains the text "{error_message}"')

def step_verify_error_message(context, error_message):

    wait = WebDriverWait(context.driver, 10)

    error_message_element = wait.until(

        EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(),'Epic sadface: Sorry, this user has been locked out')]")))

    actual_error_message = error_message_element.text

    assert error_message in actual_error_message, (

        f"Expected error message to contain '{error_message}', but got '{actual_error_message}'"

    )



@when('user sorts products from high price to low price')

def step_sort_products_high_to_low(context):

    wait = WebDriverWait(context.driver, 10)

    sort_dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product_sort_container")))

    Select(sort_dropdown).select_by_value("hilo")



@when('user adds highest priced product')

def step_add_highest_priced_product(context):

    add_button = context.driver.find_element(By.XPATH, "//div[@class='inventory_item'][1]//button")

    add_button.click()



@when('user clicks on cart')

def step_click_cart(context):

    context.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()



@when('user clicks on checkout')

def step_click_checkout(context):

    context.driver.find_element(By.ID, "checkout").click()



@when('user enters first name {first_name}')

def step_enter_first_name(context, first_name):

    context.driver.find_element(By.ID, "first-name").send_keys(first_name)



@when('user enters last name {last_name}')

def step_enter_last_name(context, last_name):

    context.driver.find_element(By.ID, "last-name").send_keys(last_name)



@when('user enters zip code {zip_code}')

def step_enter_zip_code(context, zip_code):

    context.driver.find_element(By.ID, "postal-code").send_keys(zip_code)



@when('user clicks Continue button')

def step_click_continue(context):

    context.driver.find_element(By.ID, "continue").click()



@then('I verify in Checkout overview page if the total amount for the added item is $49.99')

def step_verify_total_amount(context):

    total_amount_element = context.driver.find_element(By.CLASS_NAME, "summary_total_label")

    total_amount = total_amount_element.text

    assert "$49.99" in total_amount, f"Expected total amount $49.99, but got {total_amount}"



@when('user clicks Finish button')

def step_click_finish_button(context):

    context.driver.find_element(By.ID, "finish").click()



@then('Thank You header is shown in Checkout Complete page')

def step_verify_thank_you_header(context):

    thank_you_header = context.driver.find_element(By.CLASS_NAME, "complete-header")

    assert thank_you_header.is_displayed(), "Thank You header is not displayed"

    context.driver.quit()