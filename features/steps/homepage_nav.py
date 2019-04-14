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
    br.find_element_by_id('patients').click()

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
    Then I am directed to the roadmaps page

    When I click the profile tab
    Then The dropdown opens
    When I click logout
    Then I am logged out