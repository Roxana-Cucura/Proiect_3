import unittest
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, wait


class TestLogin(unittest.TestCase):
    H2_TEXT = (By.XPATH, '//h2[text()="Login Page"]')
    LOGIN_BTN = (By.XPATH, '//button[@type = "submit"]')
    ELEMENT_LINK = (By.XPATH, '//*[@href="http://elementalselenium.com/"]')
    ERROR_MESSAGES = (By.XPATH, '//div[@class="flash error"]')
    CLOSE_ERROR_BTN = (By.XPATH, '//*[@href="#"]')

    chrome = None

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.ELEMENT_ATRIBUTE = None

    def setUp(self):
        s = Service(ChromeDriverManager().install())
        self.chrome = webdriver.Chrome(service=s)
        self.chrome.maximize_window()
        self.chrome.get('https://the-internet.herokuapp.com/login')

    def tearDown(self):
        self.chrome.quit()

    # Test1: Verificati ca noul url e corect
    def test_url(self) -> None:
        actual = self.chrome.current_url
        expected = 'https://the-internet.herokuapp.com/login'
        self.assertEqual(expected, actual, 'URL incorrect')

    # Test2: Verificati ca page title e corect
    def test_page_title(self):
        actual = self.chrome.title
        expected = 'Login Page'
        self.assertEqual(actual, expected, 'page title incorrect')

    # Test3: Verificati textul de pe elementul xpath=//h2 e corect
    def test_h2_correct_text(self):
        actual = self.chrome.find_element(*self.H2_TEXT).text
        expected = 'Login Page'
        self.assertEqual(actual, expected, 'Text incorrect')

    # Test4: Verificati ca butonul de login este displayed
    def test_login_btn_visible(self):
        element = self.chrome.find_element(*self.LOGIN_BTN)
        self.assertTrue(element.is_displayed(), 'Button not visible')

    # Test5: Verificati ca atributul href al linkului ‘Elemental Selenium’ e corect
    def test_correct_atribute_element(self):
        actual = self.chrome.find_element(*self.ELEMENT_ATRIBUTE).get_attribute('href')
        expected = 'http://elementalselenium.com/'
        self.assertEqual(actual, expected, 'Atribute incorrect')

    # Test6: Lasati goale user si pass. Click login. Verifica ca eroarea e displayed
    def test_displayed_error(self):
        self.chrome.find_element(*self.LOGIN_BTN).click()
        error_messages = self.chrome.find_elements(*self.ERROR_MESSAGES)
        self.assertEqual(len(error_messages) == 0, 'No flash error found !')

    # Test7: Completeaza cu user si pass invalide. Click login. Verifica ca mesajul de pe eroare e corect
    def test_invalid_credentiales_error(self):
        input_user = self.chrome.find_element(By.XPATH, '//*[@name="username"]')
        input_user.send_keys('Roxana')
        input_pw = self.chrome.find_element(By.XPATH, '//*[@name="password"]')
        input_pw.send_keys('Ab235C')

        sleep(2)

        self.chrome.find_element(*self.LOGIN_BTN).click()

        sleep(2)

        actual = self.chrome.find_element(By.XPATH, '//*[@id="flash"]').text
        expected = 'Your username is invalid!'
        self.assertTrue(expected in actual, 'Error message text is incorrect')

    # Test8: Lasati goale user si pass.Click login.Apasa x la eroare. Verifica ca eroarea a disparut
    def test_error_disappeared(self):
        self.chrome.find_element(*self.LOGIN_BTN).click()
        error_messages = self.chrome.find_elements(*self.ERROR_MESSAGES)
        self.chrome.find_element(*self.CLOSE_ERROR_BTN).click()
        self.assertEqual(len(error_messages), 0, 0)

        sleep(2)

    #Test9: Ia ca o lista toate //label. Verifica textul ca textul de pe ele sa fie cel asteptat (Username si
    #Password). Aici e ok sa avem 2 asserturi
    def test_label_text(self):
            actual = self.chrome.find_elements(By.XPATH, '//*[@id="login"]/div[2]/div/label////*[@id="login"]/div[1]/div/label')
            expected = 'Username', 'Password'
            self.assertEqal(actual, expected, 'Eroare')

    '''Test10: Completeaza cu user si pass valide
    Click login
    Verifica ca noul url CONTINE /secure
    Foloseste un explicit wait pentru elementul cu clasa ’flash succes’
    Verifica ca elementul cu clasa=’flash succes’ este displayed
    Verifica ca mesajul de pe acest element CONTINE textul ‘secure area!’
 '''
    def test_valid_login(self):
        self.chrome.find_element(By.XPATH, '//*[@name="username"]').send_keys('tomsmith')
        self.chrome.find_element(By.XPATH, '//*[@name="password"]').send_keys('SuperSecretPassword!')
        self.chrome.find_element(By.XPATH, '//*[@type="submit"]').click()
        WebDriverWait(self.chrome, 2).until(EC.url_contains('/secure'))
        self.chrome.find_element(By.XPATH, '//*[@id="flash"]')
        WebDriverWait(self.chrome, 2).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="flash success"]')))
        actual = self.chrome.find_element(By.XPATH, '//*[@id="flash"]').text
        expected = 'secure area'
        self.assertTrue(expected in actual, 'Text message text is incorrect')


    '''Test11:
    Completeaza cu user si pass valide
    Click login
    Click logout
    Verifica ca ai ajuns pe https://the-internet.herokuapp.com/login
    '''

    def test_valid_login2(self):
        self.chrome.find_element(By.XPATH, '//*[@name="username"]').send_keys('tomsmith')
        self.chrome.find_element(By.XPATH, '//*[@name="password"]').send_keys('SuperSecretPassword!')
        self.chrome.find_element(By.XPATH, '//*[@type="submit"]').click()
        self.chrome.find_element(By.XPATH, '//*[@href="/logout"]').click()
        actual = self.chrome.current_url
        expected = 'https://the-internet.herokuapp.com/login'
        self.assertEqual(expected, actual, 'URL incorrect')
