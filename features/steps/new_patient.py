from behave import given, when, then
from test.factories.accounts import UserFactory
from django.contrib.auth import authenticate


@when('I click on the patients tab')
def step_impl(context):
    br = context.browser
    br.find_element_by_name('patients').click()


@then('I am redirected to the patients page')
def step_impl(context):
    br = context.browser
    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()
    assert br.current_url.endswith('/patients/')


@when('I click on add a new patient')
def step_impl(context):
    br = context.browser
    br.find_element_by_name('new-patient-button').click()


@then('I am redirected to the new patients page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/patients/create/')


@when('I submit a valid new patient')
def step_impl(context):
    br = context.browser
    br.find_element_by_name('firstName').send_keys('Harry')
    br.find_element_by_name('lastName').send_keys('Potter')
    br.find_element_by_name('recordNumber').send_keys('4')
    br.find_element_by_name('birthDate').send_keys('07/31/1980')
    br.find_element_by_name('referringPhysician').send_keys('Madam Pomfrey')
    br.find_element_by_name('dateOfReferral').send_keys('01/01/1992')
    br.find_element_by_name('submit').click()


@then('I am redirected to the patients landing page')
def step_impl(context):
    br = context.browser
    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()
    assert br.current_url.endswith('/patients/')
