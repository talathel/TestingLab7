import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Firefox()


def log_in(browser):
    login = browser.find_element(By.ID, 'id_username')
    login.send_keys('test_user' + Keys.TAB + 'AEAKS123')
    browser.find_element(By.XPATH, r'/html/body/form/button').click()


def test_main_page():
    browser.delete_all_cookies()
    browser.get('https://aekas.newacidrain.repl.co')
    assert "АЕКАС" in browser.title
    try:
        el = browser.find_element(By.ID, 'btn-text')
        assert 'Начнем!' in el.text
    except NoSuchElementException:
        assert False


def test_unauthorized_task_redirect_after_login():
    browser.delete_all_cookies()
    browser.get('https://aekas.newacidrain.repl.co/exercises/?page=1')
    assert browser.current_url.startswith('https://aekas.newacidrain.repl.co/login')
    log_in(browser)
    assert browser.current_url == r'https://aekas.newacidrain.repl.co/exercises/?page=1'


def test_solve_task_incorrectly():
    test_unauthorized_task_redirect_after_login()
    if 'page-num' != browser.find_element(By.ID, 'page-nums').get_attribute('class'):
        print('reseting progress')
        browser.get(r'https://aekas.newacidrain.repl.co/reset_progress')
    assert browser.find_element(By.CLASS_NAME, 'title_ex').find_element(By.TAG_NAME, 'h1').text == 'Тестовая задача 1'
    assert browser.find_element(By.CLASS_NAME, 'text_ex').find_element(By.TAG_NAME,
                                                                       'h1').text == 'Напишите функцию f, которая на вход получает число х, а возвращает х+1'
    code_area = browser.find_element(By.ID, 'code-textarea')
    code_area.send_keys('''
def f(x):
    return x+2    
    ''')
    browser.find_element(By.ID, 'code-btn').click()
    assert browser.find_element(By.ID, 'result').text == "Неправильно"
    assert 'page-num-fail' in browser.find_element(value='links-1').find_element(By.TAG_NAME, 'li').get_attribute(
        'class')


def test_solve_task_incorrect_func_name():
    browser.delete_all_cookies()
    test_unauthorized_task_redirect_after_login()
    if 'page-num' != browser.find_element(By.ID, 'page-nums').get_attribute('class'):
        print('reseting progress')
        browser.get(r'https://aekas.newacidrain.repl.co/reset_progress')
    assert browser.find_element(By.CLASS_NAME, 'title_ex').find_element(By.TAG_NAME, 'h1').text == 'Тестовая задача 1'
    assert browser.find_element(By.CLASS_NAME, 'text_ex').find_element(By.TAG_NAME,
                                                                       'h1').text == 'Напишите функцию f, которая на вход получает число х, а возвращает х+1'
    code_area = browser.find_element(By.ID, 'code-textarea')
    code_area.send_keys('''
def y(x):
    return x+1    
    ''')
    browser.find_element(By.ID, 'code-btn').click()
    assert browser.find_element(By.ID, 'result').text == "Неправильно"
    assert 'page-num-fail' in browser.find_element(value='links-1').find_element(By.TAG_NAME, 'li').get_attribute(
        'class')


def test_solve_task_no_func_args():
    browser.delete_all_cookies()
    test_unauthorized_task_redirect_after_login()
    if 'page-num' != browser.find_element(By.ID, 'page-nums').get_attribute('class'):
        print('reseting progress')
        browser.get(r'https://aekas.newacidrain.repl.co/reset_progress')
    assert browser.find_element(By.CLASS_NAME, 'title_ex').find_element(By.TAG_NAME, 'h1').text == 'Тестовая задача 1'
    assert browser.find_element(By.CLASS_NAME, 'text_ex').find_element(By.TAG_NAME,
                                                                       'h1').text == 'Напишите функцию f, которая на вход получает число х, а возвращает х+1'
    code_area = browser.find_element(By.ID, 'code-textarea')
    code_area.send_keys('''
def f():
    x=1
    return x+1    
    ''')
    browser.find_element(By.ID, 'code-btn').click()
    assert browser.find_element(By.ID, 'result').text == "Неправильно"
    assert 'page-num-fail' in browser.find_element(value='links-1').find_element(By.TAG_NAME, 'li').get_attribute(
        'class')


def test_solve_task_syntax_err():
    browser.delete_all_cookies()
    test_unauthorized_task_redirect_after_login()
    if 'page-num' != browser.find_element(By.ID, 'page-nums').get_attribute('class'):
        print('reseting progress')
        browser.get(r'https://aekas.newacidrain.repl.co/reset_progress')
    assert browser.find_element(By.CLASS_NAME, 'title_ex').find_element(By.TAG_NAME, 'h1').text == 'Тестовая задача 1'
    assert browser.find_element(By.CLASS_NAME, 'text_ex').find_element(By.TAG_NAME,
                                                                       'h1').text == 'Напишите функцию f, которая на вход получает число х, а возвращает х+1'
    code_area = browser.find_element(By.ID, 'code-textarea')
    code_area.send_keys('''
def f():
x=1
    return x+1    
    ''')
    browser.find_element(By.ID, 'code-btn').click()
    assert browser.find_element(By.ID, 'result').text == "Неправильно"
    assert 'page-num-fail' in browser.find_element(value='links-1').find_element(By.TAG_NAME, 'li').get_attribute(
        'class')


def test_solve_task_correct():
    browser.delete_all_cookies()
    test_unauthorized_task_redirect_after_login()
    if 'page-num' != browser.find_element(By.ID, 'page-nums').get_attribute('class'):
        print('reseting progress')
        browser.get(r'https://aekas.newacidrain.repl.co/reset_progress')
    assert browser.find_element(By.CLASS_NAME, 'title_ex').find_element(By.TAG_NAME, 'h1').text == 'Тестовая задача 1'
    assert browser.find_element(By.CLASS_NAME, 'text_ex').find_element(By.TAG_NAME,
                                                                       'h1').text == 'Напишите функцию f, которая на вход получает число х, а возвращает х+1'
    code_area = browser.find_element(By.ID, 'code-textarea')
    code_area.send_keys('''
def f(x):
    return x+1    
        ''')
    browser.find_element(By.ID, 'code-btn').click()
    assert browser.find_element(By.ID, 'result').text == "Правильно"
    assert 'page-num-success' in browser.find_element(value='links-1').find_element(By.TAG_NAME, 'li').get_attribute(
        'class')


def test_register_existing_user():
    browser.delete_all_cookies()
    browser.get(r'https://aekas.newacidrain.repl.co/register')
    browser.find_element(By.ID, 'id_username').send_keys(
        'test_user' + Keys.TAB + 'ungabunga123' + Keys.TAB + 'ungabunga123')
    browser.find_element(By.XPATH, '/html/body/form/button').click()
    assert browser.current_url == r'https://aekas.newacidrain.repl.co/register'
    assert browser.find_element(By.XPATH, '/html/body/form/p[2]').text == 'A user with that username already exists.'


def test_password_doesnt_match():
    browser.delete_all_cookies()
    browser.get(r'https://aekas.newacidrain.repl.co/register')
    browser.find_element(By.ID, 'id_username').send_keys(
        'test_user123123123' + Keys.TAB + 'ungabunga123' + Keys.TAB + 'ungabunga1234')
    browser.find_element(By.XPATH, '/html/body/form/button').click()
    assert browser.current_url == r'https://aekas.newacidrain.repl.co/register'
    assert browser.find_element(By.XPATH, '/html/body/form/p[4]').text == 'The two password fields didn’t match.'


def test_authorized_user_register():
    browser.delete_all_cookies()
    browser.get("https://aekas.newacidrain.repl.co/login")
    log_in(browser)
    browser.get('https://aekas.newacidrain.repl.co/register')
    assert browser.current_url == 'https://aekas.newacidrain.repl.co/'


def test_button_main_page():
    browser.delete_all_cookies()
    URL = "https://AEKAS.newacidrain.repl.co"
    browser.get(url=URL)
    time.sleep(2)
    browser.find_element(By.CLASS_NAME, value="btn").click()
    time.sleep(2)
    test = browser.find_element(By.XPATH, '/html/body/form/p[1]/label').text
    assert test == "Username:"


def test_login_and_invalid_login():
    URL = "https://aekas.newacidrain.repl.co/login"
    browser.get(url=URL)
    browser.find_element(By.XPATH, value="//*[@id='id_username']").send_keys('uhidsaj')
    browser.find_element(By.XPATH, value="//*[@id='id_password']").send_keys('hnfkjlas')
    browser.find_element(By.XPATH, value="/html/body/form/button").click()
    time.sleep(2)
    test = browser.find_element(By.XPATH, value="/html/body/form/ul/li").text
    assert test
    time.sleep(2)
    browser.find_element(By.XPATH, value="//*[@id='id_username']").clear()
    browser.find_element(By.XPATH, value="//*[@id='id_username']").send_keys('admin')
    browser.find_element(By.XPATH, value="//*[@id='id_password']").send_keys('123')
    time.sleep(2)
    browser.find_element(By.XPATH, value="/html/body/form/button").click()
    time.sleep(2)
    test = browser.find_element(By.CLASS_NAME, value="description").text
    assert test == "Образовательная платформа АЕАКС"


def test_ex_title():
    URL = "https://aekas.newacidrain.repl.co/exercises/?page=1"
    browser.get(url=URL)
    time.sleep(2)
    test = browser.find_element(By.XPATH, "//*[@id='container']/label[1]/h1").text
    assert test == "Тестовая задача 1"


def test_ex_text():
    URL = "https://aekas.newacidrain.repl.co/exercises/?page=1"
    browser.get(url=URL)
    time.sleep(2)
    test = browser.find_element(By.XPATH, "//*[@id='container']/label[2]/h1").text
    assert test == "Напишите функцию f, которая на вход получает число х, а возвращает х+1"


def test_text_field():
    URL = "https://aekas.newacidrain.repl.co/exercises/?page=1"
    browser.get(url=URL)
    # browser.find_element(By.XPATH, value="//*[@id='id_username']").send_keys('admin')
    # browser.find_element(By.XPATH, value="//*[@id='id_password']").send_keys('123')
    # time.sleep(2)
    # browser.find_element(By.XPATH, value="/html/body/form/button").click()
    time.sleep(2)
    test = browser.find_element(By.XPATH, '//*[@id="code-textarea"]')
    time.sleep(2)
    assert test


def test_ex_btn():
    URL = "https://aekas.newacidrain.repl.co/exercises/?page=1"
    browser.get(url=URL)
    # browser.find_element(By.XPATH, value="//*[@id='id_username']").send_keys('admin')
    # browser.find_element(By.XPATH, value="//*[@id='id_password']").send_keys('123')
    # browser.find_element(By.XPATH, value="/html/body/form/button").click()
    time.sleep(2)
    browser.find_element(By.ID, value='links-2').click()
    time.sleep(2)
    test = browser.find_element(By.XPATH, value='//*[@id="container"]/label[1]/h1').text
    assert test


def test_log_out():
    URL = "https://aekas.newacidrain.repl.co/exercises/?page=1"
    browser.get(url=URL)
    # browser.find_element(By.XPATH, value="//*[@id='id_username']").send_keys('admin')
    # browser.find_element(By.XPATH, value="//*[@id='id_password']").send_keys('123')
    # browser.find_element(By.XPATH, value="/html/body/form/button").click()
    time.sleep(2)
    browser.find_element(By.XPATH, value="/html/body/header/div/a[3]").click()
    test = browser.find_element(By.XPATH, value="/html/body/header/div/a[3]").text
    time.sleep(2)
    assert test != "Log out"


def test_title_btn():
    URL = "https://aekas.newacidrain.repl.co/login?next=/exercises/%3Fpage%3D1"
    browser.get(url=URL)
    time.sleep(2)
    # browser.find_element(By.XPATH, value="//*[@id='id_username']").send_keys('admin')
    # browser.find_element(By.XPATH, value="//*[@id='id_password']").send_keys('123')
    # browser.find_element(By.XPATH, value="/html/body/form/button").click()
    # time.sleep(2)
    browser.find_element(By.ID, value="title-link").click()
    time.sleep(2)
    test = browser.find_element(By.XPATH, value='//*[@id="description"]').text
    assert test == "Образовательная платформа АЕАКС"


def test_reg():
    browser.delete_all_cookies()
    URL = "https://aekas.newacidrain.repl.co/register"
    browser.get(url=URL)
    browser.find_element(By.NAME, value="username").send_keys('yaga123456')
    time.sleep(2)
    browser.find_element(By.NAME, value="password1").send_keys('newpassword1')
    browser.find_element(By.NAME, value="password2").send_keys('newpassword1')
    time.sleep(2)
    browser.find_element(By.XPATH, value="/html/body/form/button").click()
    time.sleep(2)
    test = browser.find_element(By.XPATH, value='/html/body/header/div/a[3]').text
    assert test == "Log out"