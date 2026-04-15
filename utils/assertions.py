import allure
from pprint import pformat

def assert_equal(actual, expected, name=""):
    with allure.step(f"ASSERT EQUAL: {name}"):

        allure.attach(
            f"TYPE ACTUAL: {type(actual)}\n{pformat(actual)}",
            "ACTUAL",
            allure.attachment_type.TEXT
        )

        allure.attach(
            f"TYPE EXPECTED: {type(expected)}\n{pformat(expected)}",
            "EXPECTED",
            allure.attachment_type.TEXT
        )

        if actual != expected:
            allure.attach(
                "VALUES ARE DIFFERENT ❌",
                "DIFF STATUS",
                allure.attachment_type.TEXT
            )

        assert actual == expected

def assert_in(member, container, name=""):
    with allure.step(f"ASSERT IN: {name}"):

        allure.attach(
            f"MEMBER:\n{pformat(member)}",
            "LOOKING FOR",
            allure.attachment_type.TEXT
        )

        allure.attach(
            f"CONTAINER TYPE: {type(container)}\n{pformat(container)}",
            "CONTAINER",
            allure.attachment_type.TEXT
        )

        if member not in container:
            allure.attach(
                "NOT FOUND ❌",
                "RESULT",
                allure.attachment_type.TEXT
            )
            assert False, f"{member} not found in container"

        allure.attach(
            "FOUND ✅",
            "RESULT",
            allure.attachment_type.TEXT
        )