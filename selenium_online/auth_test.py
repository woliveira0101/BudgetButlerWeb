from SeleniumTest import SeleniumTestClass
from SeleniumTest import fill_element
from SeleniumTest import login
from SeleniumTest import generate_unique_name
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin(SeleniumTestClass):
    def test_login_page(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/login.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)

    def test_login_admin(self, get_driver, close_driver):
        driver = get_driver()

        login(driver, 'admin@admin.de', 'admin')
        driver.get('http://localhost/logout.php')
        assert driver.title == 'BudgetButlerWeb - Logout'
        close_driver(driver)


    def test_add_user(self, get_driver, close_driver):
        driver = get_driver()

        new_user_id = generate_unique_name()
        new_user_email = new_user_id + '@s.de'
        passwd = 'funnypass'

        login(driver, 'admin@admin.de', 'admin')

        driver.get('http://localhost/dashboard.php')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        fill_element(driver, 'username', new_user_id)
        fill_element(driver, 'email', new_user_email)
        fill_element(driver, 'password', passwd)
        driver.find_element_by_id('btn_add_user').send_keys(Keys.ENTER)

        driver.get('http://localhost/logout.php')

        login(driver, new_user_email, passwd)
        assert driver.title == 'BudgetButlerWeb - Dashboard'
        driver.get('http://localhost/logout.php')
        assert driver.title == 'BudgetButlerWeb - Logout'
        close_driver(driver)

class TestAutoRedirectWhenNotLoggedIn(SeleniumTestClass):

    def test_dashboard(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/logout.php')

        driver.get('http://localhost/dashboard.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)


    def test_deletegemeinsam(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/logout.php')

        driver.get('http://localhost/deletegemeinsam.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)


    def test_deleteitems(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/logout.php')

        driver.get('http://localhost/deleteitems.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)


    def test_getabrechnung(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/logout.php')

        driver.get('http://localhost/getabrechnung.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)


    def test_getgemeinsam(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/logout.php')

        driver.get('http://localhost/getgemeinsam.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)


    def test_getusername(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/logout.php')

        driver.get('http://localhost/getusername.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)


    def test_setkategorien(self, get_driver, close_driver):
        driver = get_driver()
        driver.get('http://localhost/logout.phpp')

        driver.get('http://localhost/setkategorien.php')
        assert driver.title == 'BudgetButlerWeb - Login'
        close_driver(driver)

