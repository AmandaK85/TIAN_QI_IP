# ===== Imports =====
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pytest
import os
import time
from datetime import datetime
import logging
import sys
import traceback
from typing import Dict, List, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_reports.test_report import TestReport, TestCase, TestStep, track_step, create_test_case

class WebsiteTestTemplate:
    def __init__(self, config: Dict):
        """
        Initialize the test template with configuration
        
        Args:
            config: Dictionary containing test configuration including:
                - base_url: Base URL of the website
                - credentials: Dictionary of test credentials
                - selectors: Dictionary of page element selectors
                - test_data: Dictionary of test data
        """
        self.config = config
        self.driver = None
        self.wait = None
        self.report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
        
    def setup(self) -> None:
        """Initialize WebDriver and create report directory"""
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()
        
    def teardown(self) -> None:
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            
    def create_report_dir(self, test_name: str) -> str:
        """
        Creates a unique report directory with timestamp
        
        Args:
            test_name: Name of the test for the directory
            
        Returns:
            str: Path to created directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_dir = os.path.join(self.report_dir, f"{test_name}_{timestamp}")
        os.makedirs(test_dir, exist_ok=True)
        return test_dir
        
    def find_element_with_fallback(self, 
                                 selector_list: List[str], 
                                 timeout: int = 20, 
                                 description: str = "element") -> WebDriver:
        """
        Find element using fallback selectors with improved error handling
        
        Args:
            selector_list: List of XPath selectors to try in order
            timeout: Maximum time to wait for element
            description: Description of element for error messages
        
        Returns:
            WebElement: Found element
            
        Raises:
            TimeoutException: If no selector works
        """
        wait = WebDriverWait(self.driver, timeout)
        
        for i, selector in enumerate(selector_list):
            try:
                print(f"Trying selector {i+1}/{len(selector_list)} for {description}: {selector}")
                element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                print(f"✅ Found {description} using selector {i+1}")
                return element
            except TimeoutException:
                print(f"⚠️ Selector {i+1} failed for {description}")
                continue
            except Exception as e:
                print(f"⚠️ Selector {i+1} error for {description}: {str(e)}")
                continue
        
        raise TimeoutException(f"Could not find {description} using any of the {len(selector_list)} selectors")

    def safe_click(self, element: WebDriver, description: str = "element") -> None:
        """
        Safely click an element with JavaScript fallback
        
        Args:
            element: WebElement to click
            description: Description of element for logging
        """
        try:
            element.click()
            print(f"✅ Successfully clicked {description}")
        except Exception as e:
            print(f"⚠️ Regular click failed for {description}, trying JavaScript click: {str(e)}")
            try:
                self.driver.execute_script("arguments[0].click();", element)
                print(f"✅ Successfully clicked {description} using JavaScript")
            except Exception as js_e:
                print(f"❌ JavaScript click also failed for {description}: {str(js_e)}")
                raise

    def login(self, test_case: TestCase, credentials: Dict) -> None:
        """
        Generic login function
        
        Args:
            test_case: TestCase object for reporting
            credentials: Dictionary containing login credentials
        """
        with track_step(test_case, "Login", "Logging into the website"):
            try:
                # Navigate to login page
                print(f"Navigating to login page: {self.config['base_url']}/login")
                self.driver.get(f"{self.config['base_url']}/login")
                time.sleep(3)
                
                # Find and fill login fields
                username_input = self.find_element_with_fallback(
                    self.config['selectors']['login']['username_input'],
                    description="username input"
                )
                username_input.send_keys(credentials['username'])
                
                password_input = self.find_element_with_fallback(
                    self.config['selectors']['login']['password_input'],
                    description="password input"
                )
                password_input.send_keys(credentials['password'])
                
                # Click login button
                login_button = self.find_element_with_fallback(
                    self.config['selectors']['login']['login_button'],
                    description="login button"
                )
                self.safe_click(login_button, "login button")
                
            except Exception as e:
                print(f"❌ Login failed: {str(e)}")
                raise

    def select_item(self, test_case: TestCase, item_selectors: List[str], description: str) -> None:
        """
        Generic function to select an item (product, package, etc.)
        
        Args:
            test_case: TestCase object for reporting
            item_selectors: List of selectors for the item
            description: Description of the item for logging
        """
        with track_step(test_case, f"Select {description}", f"Selecting {description}"):
            item = self.find_element_with_fallback(item_selectors, description=description)
            self.safe_click(item, description)

    def complete_payment(self, test_case: TestCase, payment_method: str) -> None:
        """
        Generic payment completion function
        
        Args:
            test_case: TestCase object for reporting
            payment_method: Payment method to use
        """
        with track_step(test_case, "Complete Payment", f"Completing payment using {payment_method}"):
            # Select payment method
            payment_selector = self.config['selectors']['payment'][payment_method]
            payment_option = self.find_element_with_fallback(payment_selector, description=f"{payment_method} payment option")
            self.safe_click(payment_option, f"{payment_method} payment option")
            
            # Click payment button
            pay_button = self.find_element_with_fallback(
                self.config['selectors']['buttons']['pay_now'],
                description="pay now button"
            )
            self.safe_click(pay_button, "pay now button")
            
            # Handle payment confirmation if needed
            if payment_method in self.config['selectors'].get('payment_confirmation', {}):
                self._handle_payment_confirmation(payment_method)

    def _handle_payment_confirmation(self, payment_method: str) -> None:
        """
        Handle payment confirmation steps for specific payment methods
        
        Args:
            payment_method: Payment method being used
        """
        confirmation_selectors = self.config['selectors']['payment_confirmation'][payment_method]
        for step in confirmation_selectors:
            element = self.find_element_with_fallback(
                step['selectors'],
                description=step['description']
            )
            if step.get('input'):
                element.send_keys(step['input'])
            else:
                self.safe_click(element, step['description'])
            
            if step.get('wait_time'):
                time.sleep(step['wait_time'])

    def verify_success(self, test_case: TestCase) -> None:
        """
        Verify successful completion of the test
        
        Args:
            test_case: TestCase object for reporting
        """
        with track_step(test_case, "Verify Success", "Verifying successful completion"):
            success_message = self.find_element_with_fallback(
                self.config['selectors']['status']['success_message'],
                description="success message"
            )
            assert success_message.is_displayed(), "Success message not displayed"

    def handle_error(self, test_case: TestCase, expected_error: Optional[str] = None) -> None:
        """
        Handle and verify error messages
        
        Args:
            test_case: TestCase object for reporting
            expected_error: Expected error message (if any)
        """
        with track_step(test_case, "Handle Error", "Handling error message"):
            error_message = self.find_element_with_fallback(
                self.config['selectors']['status']['error_message'],
                description="error message"
            )
            if expected_error:
                assert expected_error in error_message.text, f"Expected error '{expected_error}' not found"
