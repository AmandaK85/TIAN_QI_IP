# Sample configuration for Tian Qi IP website tests
TIANQI_CONFIG = {
    'base_url': 'https://test-ip-tianqi.cd.xiaoxigroup.net',
    'credentials': {
        'with_balance': {
            'username': '15332595364',
            'password': 'Test@123'
        },
        'without_balance': {
            'username': '15658873355',
            'password': 'Test@123'
        }
    },
    'selectors': {
        'login': {
            'username_input': [
                "//*[@id='__BVID__23']",
                "//input[@placeholder='请输入手机号' or @placeholder='手机号']",
                "//input[@type='tel' or @type='text'][contains(@class, 'form-control')]",
                "//input[contains(@name, 'phone') or contains(@name, 'mobile')]"
            ],
            'password_input': [
                "//*[@id='__BVID__24']",
                "//input[@placeholder='请输入密码' or @placeholder='密码']",
                "//input[@type='password']",
                "//input[contains(@name, 'password') or contains(@name, 'pwd')]"
            ],
            'login_button': [
                "//button[contains(text(), '登录')]",
                "//button[@type='submit']",
                "//input[@type='submit']",
                "//button[contains(@class, 'btn-primary') or contains(@class, 'login')]"
            ]
        },
        'packages': {
            'dynamic_supreme': [
                "//div[contains(text(), '天启动态尊享')]",
                "//div[contains(@class, 'package-card') and contains(text(), '动态尊享')]",
                "//div[@data-package='supreme' or @data-package='dynamic-supreme']"
            ],
            'static_ip': [
                "//div[contains(text(), '静态IP-天启')]",
                "//div[contains(@class, 'package-card') and contains(text(), '静态IP')]",
                "//div[@data-package='static' or @data-package='static-ip']"
            ]
        },
        'payment': {
            'balance': [
                "//div[contains(text(), '余额')]",
                "//div[@data-payment='balance' or @data-payment='wallet']",
                "//div[contains(@class, 'payment-option') and contains(text(), '余额')]"
            ],
            'alipay': [
                "//div[contains(text(), '支付宝')]",
                "//div[@data-payment='alipay']",
                "//div[contains(@class, 'payment-option') and contains(text(), '支付宝')]"
            ]
        },
        'payment_confirmation': {
            'alipay': [
                {
                    'description': 'email input',
                    'selectors': ["//*[@id='J_tLoginId']"],
                    'input': 'test@example.com'
                },
                {
                    'description': 'password input',
                    'selectors': ["//*[@id='payPasswd_rsainput']"],
                    'input': 'test123'
                },
                {
                    'description': 'next button',
                    'selectors': ["//*[@id='J_newBtn']/span"],
                    'wait_time': 2
                }
            ]
        },
        'buttons': {
            'buy_now': [
                "//div[contains(text(), '立即购买')]",
                "//button[contains(text(), '立即购买')]",
                "//div[@data-action='buy-now' or @data-action='purchase']"
            ],
            'pay_now': [
                "//div[contains(text(), '立即支付')]",
                "//button[contains(text(), '立即支付')]",
                "//div[@data-action='pay-now' or @data-action='payment']"
            ]
        },
        'status': {
            'success_message': [
                "//div[contains(text(), '套餐购买成功')]",
                "//div[contains(text(), '创建成功')]",
                "//div[contains(@class, 'success') and contains(text(), '成功')]"
            ],
            'error_message': [
                "//div[contains(text(), '账户余额不足')]",
                "//div[contains(text(), '余额不足')]",
                "//div[contains(@class, 'error') and contains(text(), '不足')]"
            ]
        }
    }
}
