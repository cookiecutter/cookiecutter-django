from behave import *

use_step_matcher("re")


@given("we have behave installed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given we have behave installed')


@when("we implement a test")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When we implement a test')


@then("behave will test it for us!")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then behave will test it for us!')
