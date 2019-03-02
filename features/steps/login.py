from behave import given, when, then
from test.factories.accounts import UserFactory


@given('an anonymous user')
def step_impl(context):
    from django.contrib.auth.models import User

    u = UserFactory(username='foo', email='foo@example.com')
    u.set_password('bar')

    u.save()


@when('I submit a valid login page')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/login/')

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    br.find_element_by_name('username').send_keys('foo')
    br.find_element_by_name('password').send_keys('bar')
    br.find_element_by_name('submit').click()


@then('I am redirected to the homepage')
def step_impl(context):
    br = context.browser

    assert br.current_url.endswitch('/homepage/')


@when('I submit an invalid login page')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/login/')

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    br.find_element_by_name('username').send_keys('foo')
    br.find_element_by_name('password').send_keys('bar-is-invalid')
    br.find_element_by_name('submit').click()


@then('I am redirected to the login page')
def step_impl(context):
    br = context.browser

    assert br.current_url.endswitch('/login/')
