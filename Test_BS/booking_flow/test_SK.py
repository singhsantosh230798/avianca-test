import time
from datetime import datetime
import random

import pytest
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException, NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager




class SeleniumHelper:
    def __init__(self):
        # Driver configuration
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()

        # Load a given URL

    def load_url(self, url):
        self.driver.get(url)
        print(f"URL loaded: {url}")

        # Close the browser driver

    def close(self):
        self.driver.quit()
        print("Driver closed.")

        # Get the current time formatted for logging

    def get_current_time(self):
        return datetime.now().strftime("%H:%M:%S")

        # Scroll to make an element visible

    def scroll_element(self, by_selector, selector_element):
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, selector_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
            print(f"Element visible after scroll: {selector_element}")
            return element
        except Exception as e:
            print(f"Error during scrolling: {e}")

        # Click on an element

    def click_element(self, by_selector, selector_element, timeout=5):
        try:
            # Determine which strategy to use for locating the element
            if by_selector == "xpath":
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, selector_element))
                )
            elif by_selector == "xpath-scroll":
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, selector_element))
                )
                # Scroll to the element if it's not in view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            
            # Perform the click
            element.click()
            print(f"[{self.get_current_time()}] - Clicked on element: {selector_element}")
        
        except StaleElementReferenceException:
            # Retry if the element reference is stale (removed from DOM)
            print(f"[{self.get_current_time()}] - Element became stale, retrying click: {selector_element}")
            self.click_element(by_selector, selector_element, timeout)
        
        except TimeoutException:
            # Handle timeout if the element is not clickable within the given time
            print(f"[{self.get_current_time()}] - Timeout while waiting for element: {selector_element}")
        
        except Exception as e:
            # General exception handling for other errors
            print(f"[{self.get_current_time()}] - Error while clicking on {selector_element}: {e}")


        # Type text into an element

    def type_text(self, by_selector, selector_element, text, timeout=2, retries=1):
    # Locate the element based on the selector type
        try:
            if by_selector == "xpath":
                # Directly wait for visibility with a reduced timeout
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, selector_element))
                )
                element.clear()  # Clear the field before typing
                element.send_keys(text)  # Type the text
                print(f"[{self.get_current_time()}] - Text entered in {selector_element}: {text}")
                return  # Exit after successful typing
        except StaleElementReferenceException as e:
            print(f"[{self.get_current_time()}] - Stale element error: {e}")
            if retries > 0:
                # Retry logic for stale element if retries remain
                return self.type_text(by_selector, selector_element, text, timeout, retries - 1)
            else:
                print(f"[{self.get_current_time()}] - Max retries reached for stale element: {selector_element}")
                return
        except TimeoutException as e:
            print(f"[{self.get_current_time()}] - Timeout while waiting for element: {selector_element}")
            return
        except Exception as e:
            print(f"[{self.get_current_time()}] - Error while typing text in {selector_element}: {e}")

        # Wait for an element to become visible

    def wait_for_visibility_of_element_located(self, by_selector, selector_element, wait_time=40):
        try:
            # Map selector types to By selectors
            selector_mapping = {
                "xpath": By.XPATH,
                "id": By.ID,
                "css": By.CSS_SELECTOR,
                "class_name": By.CLASS_NAME
            }

            # Get the appropriate selector type
            if by_selector not in selector_mapping:
                print(f"[{self.get_current_time()}] - Invalid selector type: {by_selector}")
                return False

            # Wait for visibility of the element using the mapped selector
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located((selector_mapping[by_selector], selector_element))
            )
            print(f"[{self.get_current_time()}] - Element visible: {selector_element}")
            return True
        except TimeoutException:
            print(f"[{self.get_current_time()}] - Timeout waiting for element to be visible: {selector_element}")
            return False
        except Exception as e:
            print(f"[{self.get_current_time()}] - Error occurred while waiting for visibility of {selector_element}: {e}")
            return False

        # Wait for an element to become invisible

    def wait_for_invisibility_of_element_located(self, by_selector, selector_element, wait_time=40):
        try:
            # Map selector types to By selectors
            selector_mapping = {
                "xpath": By.XPATH,
                "id": By.ID,
                "css": By.CSS_SELECTOR,
                "class_name": By.CLASS_NAME
            }

            # Get the appropriate selector type
            if by_selector not in selector_mapping:
                print(f"[{self.get_current_time()}] - Invalid selector type: {by_selector}")
                return False

            # Wait for invisibility of the element using the mapped selector
            WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located((selector_mapping[by_selector], selector_element))
            )
            print(f"[{self.get_current_time()}] - Element invisible: {selector_element}")
            return True
        except TimeoutException:
            print(f"[{self.get_current_time()}] - Timeout waiting for element to be invisible: {selector_element}")
            return False
        except Exception as e:
            print(f"[{self.get_current_time()}] - Error occurred while waiting for invisibility of {selector_element}: {e}")
            return False

        # Wait for a loader to disappear
    def wait_for_loader_invisibility(self, selector_element, wait_for_invisibility=60):
        try:
            # Wait for the loader to become invisible
            WebDriverWait(self.driver, wait_for_invisibility).until(
                EC.invisibility_of_element_located((By.XPATH, selector_element))
            )
            print(f"Loader invisible: {selector_element}")
            return True
        except TimeoutException:
            print(f"Timeout waiting for loader to be invisible: {selector_element}")
            return False
        except Exception as e:
            print(f"Error while waiting for loader invisibility: {e}")
            return False

        # Fetch dropdown options and select a random one

    def get_options(self, by_selector, options_locator):
        options = []
        try:
            # Reduce timeout to speed up execution and try using presence instead of visibility
            timeout = 2  # Reduced wait time

            # Use presence_of_all_elements_located for faster results
            if by_selector == "xpath":
                options = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_all_elements_located((By.XPATH, options_locator))
                )
            elif by_selector == "id":
                options = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_all_elements_located((By.ID, options_locator))
                )

            if options:
                # Choose a random option and return its text
                selected_option = random.choice(options)
                selected_option_text = selected_option.text
                print(f"[{self.get_current_time()}] - Selected option: {selected_option_text}")
                return str(selected_option_text)
            else:
                print(f"[{self.get_current_time()}] - No options found with locator: {options_locator}")
                return None

        except WebDriverException as exception:
            print(exception.msg)
            print(f"[{self.get_current_time()}] - Unable to get options from dropdown: {options_locator}")
            return None

    def wait_for_visibility_of_element_located_instant(self, by_selector, selector_element):
        try:
            # Find element immediately
            if by_selector == "xpath":
                element = self.driver.find_element(By.XPATH, selector_element)
            elif by_selector == "id":
                element = self.driver.find_element(By.ID, selector_element)
            else:
                print(f"[{self.get_current_time()}] - Invalid selector type: {by_selector}")
                return False

            # Verify visibility of element
            if element.is_displayed():
                print(f"[{self.get_current_time()}] - Element visible: {selector_element}")
                return True
            else:
                print(f"[{self.get_current_time()}] - Element found but not visible: {selector_element}")
                return False

        except NoSuchElementException:
            print(f"[{self.get_current_time()}] - Element not found: {selector_element}")
            return False
        except StaleElementReferenceException:
            print(f"[{self.get_current_time()}] - Element is stale and no longer attached to the DOM: {selector_element}")
            return False
        except Exception as e:
            print(f"[{self.get_current_time()}] - Error occurred while checking element visibility: {e}")
            return False

    def select_gender(self):
        self.click_element('xpath', "//button[contains(@id,'IdPaxGender') and not(contains(@class,'has-value'))]")
        selected_value = self.get_options('xpath', "//li/button[@class='ui-dropdown_item_option']")
        if selected_value:
            self.click_element('xpath', f"//li[starts-with(@class,'ui-dropdown_item') and contains(.,'{selected_value}')]")


    def type_first_name(self, text):
        self.type_text('xpath', "//*[contains(@id,'IdFirstName') and not(contains(@class,'has-value'))]", text)

    def type_last_name(self, text):
        self.type_text('xpath', "//*[contains(@id,'IdLastName') and not(contains(@class,'has-value'))]", text)

    def type_first_name_av_credits(self, text):
        self.type_text('xpath', "(//*[contains(@id,'IdFirstName')])[1]", text)

    def type_last_name_av_credits(self, text):
        self.wait_for_invisibility_of_element_located('xpath', "//*[contains(@id,'IdFirstName') and not(contains(@class,'has-value'))]")
        self.type_text('xpath', "(//*[contains(@id,'IdLastName')])[1]", text)

    def select_day(self):
        self.click_element('xpath', "//*[starts-with(@id,'dateDayId_')][not(contains(@class,'has-value'))]")
        selected_value = self.get_options('xpath', "//li/button[@class='ui-dropdown_item_option']")
        if selected_value:
            self.click_element('xpath', f"//li[starts-with(@class,'ui-dropdown_item') and contains(.,'{selected_value}')]")
   

    def select_month(self):
        self.click_element('xpath', "//*[starts-with(@id,'dateMonthId_')][not(contains(@class,'has-value'))]")
        selected_value = self.get_options('xpath', "//li/button[@class='ui-dropdown_item_option']")
        if selected_value:
            self.click_element('xpath', f"//li[starts-with(@class,'ui-dropdown_item') and contains(.,'{selected_value}')]")


    def select_year(self):
        self.click_element('xpath', "//*[starts-with(@id,'dateYearId_')][not(contains(@class,'has-value'))]")
        selected_value = self.get_options('xpath', "//li/button[@class='ui-dropdown_item_option']")
        if selected_value:
            self.click_element('xpath', f"//li[starts-with(@class,'ui-dropdown_item') and contains(.,'{selected_value}')]")
    

    def select_exp_day(self):
        self.click_element('xpath', "//button[starts-with(@id,'dateDayId_IdDocExpDate') and not(contains(@class,'has-value'))]")
        selected_value = self.get_options('xpath', "//li/button[@class='ui-dropdown_item_option']")
        if selected_value:
            self.click_element('xpath', f"//li[starts-with(@class,'ui-dropdown_item') and contains(.,'{selected_value}')]")

    def look_for_exp_day(self):
        return self.wait_for_visibility_of_element_located_instant('xpath', "//button[starts-with(@id,'dateDayId_IdDocExpDate') and not(contains(@class,'has-value'))]")

    def select_exp_month(self):
        self.click_element('xpath', "//button[starts-with(@id,'dateMonthId_IdDocExpDate') and not(contains(@class,'has-value'))]")
        selected_value = self.get_options('xpath', "//li/button[@class='ui-dropdown_item_option']")
        if selected_value:
            self.click_element('xpath', f"//li[starts-with(@class,'ui-dropdown_item') and contains(.,'{selected_value}')]")

    def select_exp_year(self):
        self.click_element('xpath', "//button[starts-with(@id,'dateYearId_IdDocExpDate') and not(contains(@class,'has-value'))]")
        selected_value = self.get_options('xpath', "//li/button[@class='ui-dropdown_item_option']")
        if selected_value:
            self.click_element('xpath', f"//li[starts-with(@class,'ui-dropdown_item') and contains(.,'{selected_value}')]")

    def select_document_type(self):
        self.click_element('xpath', "//button[starts-with(@id,'IdDocType') and not(contains(@class,'has-value'))]")
        selected_value = self.get_options('xpath', "//li/button[@class='ui-dropdown_item_option']")
        if selected_value:
            self.click_element('xpath', f"//li[starts-with(@class,'ui-dropdown_item') and contains(.,'{selected_value}')]")

    def look_for_document_type(self):
        return self.wait_for_visibility_of_element_located_instant('xpath', "//button[starts-with(@id,'IdDocType') and not(contains(@class,'has-value'))]")

    def type_document_number(self, text):
        self.type_text('xpath', "//*[starts-with(@id,'IdDocNum') and not(contains(@class,'has-value'))]", text)

    def select_nationality(self):
        self.click_element('xpath', "//button[starts-with(@id,'IdDocNationality') and not(contains(@class,'has-value'))]")
        self.click_element('xpath', f"(//button[starts-with(@class,'ui-dropdown_item') and not(contains(@style,'none'))])[{(random.randint(1, 240))}]")

    def select_booking_titular(self):
        self.click_element('xpath', "//div[@class='account-passenger']")

    def type_phone_number(self, phone_prefix, phone_number):
        self.click_element('xpath', "phone_prefixPhoneId")
        self.type_text('xpath', "phone_phoneNumberId", phone_number)

    def type_email_address(self, email):
        self.type_text('xpath', "//*[@id='email'][not(contains(@class, 'has-value'))]", email)

    def type_email_address_confirmation(self, email_confirmation):
        self.type_text('xpath', "confirmEmail", email_confirmation)
    
    def prevent_inactivity(self):
        self.driver.execute_script("document.body.dispatchEvent(new MouseEvent('mousemove'));")


# Fixture para usar SeleniumHelper en pruebas
@pytest.fixture
def helper():
    helper = SeleniumHelper()
    yield helper
    helper.close()


# Main test
@pytest.mark.test
def test_main(helper):
    """Main test to execute the specified steps."""
    helper.load_url("https://nuxqa2.avtest.ink/en")

    # 1. Click on the origin field
    helper.click_element("xpath", "//div[@id='originDiv']/input | //div[@id='originDiv']/button")
    # 2. Enter "BOG" in the origin field
    helper.type_text("xpath", "//div[@id='originDiv']//input", "BOG")
    # 3. Click on the button with ID "BOG"
    helper.click_element("xpath", "//button[@id='BOG']")
    # 4. Enter "MGA" in the destination field
    helper.type_text("xpath", "//div[@id='arrivalStationInputLabel']/following-sibling::input", "MGA")
    # 5. Click on the button with ID "MDE"
    helper.click_element("xpath", "//button[@id='MGA']")
    # 6. Click on the passenger selector
    helper.click_element("xpath", "//div[@class='control_field_button_value']")
    # 7. Increase the number of adults 8 times
    for _ in range(8):
        helper.click_element("xpath", "//ul[contains(@attr.aria-labelledby,'ibeSearchPaxControlLabel')]/li[1]/div[2]/ibe-minus-plus/div/button[2]")
    # 8. Increase the number of infants 9 times
    for _ in range(9):
        helper.click_element("xpath", "//ul[contains(@attr.aria-labelledby,'ibeSearchPaxControlLabel')]/li[4]/div[2]/ibe-minus-plus/div/button[2]")
    # 9. Click on the button to confirm passengers
    helper.click_element("xpath", "//*[@class='button control_options_selector_action_button']")
    # 10. Click on the search button
    helper.click_element("xpath", "//*[@id='searchButton' and not(contains(@style,'display:none;'))]")

    # 11. Wait for the loader to disappear
    helper.wait_for_loader_invisibility("//div[contains(@class,'loading')]", 60)
    # 12. Assert that the element with the class "journey-no-data" is not visible
    assert not helper.wait_for_visibility_of_element_located("xpath", "//div[contains(@class,'journey-no-data')]", 4), "No flight(s) available"
    # 13. Assert that the element with the class "day-selector_container" is visible instantly
    assert helper.wait_for_visibility_of_element_located("xpath", "//*[@class='day-selector_container']"), "Week calendar was not visible"
    # 14. Wait for visibility and click on the filter button
    helper.wait_for_visibility_of_element_located("xpath", "//div[@class='filters-control_button']")
    helper.click_element("xpath", "//div[@class='filters-control_button']")
    # 15. Click on the journey select option
    helper.click_element("xpath", "//div[2]/div[starts-with(@class,'journey-select_list ng-star-inserted')]/div/journey-control-custom/div/div/div/div[2]")
    # 16. Click on the fare control options
    helper.click_element("xpath", "//div[contains(@class,'fare-control')][contains(.,'light') or contains(.,'basic') or contains(.,'classic') or contains(.,'flex') or contains(.,'business')]")
    # 17. Wait for the loader to disappear
    helper.wait_for_loader_invisibility("//div[contains(@class,'loading')]",40)
    # 18. Assert again that no flight data is visible
    assert not helper.wait_for_visibility_of_element_located("xpath", "//div[contains(@class,'journey-no-data')]", 4), "No flight(s) available"
    # 19. Click again on the journey select option
    helper.click_element("xpath", "//div[2]/div[starts-with(@class,'journey-select_list ng-star-inserted')]/div/journey-control-custom/div/div/div/div[2]")
    # 20. Click on the fare control options again
    helper.click_element("xpath", "//div[contains(@class,'fare-control')][contains(.,'light') or contains(.,'basic') or contains(.,'classic') or contains(.,'flex') or contains(.,'business')]")
    # 21. Wait for the loader to disappear
    helper.wait_for_loader_invisibility("//div[contains(@class,'loading')]", 40)
    # 22. Click on the page button
    helper.click_element("xpath", "//button[contains(@class,'page_button-primary-flow')]")
    # 23. Wait for the loader to disappear again
    helper.wait_for_loader_invisibility("//div[contains(@class,'loading')]", 60)

    # The while loop starts here
    while helper.wait_for_visibility_of_element_located("xpath", "//button[starts-with(@id,'IdDocNationality') and not(contains(@class,'has-value'))]", 2):
        helper.prevent_inactivity()
        helper.select_gender()
        helper.type_first_name("firstName")
        helper.type_last_name("lastName")
        helper.select_year()
        helper.select_month()
        helper.select_day()
        if helper.look_for_document_type():
            helper.select_document_type()
            helper.type_document_number("123456789")
            if helper.look_for_exp_day():
                helper.select_exp_year()
                helper.select_exp_month()
                helper.select_exp_day()
        helper.select_nationality()

    helper.click_element("xpath","//button[@class='button modal_footer_button-action']")
    # 24. Type the phone number
    helper.type_text("xpath", "//*[@id='phone_phoneNumberId']", "32112345633")

    # 25. Click and scroll on the phone prefix selector
    helper.click_element("xpath", "//*[@id='phone_prefixPhoneId']")
    helper.click_element('xpath', f"(//button[starts-with(@class,'ui-dropdown_item') and not(contains(@style,'none'))])[{random.randint(1, 239)}]")

    # 26. Type the email
    helper.type_text("xpath", "//*[@id='email'][not(contains(@class, 'has-value'))]", "s@a.com")
