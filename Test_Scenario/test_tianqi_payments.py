# ===== Imports =====
from test_template import WebsiteTestTemplate
from test_config import TIANQI_CONFIG
from test_reports.test_report import TestReport, create_test_case
import pytest

class TestTianQiPayments:
    def setup_method(self):
        """Set up test environment before each test"""
        self.test_template = WebsiteTestTemplate(TIANQI_CONFIG)
        self.test_template.setup()
        self.report = TestReport()
        
    def teardown_method(self):
        """Clean up after each test"""
        self.test_template.teardown()
        
    def test_buy_package_with_balance(self):
        """Test buying a package using account balance"""
        test_case = create_test_case(
            "Buy Package with Balance",
            "Test purchasing a dynamic supreme package using account balance"
        )
        
        try:
            # Login with account that has balance
            self.test_template.login(test_case, TIANQI_CONFIG['credentials']['with_balance'])
            
            # Select package
            self.test_template.select_item(
                test_case,
                TIANQI_CONFIG['selectors']['packages']['dynamic_supreme'],
                "dynamic supreme package"
            )
            
            # Complete payment using balance
            self.test_template.complete_payment(test_case, 'balance')
            
            # Verify success
            self.test_template.verify_success(test_case)
            
        except Exception as e:
            test_case.fail(str(e))
            raise
        finally:
            self.report.add_test_case(test_case)
            
    def test_buy_package_insufficient_balance(self):
        """Test buying a package with insufficient balance"""
        test_case = create_test_case(
            "Buy Package with Insufficient Balance",
            "Test purchasing a package with an account that has insufficient balance"
        )
        
        try:
            # Login with account that has no balance
            self.test_template.login(test_case, TIANQI_CONFIG['credentials']['without_balance'])
            
            # Select package
            self.test_template.select_item(
                test_case,
                TIANQI_CONFIG['selectors']['packages']['dynamic_supreme'],
                "dynamic supreme package"
            )
            
            # Complete payment using balance
            self.test_template.complete_payment(test_case, 'balance')
            
            # Verify error message
            self.test_template.handle_error(test_case, "余额不足")
            
        except Exception as e:
            test_case.fail(str(e))
            raise
        finally:
            self.report.add_test_case(test_case)
            
    def test_buy_package_with_alipay(self):
        """Test buying a package using Alipay"""
        test_case = create_test_case(
            "Buy Package with Alipay",
            "Test purchasing a static IP package using Alipay"
        )
        
        try:
            # Login with any account
            self.test_template.login(test_case, TIANQI_CONFIG['credentials']['without_balance'])
            
            # Select package
            self.test_template.select_item(
                test_case,
                TIANQI_CONFIG['selectors']['packages']['static_ip'],
                "static IP package"
            )
            
            # Complete payment using Alipay
            self.test_template.complete_payment(test_case, 'alipay')
            
            # Verify success
            self.test_template.verify_success(test_case)
            
        except Exception as e:
            test_case.fail(str(e))
            raise
        finally:
            self.report.add_test_case(test_case)
