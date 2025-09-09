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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_reports.test_report import TestReport, TestCase, TestStep, track_step, create_test_case

# ===== Global Configuration =====
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
driver.maximize_window()

report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

# ===== Login Credentials =====
LOGIN_URL = "https://test-ip-tianqi.cd.xiaoxigroup.net/login"
PHONE_WITH_BALANCE = "15332595364"
PHONE_WITHOUT_BALANCE = "15658873355"
PASSWORD = "Test@123"

# ===== Utility Functions =====
def create_report_dir():
    """Creates a unique report directory with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_dir = os.path.join(report_dir, f"website_Payment_Tests_{timestamp}")
    os.makedirs(test_dir, exist_ok=True)
    return test_dir

def login_with_balance(test_case):
    """Login with account that has balance"""
    with track_step(test_case, "Login", "Login with account that has balance"):
        try:
            # Navigate to login page
            print(f"Navigating to login page: {LOGIN_URL}")
            driver.get(LOGIN_URL)
            time.sleep(3)
            
            # Print current URL to verify we're on the right page
            print(f"Current URL: {driver.current_url}")
            
            # Check if we're already logged in (redirected to main page)
            if "/packageOrder" in driver.current_url or driver.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/":
                print("Already logged in or redirected to main page")
                return
            
            # Try to find phone input field
            phone_input = wait.until(EC.element_to_be_clickable(
                (By.ID, "__BVID__23")))
            print("Phone input field found")
            phone_input.clear()
            phone_input.send_keys(PHONE_WITH_BALANCE)
            print(f"Entered phone number: {PHONE_WITH_BALANCE}")
            
            # Try to find password input field
            password_input = wait.until(EC.element_to_be_clickable(
                (By.ID, "__BVID__24")))
            print("Password input field found")
            password_input.clear()
            password_input.send_keys(PASSWORD)
            print("Entered password")
            
            # Try to find login button
            login_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), '登录')]")))
            print("Login button found")
            driver.execute_script("arguments[0].click();", login_button)
            print("Clicked login button")
            
            # Wait a bit and check what happened
            time.sleep(5)
            print(f"After login click, current URL: {driver.current_url}")
            
            # Check if login was successful by looking for user info or redirect
            try:
                # Wait for redirect to main page or package order page
                print("Waiting for redirect after login...")
                wait.until(lambda d: "/packageOrder" in d.current_url or d.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/")
                
                if driver.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/":
                    print("✅ Successfully logged in - redirected to main page")
                else:
                    print("✅ Successfully logged in - redirected to package order page")
                    
            except TimeoutException:
                # Check for error messages
                try:
                    error_msg = driver.find_element(By.XPATH, "//div[contains(text(), '错误') or contains(text(), 'error') or contains(text(), '失败')]")
                    raise Exception(f"Login failed: {error_msg.text}")
                except NoSuchElementException:
                    print(f"Current page title: {driver.title}")
                    raise Exception("Login failed - no redirect to expected page")
            
        except Exception as e:
            print(f"Login failed with error: {str(e)}")
            print(f"Current page source: {driver.page_source[:1000]}...")
            raise

def login_without_balance(test_case):
    """Login with account that has no balance"""
    with track_step(test_case, "Login", "Login with account that has no balance"):
        try:
            # Navigate to login page
            print(f"Navigating to login page: {LOGIN_URL}")
            driver.get(LOGIN_URL)
            time.sleep(3)
            
            # Print current URL to verify we're on the right page
            print(f"Current URL: {driver.current_url}")
            
            # Check if we're already logged in (redirected to main page)
            if "/packageOrder" in driver.current_url or driver.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/":
                print("Already logged in or redirected to main page")
                return
            
            # Try to find phone input field
            phone_input = wait.until(EC.element_to_be_clickable(
                (By.ID, "__BVID__23")))
            phone_input.clear()
            phone_input.send_keys(PHONE_WITHOUT_BALANCE)
            print(f"Entered phone number: {PHONE_WITHOUT_BALANCE}")
            
            # Try to find password input field
            password_input = wait.until(EC.element_to_be_clickable(
                (By.ID, "__BVID__24")))
            password_input.clear()
            password_input.send_keys(PASSWORD)
            print("Entered password")
            
            # Try to find login button
            login_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), '登录')]")))
            driver.execute_script("arguments[0].click();", login_button)
            print("Clicked login button")
            
            # Wait a bit and check what happened
            time.sleep(5)
            print(f"After login click, current URL: {driver.current_url}")
            
            # Check if login was successful by looking for user info or redirect
            try:
                # Wait for redirect to main page or package order page
                print("Waiting for redirect after login...")
                wait.until(lambda d: "/packageOrder" in d.current_url or d.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/")
                
                if driver.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/":
                    print("✅ Successfully logged in - redirected to main page")
                else:
                    print("✅ Successfully logged in - redirected to package order page")
                    
            except TimeoutException:
                # Check for error messages
                try:
                    error_msg = driver.find_element(By.XPATH, "//div[contains(text(), '错误') or contains(text(), 'error') or contains(text(), '失败')]")
                    raise Exception(f"Login failed: {error_msg.text}")
                except NoSuchElementException:
                    print("No error message found, but login seems to have failed")
                    print(f"Current page title: {driver.title}")
                    raise Exception("Login failed - no redirect to expected page")
            
        except Exception as e:
            print(f"Login failed with error: {str(e)}")
            print(f"Current page source: {driver.page_source[:1000]}...")
            raise

def navigate_to_package_order():
    """Navigation flow to package order page"""
    print(f"Navigating to package order page")
    
    # If we're already on the package order page, don't navigate again
    if "/packageOrder" in driver.current_url:
        print("Already on package order page")
        return
    
    # Navigate to package order page
    driver.get("https://test-ip-tianqi.cd.xiaoxigroup.net/packageOrder")
    time.sleep(3)
    
    print(f"After navigation, current URL: {driver.current_url}")
    
    # Check if we need to login again (redirected to login page)
    if "/login" in driver.current_url:
        print("Redirected to login page, attempting login again...")
        login_with_balance(None)  # We'll create a dummy test case
        driver.get("https://test-ip-tianqi.cd.xiaoxigroup.net/packageOrder")
        time.sleep(3)

# ===== Test Steps =====
def select_dynamic_supreme(test_case):
    """Select Dynamic Supreme package"""
    with track_step(test_case, "Select Package", "Select Dynamic Supreme package"):
        package = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), '天启动态尊享')]")))
        driver.execute_script("arguments[0].click();", package)
        time.sleep(2)

def select_Static_IP(test_case):
    """Select Static IP package"""
    with track_step(test_case, "Select Package", "Select Static IP package"):
        package = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), '静态IP-天启')]")))
        driver.execute_script("arguments[0].click();", package)
        time.sleep(2)

def select_Dynamic_Standard(test_case):
    """Select Dynamic Standard package"""
    with track_step(test_case, "Select Package", "Select Dynamic Standard package"):
        package = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), '天启动态标准套餐')]")))
        driver.execute_script("arguments[0].click();", package)
        time.sleep(2)

def select_Dynamic_Dedicated(test_case):
    """Select Dynamic Dedicated package"""
    with track_step(test_case, "Select Package", "Select Dynamic Dedicated package"):
        package = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), '天启动态独享套餐')]")))
        driver.execute_script("arguments[0].click();", package)
        time.sleep(2)

def handle_buy_now(test_case):
    """Click Buy Now button"""
    with track_step(test_case, "Click Buy Now", "Click 立即购买 button"):
        buy_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), '立即购买')]")))
        driver.execute_script("arguments[0].click();", buy_button)
        time.sleep(1)

def select_payment_method(method_name, test_case):
    """Select payment method in popup"""
    with track_step(test_case, "Select Payment", f"Select {method_name} payment"):
        method = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(text(), '{method_name}')]")))
        driver.execute_script("arguments[0].click();", method)
        time.sleep(1)

def click_pay_now(test_case):
    """Click Pay Now button"""
    with track_step(test_case, "Click Pay Now", "Click 立即支付 button"):
        pay_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), '立即支付')]")))
        driver.execute_script("arguments[0].click();", pay_button)
        time.sleep(2)

def click_recharge_now(test_case):
    """Click Recharge Now button (no balance scenario)"""
    with track_step(test_case, "Click Recharge Now", "Click 立即充值 button"):
        # Try to find the specific button with class "buyBt hover text-center" (no balance scenario)
        try:
            recharge_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='buyBt hover text-center' and contains(text(), '立即充值')]")))
            print("Found recharge button with specific class (no balance scenario)")
        except TimeoutException:
            # Fall back to general button search
            recharge_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), '立即充值')]")))
            print("Found recharge button with general selector")
        
        driver.execute_script("arguments[0].click();", recharge_button)
        time.sleep(2)

# ===== Personal Center Test Steps =====
def navigate_to_personal_center(test_case):
    """Navigate to Personal Center account manager page"""
    with track_step(test_case, "Navigate to Personal Center", "Navigate to account manager page"):
        driver.get("https://test-ip-tianqi.cd.xiaoxigroup.net/personal/accountManager")
        time.sleep(3)
        print(f"Navigated to Personal Center. Current URL: {driver.current_url}")

def click_add_paid_account(test_case):
    """Click the 添加付费账户 button"""
    with track_step(test_case, "Click Add Paid Account", "Click 添加付费账户 button"):
        add_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), '添加付费账户')]")))
        driver.execute_script("arguments[0].click();", add_button)
        time.sleep(2)
        print("Clicked add paid account button")

def wait_for_package_popup(test_case):
    """Wait for the package selection popup to appear"""
    with track_step(test_case, "Wait for Popup", "Wait for package selection popup"):
        wait.until(EC.visibility_of_element_located((By.ID, "__BVID__69___BV_modal_header_")))
        time.sleep(5)
        print("package selection popup appeared")

def select_package_type_personal(package_name, test_case):
    """Select package type in Personal Center popup"""
    with track_step(test_case, "Select Package Type", f"Select {package_name} in dropdown"):
        from selenium.webdriver.support.ui import Select
        dropdown = wait.until(EC.presence_of_element_located((By.ID, "__BVID__555")))
        select = Select(dropdown)
        
        # Map package names to their values
        package_mapping = {
            "天启动态尊享": "70",
            "静态IP-天启": "64", 
            "天启动态标准套餐": "28",
            "天启动态独享套餐": "30"
        }
        
        if package_name in package_mapping:
            select.select_by_value(package_mapping[package_name])
            print(f"Selected {package_name} using Select class")
            time.sleep(1)
        else:
            raise Exception(f"Package name {package_name} not found in mapping")

def select_package_type_personal_wallet_no_balance(package_name, test_case):
    """Select package type in Personal Center popup"""
    with track_step(test_case, "Select Package Type", f"Select {package_name} in dropdown"):
        from selenium.webdriver.support.ui import Select
        dropdown = wait.until(EC.presence_of_element_located((By.ID, "__BVID__105")))
        select = Select(dropdown)
        
        # Map package names to their values
        package_mapping = {
            "天启动态尊享": "70",
            "静态IP-天启": "64", 
            "天启动态标准套餐": "28",
            "天启动态独享套餐": "30"
        }
        
        if package_name in package_mapping:
            select.select_by_value(package_mapping[package_name])
            print(f"Selected {package_name} using Select class")
            time.sleep(1)
        else:
            raise Exception(f"Package name {package_name} not found in mapping")
        
def input_random_account(test_case):
    """Input random 8-character alphanumeric string in account field"""
    with track_step(test_case, "Input Account", "Input random 8-character account"):
        import random
        import string
        
        # Generate random 8-character alphanumeric string
        account = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        account_field = wait.until(EC.element_to_be_clickable((By.ID, "__BVID__559")))
        account_field.clear()
        account_field.send_keys(account)
        time.sleep(1)
        print(f"Entered account: {account}")

def input_random_account_personal_wallet_no_balance(test_case):
    """Input random 8-character alphanumeric string in account field"""
    with track_step(test_case, "Input Account", "Input random 8-character account"):
        import random
        import string
        
        # Generate random 8-character alphanumeric string
        account = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        account_field = wait.until(EC.element_to_be_clickable((By.ID, "__BVID__109")))
        account_field.clear()
        account_field.send_keys(account)
        time.sleep(1)
        print(f"Entered account: {account}")

def select_payment_method_personal(method_name, test_case):
    """Select payment method in Personal Center popup"""
    with track_step(test_case, "Select Payment Method", f"Select {method_name} payment"):
        method = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(text(), '{method_name}')]")))
        driver.execute_script("arguments[0].click();", method)
        time.sleep(1)
        print("payment method selected")

def click_pay_personal(test_case):
    """Click Pay button in Personal Center popup"""
    with track_step(test_case, "Click Pay", "Click Pay button"):
        pay_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), '确定')]")))
        driver.execute_script("arguments[0].click();", pay_button)
        print("Clicked 确定 button")
        time.sleep(2)
        print("pay button clicked")

def verify_success_message(test_case):
    """Verify success message appears"""
    with track_step(test_case, "Verify Success", "Check for success message"):
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'ml-20') and contains(text(), '创建成功')]")))
        assert "创建成功" in success_msg.text
        print("✅ Success message verified")

def close_wechat_popup(test_case):
    """Close WeChat QR popup"""
    with track_step(test_case, "Close WeChat Popup", "Close the WeChat QR popup"):
        close_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")))
        driver.execute_script("arguments[0].click();", close_button)
        time.sleep(1)
        print("WeChat popup closed")

def verify_alipay_sandbox(test_case, max_retries=1, retry_delay=3):
    """Verify Alipay sandbox opens with retry logic for intermittent redirects"""
    for attempt in range(max_retries + 1):
        try:
            with track_step(test_case, "Verify Alipay", f"Check Alipay sandbox opens (attempt {attempt + 1})"):
                driver.switch_to.window(driver.window_handles[-1])
                
                # Wait for redirects to complete and verify Alipay sandbox
                wait.until(lambda d: "alipaydev.com" in d.current_url)
                assert "alipaydev.com" in driver.current_url
                print(f"✅ Alipay sandbox verified on attempt {attempt + 1}: {driver.current_url}")
                return True
                
        except Exception as e:
            if attempt < max_retries:
                print(f"⚠️ Alipay verification failed on attempt {attempt + 1}: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Switch back to main window before retry
                driver.switch_to.window(driver.window_handles[0])
            else:
                print(f"❌ Alipay verification failed after {max_retries + 1} attempts: {e}")
                return False
        finally:
            # Switch back to main window
            driver.switch_to.window(driver.window_handles[0])
    
    return False

def verify_recharge_redirect(test_case):
    """Verify redirect to recharge page when no balance"""
    with track_step(test_case, "Verify Recharge Redirect", "Check redirect to recharge page"):
        wait.until(lambda d: "tab=recharge" in d.current_url)
        assert "tab=recharge" in driver.current_url
        print("✅ Recharge redirect verified - no balance detected")

def verify_insufficient_balance_error(test_case):
    """Verify insufficient balance error message appears"""
    with track_step(test_case, "Verify Insufficient Balance Error", "Check for insufficient balance error message"):
        error_msg = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'ml-20') and contains(text(), '账户余额不足')]")))
        assert "账户余额不足" in error_msg.text
        print("✅ Insufficient balance error message verified")
# ===== Test Cases Dynamic Supreme =====
def test_balance_sufficient(report_dir, test_case):
    """Test balance payment with sufficient funds"""
    test_case.start()
    try:
        login_with_balance(test_case)
        navigate_to_package_order()
        select_dynamic_supreme(test_case)
        handle_buy_now(test_case)
        select_payment_method("余额", test_case)
        click_pay_now(test_case)
        
        # Verify success popup
        with track_step(test_case, "Verify Success", "Check purchase success message"):
            success_msg = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), '套餐购买成功')]")))
            assert "套餐购买成功" in success_msg.text
            
            # Close success popup
            with track_step(test_case, "Close Success Popup", "Close the success popup"):
                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'fee-header') and contains(text(), '×')]")))
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1)
                print("Success popup closed")
            
            return True
            
    except Exception as e:
        print(f"Balance sufficient test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_alipay_payment(report_dir, test_case):
    """Test Alipay payment flow"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_dynamic_supreme(test_case)
        handle_buy_now(test_case)
        select_payment_method("支付宝", test_case)
        click_pay_now(test_case)
        
        # Verify Alipay sandbox
        if not verify_alipay_sandbox(test_case):
            return False
        return True
            
    except Exception as e:
        print(f"Alipay test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_wechat_payment(report_dir, test_case):
    """Test WeChat payment flow"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_dynamic_supreme(test_case)
        handle_buy_now(test_case)
        select_payment_method("微信", test_case)
        click_pay_now(test_case)
        
        # Verify WeChat QR
        with track_step(test_case, "Verify WeChat", "Check QR code appears"):
            qr_code = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), '微信扫码支付')]")))
            assert qr_code.is_displayed()
            
            # Close WeChat QR popup
            with track_step(test_case, "Close WeChat QR Popup", "Close the WeChat QR popup"):
                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")))
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1)
                print("WeChat QR popup closed")
            
            return True
            
    except Exception as e:
        print(f"WeChat test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

# ===== Test Cases Static IP =====
def test_balance_sufficient_static(report_dir, test_case):
    """Test balance payment with sufficient funds for Static IP"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Static_IP(test_case)
        handle_buy_now(test_case)
        select_payment_method("余额", test_case)
        click_pay_now(test_case)
        
        # Verify success popup
        with track_step(test_case, "Verify Success", "Check purchase success message"):
            success_msg = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), '套餐购买成功')]")))
            assert "套餐购买成功" in success_msg.text
            
            # Close success popup
            with track_step(test_case, "Close Success Popup", "Close the success popup"):
                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'fee-header') and contains(text(), '×')]")))
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1)
                print("Success popup closed")
            
            return True
            
    except Exception as e:
        print(f"Balance sufficient test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_alipay_payment_static(report_dir, test_case):
    """Test Alipay payment flow for Static IP"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Static_IP(test_case)
        handle_buy_now(test_case)
        select_payment_method("支付宝", test_case)
        click_pay_now(test_case)
        
        # Verify Alipay sandbox
        if not verify_alipay_sandbox(test_case):
            return False
        return True
            
    except Exception as e:
        print(f"Alipay test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_wechat_payment_static(report_dir, test_case):
    """Test WeChat payment flow for Static IP"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Static_IP(test_case)
        handle_buy_now(test_case)
        select_payment_method("微信", test_case)
        click_pay_now(test_case)
        
        # Verify WeChat QR
        with track_step(test_case, "Verify WeChat", "Check QR code appears"):
            qr_code = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), '微信扫码支付')]")))
            assert qr_code.is_displayed()
            
            # Close WeChat QR popup
            with track_step(test_case, "Close WeChat QR Popup", "Close the WeChat QR popup"):
                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")))
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1)
                print("WeChat QR popup closed")
            
            return True
            
    except Exception as e:
        print(f"WeChat test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

# ===== Test Cases Dynamic Standard =====
def test_balance_sufficient_standard(report_dir, test_case):
    """Test balance payment with sufficient funds for Dynamic Standard"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Dynamic_Standard(test_case)
        handle_buy_now(test_case)
        select_payment_method("余额", test_case)
        click_pay_now(test_case)
        
        # Verify success popup
        with track_step(test_case, "Verify Success", "Check purchase success message"):
            success_msg = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), '套餐购买成功')]")))
            assert "套餐购买成功" in success_msg.text
            
            # Close success popup
            with track_step(test_case, "Close Success Popup", "Close the success popup"):
                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'fee-header') and contains(text(), '×')]")))
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1)
                print("Success popup closed")
            
            return True
            
    except Exception as e:
        print(f"Balance sufficient test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_alipay_payment_standard(report_dir, test_case):
    """Test Alipay payment flow for Dynamic Standard"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Dynamic_Standard(test_case)
        handle_buy_now(test_case)
        select_payment_method("支付宝", test_case)
        click_pay_now(test_case)
        
        # Verify Alipay sandbox
        if not verify_alipay_sandbox(test_case):
            return False
        return True
            
    except Exception as e:
        print(f"Alipay test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_wechat_payment_standard(report_dir, test_case):
    """Test WeChat payment flow for Dynamic Standard"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Dynamic_Standard(test_case)
        handle_buy_now(test_case)
        select_payment_method("微信", test_case)
        click_pay_now(test_case)
        
        # Verify WeChat QR
        with track_step(test_case, "Verify WeChat", "Check QR code appears"):
            qr_code = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), '微信扫码支付')]")))
            assert qr_code.is_displayed()
            
            # Close WeChat QR popup
            with track_step(test_case, "Close WeChat QR Popup", "Close the WeChat QR popup"):
                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")))
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1)
                print("WeChat QR popup closed")
            
            return True
            
    except Exception as e:
        print(f"WeChat test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

# ===== Test Cases Dynamic Dedicated =====
def test_balance_sufficient_dedicated(report_dir, test_case):
    """Test balance payment with sufficient funds for Dynamic Dedicated"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Dynamic_Dedicated(test_case)
        handle_buy_now(test_case)
        select_payment_method("余额", test_case)
        click_pay_now(test_case)
        
        # Verify success popup
        with track_step(test_case, "Verify Success", "Check purchase success message"):
            success_msg = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), '套餐购买成功')]")))
            assert "套餐购买成功" in success_msg.text
            
            # Close success popup
            with track_step(test_case, "Close Success Popup", "Close the success popup"):
                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'fee-header') and contains(text(), '×')]")))
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1)
                print("Success popup closed")
            
            return True
            
    except Exception as e:
        print(f"Balance sufficient test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_alipay_payment_dedicated(report_dir, test_case):
    """Test Alipay payment flow for Dynamic Dedicated"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Dynamic_Dedicated(test_case)
        handle_buy_now(test_case)
        select_payment_method("支付宝", test_case)
        click_pay_now(test_case)
        
        # Verify Alipay sandbox
        if not verify_alipay_sandbox(test_case):
            return False
        return True
            
    except Exception as e:
        print(f"Alipay test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_wechat_payment_dedicated(report_dir, test_case):
    """Test WeChat payment flow for Dynamic Dedicated"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Dynamic_Dedicated(test_case)
        handle_buy_now(test_case)
        select_payment_method("微信", test_case)
        click_pay_now(test_case)
        
        # Verify WeChat QR
        with track_step(test_case, "Verify WeChat", "Check QR code appears"):
            qr_code = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), '微信扫码支付')]")))
            assert qr_code.is_displayed()
            
            # Close WeChat QR popup
            with track_step(test_case, "Close WeChat QR Popup", "Close the WeChat QR popup"):
                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")))
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1)
                print("WeChat QR popup closed")
            
            return True
            
    except Exception as e:
        print(f"WeChat test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_wechat_dedicated(report_dir, test_case):
    """Test WeChat payment for Dynamic Dedicated in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态独享套餐", test_case)
        input_random_account(test_case)
        select_payment_method_personal("微信", test_case)
        click_pay_personal(test_case)
        close_wechat_popup(test_case)
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Dedicated WeChat test failed: {str(e)}")
        return False
    finally:
        test_case.complete()
        
# ===== Test Cases Personal Center =====
def test_personal_balance_supreme(report_dir, test_case):
    """Test balance payment for Dynamic Supreme in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态尊享", test_case)
        input_random_account(test_case)
        select_payment_method_personal("余额", test_case)
        click_pay_personal(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Supreme Balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_alipay_supreme(report_dir, test_case):
    """Test Alipay payment for Dynamic Supreme in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态尊享", test_case)
        input_random_account(test_case)
        select_payment_method_personal("支付宝", test_case)
        click_pay_personal(test_case)
        if not verify_alipay_sandbox(test_case):
            return False
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Supreme Alipay test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_wechat_supreme(report_dir, test_case):
    """Test WeChat payment for Dynamic Supreme in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态尊享", test_case)
        input_random_account(test_case)
        select_payment_method_personal("微信", test_case)
        click_pay_personal(test_case)
        close_wechat_popup(test_case)
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Supreme WeChat test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_balance_static(report_dir, test_case):
    """Test balance payment for Static IP in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("静态IP-天启", test_case)
        input_random_account(test_case)
        select_payment_method_personal("余额", test_case)
        click_pay_personal(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Personal Center Static IP Balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_alipay_static(report_dir, test_case):
    """Test Alipay payment for Static IP in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("静态IP-天启", test_case)
        input_random_account(test_case)
        select_payment_method_personal("支付宝", test_case)
        click_pay_personal(test_case)
        if not verify_alipay_sandbox(test_case):
            return False
        return True
    except Exception as e:
        print(f"Personal Center Static IP Alipay test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_wechat_static(report_dir, test_case):
    """Test WeChat payment for Static IP in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("静态IP-天启", test_case)
        input_random_account(test_case)
        select_payment_method_personal("微信", test_case)
        click_pay_personal(test_case)
        close_wechat_popup(test_case)
        return True
    except Exception as e:
        print(f"Personal Center Static IP WeChat test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_balance_standard(report_dir, test_case):
    """Test balance payment for Dynamic Standard in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态标准套餐", test_case)
        input_random_account(test_case)
        select_payment_method_personal("余额", test_case)
        click_pay_personal(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Standard Balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_alipay_standard(report_dir, test_case):
    """Test Alipay payment for Dynamic Standard in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态标准套餐", test_case)
        input_random_account(test_case)
        select_payment_method_personal("支付宝", test_case)
        click_pay_personal(test_case)
        if not verify_alipay_sandbox(test_case):
            return False
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Standard Alipay test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_wechat_standard(report_dir, test_case):
    """Test WeChat payment for Dynamic Standard in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态标准套餐", test_case)
        input_random_account(test_case)
        select_payment_method_personal("微信", test_case)
        click_pay_personal(test_case)
        close_wechat_popup(test_case)
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Standard WeChat test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_balance_dedicated(report_dir, test_case):
    """Test balance payment for Dynamic Dedicated in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态独享套餐", test_case)
        input_random_account(test_case)
        select_payment_method_personal("余额", test_case)
        click_pay_personal(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Dedicated Balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_alipay_dedicated(report_dir, test_case):
    """Test Alipay payment for Dynamic Dedicated in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态独享套餐", test_case)
        input_random_account(test_case)
        select_payment_method_personal("支付宝", test_case)
        click_pay_personal(test_case)
        if not verify_alipay_sandbox(test_case):
            return False
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Dedicated Alipay test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_wechat_dedicated(report_dir, test_case):
    """Test WeChat payment for Dynamic Dedicated in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal("天启动态独享套餐", test_case)
        input_random_account(test_case)
        select_payment_method_personal("微信", test_case)
        click_pay_personal(test_case)
        close_wechat_popup(test_case)
        return True
    except Exception as e:
        print(f"Personal Center Dynamic Dedicated WeChat test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

# ===== Test Cases No Balance =====
def test_wallet_no_balance_supreme(report_dir, test_case):
    """Test wallet payment with no balance for Dynamic Supreme"""
    test_case.start()
    try:
        login_without_balance(test_case)
        navigate_to_package_order()
        select_dynamic_supreme(test_case)
        handle_buy_now(test_case)
        select_payment_method("余额", test_case)
        click_recharge_now(test_case)
        
        # Verify recharge redirect
        verify_recharge_redirect(test_case)
        return True
        
    except Exception as e:
        print(f"Wallet no balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_wallet_no_balance_static(report_dir, test_case):
    """Test wallet payment with no balance for Static IP"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Static_IP(test_case)
        handle_buy_now(test_case)
        select_payment_method("余额", test_case)
        click_recharge_now(test_case)
        
        # Verify recharge redirect
        verify_recharge_redirect(test_case)
        return True
        
    except Exception as e:
        print(f"Wallet no balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_wallet_no_balance_standard(report_dir, test_case):
    """Test wallet payment with no balance for Dynamic Standard"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Dynamic_Standard(test_case)
        handle_buy_now(test_case)
        select_payment_method("余额", test_case)
        click_recharge_now(test_case)
        
        # Verify recharge redirect
        verify_recharge_redirect(test_case)
        return True
        
    except Exception as e:
        print(f"Wallet no balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_wallet_no_balance_dedicated(report_dir, test_case):
    """Test wallet payment with no balance for Dynamic Dedicated"""
    test_case.start()
    try:
        navigate_to_package_order()
        select_Dynamic_Dedicated(test_case)
        handle_buy_now(test_case)
        select_payment_method("余额", test_case)
        click_recharge_now(test_case)
        
        # Verify recharge redirect
        verify_recharge_redirect(test_case)
        return True
        
    except Exception as e:
        print(f"Wallet no balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_wallet_no_balance_supreme(report_dir, test_case):
    """Test wallet payment with no balance for Dynamic Supreme in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal_wallet_no_balance("天启动态尊享", test_case)
        input_random_account_personal_wallet_no_balance(test_case)
        select_payment_method_personal("余额", test_case)
        click_pay_personal(test_case)
        
        # Verify insufficient balance error message
        verify_insufficient_balance_error(test_case)
        return True
        
    except Exception as e:
        print(f"Personal Center Dynamic Supreme Wallet No Balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_wallet_no_balance_static(report_dir, test_case):
    """Test wallet payment with no balance for Static IP in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal_wallet_no_balance("静态IP-天启", test_case)
        input_random_account_personal_wallet_no_balance(test_case)
        select_payment_method_personal("余额", test_case)
        click_pay_personal(test_case)
        
        # Verify insufficient balance error message
        verify_insufficient_balance_error(test_case)
        return True
        
    except Exception as e:
        print(f"Personal Center Static IP Wallet No Balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_wallet_no_balance_standard(report_dir, test_case):
    """Test wallet payment with no balance for Dynamic Standard in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal_wallet_no_balance("天启动态标准套餐", test_case)
        input_random_account_personal_wallet_no_balance(test_case)
        select_payment_method_personal("余额", test_case)
        click_pay_personal(test_case)
        
        # Verify insufficient balance error message
        verify_insufficient_balance_error(test_case)
        return True
        
    except Exception as e:
        print(f"Personal Center Dynamic Standard Wallet No Balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_personal_wallet_no_balance_dedicated(report_dir, test_case):
    """Test wallet payment with no balance for Dynamic Dedicated in Personal Center"""
    test_case.start()
    try:
        navigate_to_personal_center(test_case)
        click_add_paid_account(test_case)
        wait_for_package_popup(test_case)
        select_package_type_personal_wallet_no_balance("天启动态独享套餐", test_case)
        input_random_account_personal_wallet_no_balance(test_case)
        select_payment_method_personal("余额", test_case)
        click_pay_personal(test_case)
        
        # Verify insufficient balance error message
        verify_insufficient_balance_error(test_case)
        return True
        
    except Exception as e:
        print(f"Personal Center Dynamic Dedicated Wallet No Balance test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

# ===== Main Execution =====
def main():
    report_dir = create_report_dir()
    test_report = TestReport(report_dir)
    test_report.start()

    test_results = {
        "1.1_wallet_balance": False,
        "1.2_alipay": False,
        "1.3_wechat": False,
        "1.4_wallet_no_balance": False,
        "2.1_wallet_balance": False,
        "2.2_alipay": False,
        "2.3_wechat": False,
        "2.4_wallet_no_balance": False,
        "3.1_wallet_balance": False,
        "3.2_alipay": False,
        "3.3_wechat": False,
        "3.4_wallet_no_balance": False,
        "4.1_wallet_balance": False,
        "4.2_alipay": False,
        "4.3_wechat": False,
        "4.4_wallet_no_balance": False,
        "5.1.1_wallet_balance": False,
        "5.1.2_alipay": False,
        "5.1.3_wechat": False,
        "5.1.4_wallet_no_balance": False,
        "5.2.1_wallet_balance": False,
        "5.2.2_alipay": False,
        "5.2.3_wechat": False,
        "5.2.4_wallet_no_balance": False,
        "5.3.1_wallet_balance": False,
        "5.3.2_alipay": False,
        "5.3.3_wechat": False,
        "5.3.4_wallet_no_balance": False,
        "5.4.1_wallet_balance": False,
        "5.4.2_alipay": False,
        "5.4.3_wechat": False,
        "5.4.4_wallet_no_balance": False
    }

    try:
        # 1. Dynamic Supreme Tests
        print("\n" + "="*60)
        print("1. DYNAMIC SUPREME TESTS")
        print("="*60)
        
        # 1.1 Wallet Balance Payment
        print("\n--- 1.1 Wallet Balance Payment ---")
        test_case1 = create_test_case("1.1 Dynamic Supreme - Wallet Balance", "Test wallet balance payment for Dynamic Supreme package")
        test_results["1.1_wallet_balance"] = test_balance_sufficient(report_dir, test_case1)
        test_report.add_test_case(test_case1)

        # 1.2 Alipay Payment
        print("\n--- 1.2 Alipay Payment ---")
        test_case2 = create_test_case("1.2 Dynamic Supreme - Alipay", "Test Alipay payment flow for Dynamic Supreme package")
        test_results["1.2_alipay"] = test_alipay_payment(report_dir, test_case2)
        test_report.add_test_case(test_case2)

        # 1.3 WeChat Payment
        print("\n--- 1.3 WeChat Payment ---")
        test_case3 = create_test_case("1.3 Dynamic Supreme - WeChat", "Test WeChat payment flow for Dynamic Supreme package")
        test_results["1.3_wechat"] = test_wechat_payment(report_dir, test_case3)
        test_report.add_test_case(test_case3)

        # 2. Static IP Tests
        print("\n" + "="*60)
        print("2. STATIC IP TESTS")
        print("="*60)
        
        # 2.1 Wallet Balance Payment
        print("\n--- 2.1 Wallet Balance Payment ---")
        test_case4 = create_test_case("2.1 Static IP - Wallet Balance", "Test wallet balance payment for Static IP package")
        test_results["2.1_wallet_balance"] = test_balance_sufficient_static(report_dir, test_case4)
        test_report.add_test_case(test_case4)

        # 2.2 Alipay Payment
        print("\n--- 2.2 Alipay Payment ---")
        test_case5 = create_test_case("2.2 Static IP - Alipay", "Test Alipay payment flow for Static IP package")
        test_results["2.2_alipay"] = test_alipay_payment_static(report_dir, test_case5)
        test_report.add_test_case(test_case5)

        # 2.3 WeChat Payment
        print("\n--- 2.3 WeChat Payment ---")
        test_case6 = create_test_case("2.3 Static IP - WeChat", "Test WeChat payment flow for Static IP package")
        test_results["2.3_wechat"] = test_wechat_payment_static(report_dir, test_case6)
        test_report.add_test_case(test_case6)

        # 3. Dynamic Standard Tests
        print("\n" + "="*60)
        print("3. DYNAMIC STANDARD TESTS")
        print("="*60)
        
        # 3.1 Wallet Balance Payment
        print("\n--- 3.1 Wallet Balance Payment ---")
        test_case7 = create_test_case("3.1 Dynamic Standard - Wallet Balance", "Test wallet balance payment for Dynamic Standard package")
        test_results["3.1_wallet_balance"] = test_balance_sufficient_standard(report_dir, test_case7)
        test_report.add_test_case(test_case7)

        # 3.2 Alipay Payment
        print("\n--- 3.2 Alipay Payment ---")
        test_case8 = create_test_case("3.2 Dynamic Standard - Alipay", "Test Alipay payment flow for Dynamic Standard package")
        test_results["3.2_alipay"] = test_alipay_payment_standard(report_dir, test_case8)
        test_report.add_test_case(test_case8)

        # 3.3 WeChat Payment
        print("\n--- 3.3 WeChat Payment ---")
        test_case9 = create_test_case("3.3 Dynamic Standard - WeChat", "Test WeChat payment flow for Dynamic Standard package")
        test_results["3.3_wechat"] = test_wechat_payment_standard(report_dir, test_case9)
        test_report.add_test_case(test_case9)

        # 4. Dynamic Dedicated Tests
        print("\n" + "="*60)
        print("4. DYNAMIC DEDICATED TESTS")
        print("="*60)
        
        # 4.1 Wallet Balance Payment
        print("\n--- 4.1 Wallet Balance Payment ---")
        test_case10 = create_test_case("4.1 Dynamic Dedicated - Wallet Balance", "Test wallet balance payment for Dynamic Dedicated package")
        test_results["4.1_wallet_balance"] = test_balance_sufficient_dedicated(report_dir, test_case10)
        test_report.add_test_case(test_case10)

        # 4.2 Alipay Payment
        print("\n--- 4.2 Alipay Payment ---")
        test_case11 = create_test_case("4.2 Dynamic Dedicated - Alipay", "Test Alipay payment flow for Dynamic Dedicated package")
        test_results["4.2_alipay"] = test_alipay_payment_dedicated(report_dir, test_case11)
        test_report.add_test_case(test_case11)

        # 4.3 WeChat Payment
        print("\n--- 4.3 WeChat Payment ---")
        test_case12 = create_test_case("4.3 Dynamic Dedicated - WeChat", "Test WeChat payment flow for Dynamic Dedicated package")
        test_results["4.3_wechat"] = test_wechat_payment_dedicated(report_dir, test_case12)
        test_report.add_test_case(test_case12)

        # 5. Personal Center Tests
        print("\n" + "="*60)
        print("5. PERSONAL CENTER TESTS")
        print("="*60)
        
        # 5.1 Dynamic Supreme Tests
        print("\n--- 5.1 Dynamic Supreme ---")
        
        # 5.1.1 Wallet Balance Payment
        print("\n--- 5.1.1 Wallet Balance Payment ---")
        test_case13 = create_test_case("5.1.1 Dynamic Supreme - Wallet Balance", "Test wallet balance payment for Dynamic Supreme in Personal Center")
        test_results["5.1.1_wallet_balance"] = test_personal_balance_supreme(report_dir, test_case13)
        test_report.add_test_case(test_case13)

        # 5.1.2 Alipay Payment
        print("\n--- 5.1.2 Alipay Payment ---")
        test_case14 = create_test_case("5.1.2 Dynamic Supreme - Alipay", "Test Alipay payment flow for Dynamic Supreme in Personal Center")
        test_results["5.1.2_alipay"] = test_personal_alipay_supreme(report_dir, test_case14)
        test_report.add_test_case(test_case14)

        # 5.1.3 WeChat Payment
        print("\n--- 5.1.3 WeChat Payment ---")
        test_case15 = create_test_case("5.1.3 Dynamic Supreme - WeChat", "Test WeChat payment flow for Dynamic Supreme in Personal Center")
        test_results["5.1.3_wechat"] = test_personal_wechat_supreme(report_dir, test_case15)
        test_report.add_test_case(test_case15)

        # 5.2 Static IP Tests
        print("\n--- 5.2 Static IP ---")
        
        # 5.2.1 Wallet Balance Payment
        print("\n--- 5.2.1 Wallet Balance Payment ---")
        test_case16 = create_test_case("5.2.1 Static IP - Wallet Balance", "Test wallet balance payment for Static IP in Personal Center")
        test_results["5.2.1_wallet_balance"] = test_personal_balance_static(report_dir, test_case16)
        test_report.add_test_case(test_case16)

        # 5.2.2 Alipay Payment
        print("\n--- 5.2.2 Alipay Payment ---")
        test_case17 = create_test_case("5.2.2 Static IP - Alipay", "Test Alipay payment flow for Static IP in Personal Center")
        test_results["5.2.2_alipay"] = test_personal_alipay_static(report_dir, test_case17)
        test_report.add_test_case(test_case17)

        # 5.2.3 WeChat Payment
        print("\n--- 5.2.3 WeChat Payment ---")
        test_case18 = create_test_case("5.2.3 Static IP - WeChat", "Test WeChat payment flow for Static IP in Personal Center")
        test_results["5.2.3_wechat"] = test_personal_wechat_static(report_dir, test_case18)
        test_report.add_test_case(test_case18)

        # 5.3 Dynamic Standard Tests
        print("\n--- 5.3 Dynamic Standard ---")
        
        # 5.3.1 Wallet Balance Payment
        print("\n--- 5.3.1 Wallet Balance Payment ---")
        test_case19 = create_test_case("5.3.1 Dynamic Standard - Wallet Balance", "Test wallet balance payment for Dynamic Standard in Personal Center")
        test_results["5.3.1_wallet_balance"] = test_personal_balance_standard(report_dir, test_case19)
        test_report.add_test_case(test_case19)

        # 5.3.2 Alipay Payment
        print("\n--- 5.3.2 Alipay Payment ---")
        test_case20 = create_test_case("5.3.2 Dynamic Standard - Alipay", "Test Alipay payment flow for Dynamic Standard in Personal Center")
        test_results["5.3.2_alipay"] = test_personal_alipay_standard(report_dir, test_case20)
        test_report.add_test_case(test_case20)

        # 5.3.3 WeChat Payment
        print("\n--- 5.3.3 WeChat Payment ---")
        test_case21 = create_test_case("5.3.3 Dynamic Standard - WeChat", "Test WeChat payment flow for Dynamic Standard in Personal Center")
        test_results["5.3.3_wechat"] = test_personal_wechat_standard(report_dir, test_case21)
        test_report.add_test_case(test_case21)

        # 5.4 Dynamic Dedicated Tests
        print("\n--- 5.4 Dynamic Dedicated ---")
        
        # 5.4.1 Wallet Balance Payment
        print("\n--- 5.4.1 Wallet Balance Payment ---")
        test_case22 = create_test_case("5.4.1 Dynamic Dedicated - Wallet Balance", "Test wallet balance payment for Dynamic Dedicated in Personal Center")
        test_results["5.4.1_wallet_balance"] = test_personal_balance_dedicated(report_dir, test_case22)
        test_report.add_test_case(test_case22)

        # 5.4.2 Alipay Payment
        print("\n--- 5.4.2 Alipay Payment ---")
        test_case23 = create_test_case("5.4.2 Dynamic Dedicated - Alipay", "Test Alipay payment flow for Dynamic Dedicated in Personal Center")
        test_results["5.4.2_alipay"] = test_personal_alipay_dedicated(report_dir, test_case23)
        test_report.add_test_case(test_case23)

        # 5.4.3 WeChat Payment
        print("\n--- 5.4.3 WeChat Payment ---")
        test_case24 = create_test_case("5.4.3 Dynamic Dedicated - WeChat", "Test WeChat payment flow for Dynamic Dedicated in Personal Center")
        test_results["5.4.3_wechat"] = test_personal_wechat_dedicated(report_dir, test_case24)
        test_report.add_test_case(test_case24)

        # 1.4 Wallet No Balance
        print("\n--- 1.4 Wallet No Balance ---")
        test_case1_4 = create_test_case("1.4 Dynamic Supreme - Wallet No Balance", "Test wallet payment with no balance for Dynamic Supreme package")
        test_results["1.4_wallet_no_balance"] = test_wallet_no_balance_supreme(report_dir, test_case1_4)
        test_report.add_test_case(test_case1_4)

        # 2.4 Wallet No Balance
        print("\n--- 2.4 Wallet No Balance ---")
        test_case2_4 = create_test_case("2.4 Static IP - Wallet No Balance", "Test wallet payment with no balance for Static IP package")
        test_results["2.4_wallet_no_balance"] = test_wallet_no_balance_static(report_dir, test_case2_4)
        test_report.add_test_case(test_case2_4)

        # 3.4 Wallet No Balance
        print("\n--- 3.4 Wallet No Balance ---")
        test_case3_4 = create_test_case("3.4 Dynamic Standard - Wallet No Balance", "Test wallet payment with no balance for Dynamic Standard package")
        test_results["3.4_wallet_no_balance"] = test_wallet_no_balance_standard(report_dir, test_case3_4)
        test_report.add_test_case(test_case3_4)

        # 4.4 Wallet No Balance
        print("\n--- 4.4 Wallet No Balance ---")
        test_case4_4 = create_test_case("4.4 Dynamic Dedicated - Wallet No Balance", "Test wallet payment with no balance for Dynamic Dedicated package")
        test_results["4.4_wallet_no_balance"] = test_wallet_no_balance_dedicated(report_dir, test_case4_4)
        test_report.add_test_case(test_case4_4)

        # 5.1.4 Wallet No Balance
        print("\n--- 5.1.4 Wallet No Balance ---")
        test_case5_1_4 = create_test_case("5.1.4 Dynamic Supreme - Wallet No Balance", "Test wallet payment with no balance for Dynamic Supreme in Personal Center")
        test_results["5.1.4_wallet_no_balance"] = test_personal_wallet_no_balance_supreme(report_dir, test_case5_1_4)
        test_report.add_test_case(test_case5_1_4)

        # 5.2.4 Wallet No Balance
        print("\n--- 5.2.4 Wallet No Balance ---")
        test_case5_2_4 = create_test_case("5.2.4 Static IP - Wallet No Balance", "Test wallet payment with no balance for Static IP in Personal Center")
        test_results["5.2.4_wallet_no_balance"] = test_personal_wallet_no_balance_static(report_dir, test_case5_2_4)
        test_report.add_test_case(test_case5_2_4)

        # 5.3.4 Wallet No Balance
        print("\n--- 5.3.4 Wallet No Balance ---")
        test_case5_3_4 = create_test_case("5.3.4 Dynamic Standard - Wallet No Balance", "Test wallet payment with no balance for Dynamic Standard in Personal Center")
        test_results["5.3.4_wallet_no_balance"] = test_personal_wallet_no_balance_standard(report_dir, test_case5_3_4)
        test_report.add_test_case(test_case5_3_4)

        # 5.4.4 Wallet No Balance
        print("\n--- 5.4.4 Wallet No Balance ---")
        test_case5_4_4 = create_test_case("5.4.4 Dynamic Dedicated - Wallet No Balance", "Test wallet payment with no balance for Dynamic Dedicated in Personal Center")
        test_results["5.4.4_wallet_no_balance"] = test_personal_wallet_no_balance_dedicated(report_dir, test_case5_4_4)
        test_report.add_test_case(test_case5_4_4)

    finally:
        test_report.complete()
        driver.quit()
        
        # Print final results in organized format
        print("\n" + "="*60)
        print("FINAL TEST RESULTS")
        print("="*60)
        
        print("\n1. DYNAMIC SUPREME:")
        print(f"   1.1 Wallet Balance Payment: {'✅ PASSED' if test_results['1.1_wallet_balance'] else '❌ FAILED'}")
        print(f"   1.2 Alipay Payment: {'✅ PASSED' if test_results['1.2_alipay'] else '❌ FAILED'}")
        print(f"   1.3 WeChat Payment: {'✅ PASSED' if test_results['1.3_wechat'] else '❌ FAILED'}")
        print(f"   1.4 Wallet No Balance: {'✅ PASSED' if test_results['1.4_wallet_no_balance'] else '❌ FAILED'}")
        
        print("\n2. STATIC IP:")
        print(f"   2.1 Wallet Balance Payment: {'✅ PASSED' if test_results['2.1_wallet_balance'] else '❌ FAILED'}")
        print(f"   2.2 Alipay Payment: {'✅ PASSED' if test_results['2.2_alipay'] else '❌ FAILED'}")
        print(f"   2.3 WeChat Payment: {'✅ PASSED' if test_results['2.3_wechat'] else '❌ FAILED'}")
        print(f"   2.4 Wallet No Balance: {'✅ PASSED' if test_results['2.4_wallet_no_balance'] else '❌ FAILED'}")
        
        print("\n3. DYNAMIC STANDARD:")
        print(f"   3.1 Wallet Balance Payment: {'✅ PASSED' if test_results['3.1_wallet_balance'] else '❌ FAILED'}")
        print(f"   3.2 Alipay Payment: {'✅ PASSED' if test_results['3.2_alipay'] else '❌ FAILED'}")
        print(f"   3.3 WeChat Payment: {'✅ PASSED' if test_results['3.3_wechat'] else '❌ FAILED'}")
        print(f"   3.4 Wallet No Balance: {'✅ PASSED' if test_results['3.4_wallet_no_balance'] else '❌ FAILED'}")
        
        print("\n4. DYNAMIC DEDICATED:")
        print(f"   4.1 Wallet Balance Payment: {'✅ PASSED' if test_results['4.1_wallet_balance'] else '❌ FAILED'}")
        print(f"   4.2 Alipay Payment: {'✅ PASSED' if test_results['4.2_alipay'] else '❌ FAILED'}")
        print(f"   4.3 WeChat Payment: {'✅ PASSED' if test_results['4.3_wechat'] else '❌ FAILED'}")
        print(f"   4.4 Wallet No Balance: {'✅ PASSED' if test_results['4.4_wallet_no_balance'] else '❌ FAILED'}")

        print("\n5. PERSONAL CENTER:")
        print("   5.1 Dynamic Supreme:")
        print(f"      5.1.1 Wallet Balance Payment: {'✅ PASSED' if test_results['5.1.1_wallet_balance'] else '❌ FAILED'}")
        print(f"      5.1.2 Alipay Payment: {'✅ PASSED' if test_results['5.1.2_alipay'] else '❌ FAILED'}")
        print(f"      5.1.3 WeChat Payment: {'✅ PASSED' if test_results['5.1.3_wechat'] else '❌ FAILED'}")
        print(f"      5.1.4 Wallet No Balance: {'✅ PASSED' if test_results['5.1.4_wallet_no_balance'] else '❌ FAILED'}")
        
        print("   5.2 Static IP:")
        print(f"      5.2.1 Wallet Balance Payment: {'✅ PASSED' if test_results['5.2.1_wallet_balance'] else '❌ FAILED'}")
        print(f"      5.2.2 Alipay Payment: {'✅ PASSED' if test_results['5.2.2_alipay'] else '❌ FAILED'}")
        print(f"      5.2.3 WeChat Payment: {'✅ PASSED' if test_results['5.2.3_wechat'] else '❌ FAILED'}")
        print(f"      5.2.4 Wallet No Balance: {'✅ PASSED' if test_results['5.2.4_wallet_no_balance'] else '❌ FAILED'}")
        
        print("   5.3 Dynamic Standard:")
        print(f"      5.3.1 Wallet Balance Payment: {'✅ PASSED' if test_results['5.3.1_wallet_balance'] else '❌ FAILED'}")
        print(f"      5.3.2 Alipay Payment: {'✅ PASSED' if test_results['5.3.2_alipay'] else '❌ FAILED'}")
        print(f"      5.3.3 WeChat Payment: {'✅ PASSED' if test_results['5.3.3_wechat'] else '❌ FAILED'}")
        print(f"      5.3.4 Wallet No Balance: {'✅ PASSED' if test_results['5.3.4_wallet_no_balance'] else '❌ FAILED'}")
        
        print("   5.4 Dynamic Dedicated:")
        print(f"      5.4.1 Wallet Balance Payment: {'✅ PASSED' if test_results['5.4.1_wallet_balance'] else '❌ FAILED'}")
        print(f"      5.4.2 Alipay Payment: {'✅ PASSED' if test_results['5.4.2_alipay'] else '❌ FAILED'}")
        print(f"      5.4.3 WeChat Payment: {'✅ PASSED' if test_results['5.4.3_wechat'] else '❌ FAILED'}")
        print(f"      5.4.4 Wallet No Balance: {'✅ PASSED' if test_results['5.4.4_wallet_no_balance'] else '❌ FAILED'}")
        
        # Calculate summary
        passed_count = sum(1 for result in test_results.values() if result)
        total_count = len(test_results)
        
        print(f"\nSUMMARY: {passed_count}/{total_count} tests passed")
        
        report_file = test_report.generate_html_report()
        print(f"\nDetailed report generated: {report_file}")

if __name__ == "__main__":
    main() 