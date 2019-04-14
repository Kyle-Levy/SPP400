from behave import given, when, then
from test.factories.accounts import UserFactory

@given('I am in the homepage')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/homepage/')

@when('I click the patients tab')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/homepage/')
    br.switch_to_frame("sidebar")
    br.find_element_by_id("patients").click()

@then('I am directed to the patients page')
def step_impl(context):
    br = context.browser
    assert br.curent_url.endswith('/patients/')

@when('I click the procedures tab')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/homepage/')
    br.find_element_by_id('procedures').click()

@then('I am directed to the procedures page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/procedures/')

@when('I click the roadmaps tab')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/homepage/')
    br.find_element_by_id('roadmaps').click()

@then('I am directed to the roadmaps page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/roadmaps/')

@when('I click the profile tab')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/homepage/')
    br.find_element_by_id('profile').click()

@then('The dropdown opens')
def step_impl(context):
    br = context.browser
    assert br.find_element_by_id('profileSubmenu').is_displayed()

@when('I click logout')
def step_impl(context):
    br = context.browser
    br.find_element_by_link_text('Logout').click()

@then('I am logged out')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/logout/')