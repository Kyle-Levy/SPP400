from behave import given, when, then
from test.factories.accounts import UserFactory
from django.contrib.auth import authenticate


@given('a successful login')
def step_impl(context):
    u = UserFactory(username='foo', email='foo@example.com')
    u.set_password('bar')

    u.save()

    br = context.browser
    br.get(context.base_url + '/login/')

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    br.find_element_by_name('username').send_keys('foo')
    br.find_element_by_name('password').send_keys('bar')
    br.find_element_by_name('submit').click()

    br = context.browser

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    user = authenticate(username='foo', password='bar')
    user.profile.key = 94759374
    user.save()

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()
    br.find_element_by_name('key').send_keys(94759374)
    br.find_element_by_name('submit').click()

    br = context.browser

    assert br.current_url.endswith('/homepage/')


@when('I click on the procedures tab')
def step_impl(context):
    br = context.browser

    br.find_element_by_name('procedures').click()


@then('I am redirected to the procedures page')
def step_impl(context):
    br = context.browser

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    assert br.current_url.endswith('/procedures/')


@when('I click on the Add New Procedure button')
def step_impl(context):
    br = context.browser

    br.find_element_by_name('new-procedure-button').click()


@then('I am redirected to the procedure form page')
def step_impl(context):
    br = context.browser

    assert br.current_url.endswith('/procedures/create/')
