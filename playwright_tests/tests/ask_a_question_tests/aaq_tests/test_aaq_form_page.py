import allure
import pytest
from pytest_check import check

from playwright.sync_api import expect, Page
from playwright_tests.core.testutilities import TestUtilities
from playwright_tests.messages.ask_a_question_messages.AAQ_messages.aaq_form_page_messages import (
    AAQFormMessages)
from playwright_tests.messages.ask_a_question_messages.AAQ_messages.question_page_messages import \
    QuestionPageMessages
from playwright_tests.messages.ask_a_question_messages.contact_support_messages import (
    ContactSupportMessages)
from playwright_tests.messages.contribute_messages.con_pages.con_page_messages import (
    ContributePageMessages)
from playwright_tests.pages.sumo_pages import SumoPages


# C2188694, C2188695
@pytest.mark.aaqPage
def test_community_card_and_helpful_tip_are_displayed_for_freemium_product(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    with allure.step("Signing in with a non-admin user account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts['TEST_ACCOUNT_12']
        ))

    with allure.step("Navigating to each freemium aaq form"):
        for freemium_product in test_utilities.general_test_data["freemium_products"]:
            test_utilities.navigate_to_link(
                test_utilities.aaq_question_test_data["products_aaq_url"][freemium_product]
            )

            with allure.step(f"Verifying that the helpful tip card is displayed for the "
                             f"{freemium_product} product"):
                expect(sumo_pages.aaq_form_page._get_helpful_tip_locator()).to_be_visible()

            with allure.step("Clicking on the 'Learn More' button from the community help "
                             "card and verifying that we are on the contribute messages page"):
                sumo_pages.aaq_form_page._click_on_learn_more_button()
                expect(page).to_have_url(ContributePageMessages.STAGE_CONTRIBUTE_PAGE_URL)


# C2188694, C2188695
@pytest.mark.aaqPage
def test_community_card_and_helpful_tip_not_displayed_for_premium_products(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    with allure.step("Signing in with a non-admin account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts['TEST_ACCOUNT_12']
        ))

    with allure.step("Navigating to each premium aaq form"):
        for premium_product in test_utilities.general_test_data["premium_products"]:
            test_utilities.navigate_to_link(
                test_utilities.aaq_question_test_data["products_aaq_url"][premium_product]
            )

            with allure.step(f"Verifying that the helpful tip options is displayed for the "
                             f"{premium_product}"):
                expect(sumo_pages.aaq_form_page._get_helpful_tip_locator()).to_be_hidden()

            with allure.step("Verifying that the 'Learn More' button from the community help "
                             "banner is not displayed"):
                expect(sumo_pages.aaq_form_page._get_learn_more_button_locator()).to_be_hidden()


# C1511570
@pytest.mark.aaqPage
@pytest.mark.parametrize("username", ['', 'TEST_ACCOUNT_12', 'TEST_ACCOUNT_MODERATOR'])
def test_scam_banner_premium_products_not_displayed(page: Page, username):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    if username != '':
        with allure.step(f"Singing in with {username} user"):
            test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
                test_utilities.user_secrets_accounts[username]
            ))

    with allure.step("Navigating to each premium product solutions page"):
        for premium_product in test_utilities.general_test_data["premium_products"]:
            test_utilities.navigate_to_link(
                test_utilities.general_test_data["product_solutions"][premium_product]
            )

            with allure.step(f"Verifying that the sam banner is not displayed for "
                             f"{premium_product} card"):
                expect(sumo_pages.product_solutions_page._get_scam_banner_locator()).to_be_hidden()

            if username != '':
                with allure.step("Clicking on the Ask Now button and verifying that the scam "
                                 "banner is not displayed"):
                    sumo_pages.product_solutions_page._click_ask_now_button()
                    test_utilities.wait_for_url_to_be(
                        test_utilities.aaq_question_test_data["products_aaq_url"][premium_product]
                    )
                    expect(sumo_pages.product_solutions_page._get_scam_banner_locator()
                           ).to_be_hidden()


# C2190040
@pytest.mark.aaqPage
@pytest.mark.parametrize("username", ['', 'TEST_ACCOUNT_12', 'TEST_ACCOUNT_MODERATOR'])
def test_scam_banner_for_freemium_products_is_displayed(page: Page, username):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    if username != '':
        with allure.step(f"Signing in with {username} user"):
            test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
                test_utilities.user_secrets_accounts[username]
            ))

    with allure.step("Navigating to each freemium product solutions page"):
        for freemium_product in test_utilities.general_test_data["freemium_products"]:
            test_utilities.navigate_to_link(
                test_utilities.general_test_data["product_solutions"][freemium_product]
            )

            with check, allure.step("Verifying that the 'Learn More' button contains the "
                                    "correct link"):
                assert sumo_pages.product_solutions_page._get_scam_alert_banner_link(
                ) == QuestionPageMessages.AVOID_SCAM_SUPPORT_LEARN_MORE_LINK

            if username != '':
                with check, allure.step("Clicking on the Ask Now button and verifying that "
                                        "the 'Learn More' button contains the correct link"):
                    sumo_pages.product_solutions_page._click_ask_now_button()
                    test_utilities.wait_for_url_to_be(
                        test_utilities.aaq_question_test_data["products_aaq_url"][freemium_product]
                    )
                    assert sumo_pages.product_solutions_page._get_scam_alert_banner_link(
                    ) == QuestionPageMessages.AVOID_SCAM_SUPPORT_LEARN_MORE_LINK


# C890537
@pytest.mark.aaqPage
def test_corresponding_aaq_product_name_and_image_are_displayed(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    with allure.step("Signing in with a non-admin account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts['TEST_ACCOUNT_12']
        ))

    with allure.step("Navigating to each product aaq form"):
        for product in test_utilities.aaq_question_test_data["products_aaq_url"]:
            test_utilities.navigate_to_link(
                test_utilities.aaq_question_test_data["products_aaq_url"][product])

            # This needs to change when we add the Mozilla Account icon/product.
            if product != "Mozilla Account":
                with allure.step("Verifying that the product image is displayed"):
                    expect(sumo_pages.aaq_form_page._get_product_image_locator()).to_be_visible()
            else:
                with allure.step("Verifying that the product image is hidden for Mozilla "
                                 "Account product"):
                    expect(sumo_pages.aaq_form_page._get_product_image_locator()).to_be_visible()

            with check, allure.step("Verifying that the correct product header is displayed"):
                assert sumo_pages.aaq_form_page._get_aaq_form_page_heading() == product


# C890535, C890536
@pytest.mark.aaqPage
def test_progress_milestone_redirect(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    with allure.step("Signing in with a non-admin user account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts['TEST_ACCOUNT_12']
        ))

    with allure.step("Navigating to each product AAQ form"):
        for product in test_utilities.aaq_question_test_data["products_aaq_url"]:
            test_utilities.navigate_to_link(
                test_utilities.aaq_question_test_data["products_aaq_url"][product])

            with check, allure.step("Verifying that the correct in progress milestone is "
                                    "displayed"):
                assert sumo_pages.aaq_form_page._get_in_progress_item_label(
                ) == AAQFormMessages.IN_PROGRESS_MILESTONE

            with allure.step(f"Clicking on the {AAQFormMessages.COMPLETED_MILESTONE_TWO} "
                             f"milestone and verifying that we are on the correct product "
                             f"solutions page"):
                sumo_pages.aaq_form_page._click_on_a_particular_completed_milestone(
                    AAQFormMessages.COMPLETED_MILESTONE_TWO)
                expect(page).to_have_url(
                    test_utilities.general_test_data["product_solutions"][product])

            with allure.step(f"Navigating back to the aaq form and clicking on the "
                             f"{AAQFormMessages.COMPLETED_MILESTONE_ONE} milestone"):
                test_utilities.navigate_to_link(
                    test_utilities.aaq_question_test_data["products_aaq_url"][product])
                sumo_pages.aaq_form_page._click_on_a_particular_completed_milestone(
                    AAQFormMessages.COMPLETED_MILESTONE_ONE)
                expect(page).to_have_url(ContactSupportMessages.PAGE_URL_CHANGE_PRODUCT_REDIRECT)


# C890612
@pytest.mark.aaqPage
def test_aaq_form_cancel_button_freemium_products(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    with allure.step("Signing in with a non-admin user account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts["TEST_ACCOUNT_MESSAGE_1"]
        ))

    with allure.step("Accessing the 'My profile' page via the top-navbar menu and extracting "
                     "the original number of posted questions"):
        sumo_pages.top_navbar._click_on_view_profile_option()
        original_number_of_questions = test_utilities.number_extraction_from_string(
            sumo_pages.my_profile_page._get_my_profile_questions_text()
        )

    with allure.step("Navigating to each product AAQ form"):
        for product in test_utilities.general_test_data["freemium_products"]:
            test_utilities.navigate_to_link(
                test_utilities.aaq_question_test_data["products_aaq_url"][product])

            with allure.step("Adding data inside the AAQ form fields and clicking on the "
                             "cancel button"):
                sumo_pages.aaq_flow.add__valid_data_to_all_aaq_fields_without_submitting(
                    subject=test_utilities.aaq_question_test_data["valid_firefox_question"]
                    ["subject"],
                    topic_value=sumo_pages.aaq_form_page._get_aaq_form_topic_options()[0],
                    body_text=test_utilities.aaq_question_test_data["valid_firefox_question"]
                    ["question_body"]
                )
                sumo_pages.aaq_form_page._click_aaq_form_cancel_button()

            with allure.step("Verifying that we are redirected back to the correct product "
                             "solutions page"):
                expect(page).to_have_url(
                    test_utilities.general_test_data["product_solutions"][product])

            with check, allure.step("Navigating back to the My Profile page and verifying "
                                    "that the correct number of posted questions is "
                                    "displayed"):
                sumo_pages.top_navbar._click_on_view_profile_option()
                new_number = test_utilities.number_extraction_from_string(
                    sumo_pages.my_profile_page._get_my_profile_questions_text()
                )
                assert new_number == original_number_of_questions


# C890614, C890613, C890538
@pytest.mark.aaqPage
def test_post_aaq_questions_for_all_freemium_products_topics(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    with allure.step("Signing in with an admin account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts["TEST_ACCOUNT_MODERATOR"]
        ))

    with allure.step("Navigating to each product AAQ form"):
        for product in test_utilities.general_test_data["freemium_products"]:
            test_utilities.navigate_to_link(
                test_utilities.aaq_question_test_data["products_aaq_url"][product])

            for topic in sumo_pages.aaq_form_page._get_aaq_form_topic_options():
                with allure.step(f"Submitting question for {product} product"):
                    question_info = sumo_pages.aaq_flow.submit_an_aaq_question(
                        subject=test_utilities.aaq_question_test_data["valid_firefox_question"]
                        ["subject"],
                        topic_name=topic,
                        body=test_utilities.aaq_question_test_data["valid_firefox_question"]
                        ["question_body"],
                        attach_image=False
                    )

                with allure.step("Verifying that the correct implicit tags are added to the "
                                 "question"):
                    topic_s = (test_utilities
                               .aaq_question_test_data['aaq_topic_tags'][product][topic])
                    if isinstance(topic_s, list):
                        slugs = topic_s
                    else:
                        slugs = [topic_s]
                    if (test_utilities.aaq_question_test_data['aaq_topic_tags'][product]
                            ['default_slug'] != "none"):
                        slugs.append(
                            test_utilities.aaq_question_test_data['aaq_topic_tags'][product]
                            ['default_slug']
                        )
                    assert (
                        all(map(
                            lambda x: x in sumo_pages.question_page._get_question_tag_options(),
                            slugs))
                    )

                with allure.step("Clicking on the 'My Questions' banner option and Verifying "
                                 "that the posted question is displayed inside the 'My "
                                 "Questions page"):
                    sumo_pages.question_page._click_on_my_questions_banner_option()
                    expect(sumo_pages.my_questions_page._get_listed_question(
                        question_info['aaq_subject'])).to_be_visible()

                with allure.step("Clicking on the question and deleting it"):
                    sumo_pages.my_questions_page._click_on_a_question_by_name(
                        question_info['aaq_subject']
                    )
                    sumo_pages.aaq_flow.deleting_question_flow()

                with allure.step("Verifying that the question is no longer displayed inside "
                                 "My Questions page"):
                    sumo_pages.top_navbar._click_on_my_questions_profile_option()
                    expect(
                        sumo_pages.my_questions_page._get_listed_question(
                            question_info['aaq_subject'])).to_be_hidden()

                with allure.step(f"Navigating back to the {product} product aa form"):
                    test_utilities.navigate_to_link(
                        test_utilities.aaq_question_test_data["products_aaq_url"][product])


@pytest.mark.aaqPage
def test_share_firefox_data_functionality(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    with allure.step("Signing in with an admin user account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts["TEST_ACCOUNT_MODERATOR"]
        ))

    with allure.step("Navigating to the Firefox AAQ form page and clicking on the 'Share "
                     "Data' option"):
        test_utilities.navigate_to_link(
            test_utilities.aaq_question_test_data["products_aaq_url"]["Firefox"])
        sumo_pages.aaq_form_page._click_on_share_data_button()

    with check, allure.step("Verifying that the 'try these manual steps' contains the "
                            "correct link"):
        assert sumo_pages.aaq_form_page._get_try_these_manual_steps_link(
        ) == QuestionPageMessages.TRY_THESE_MANUAL_STEPS_LINK

    with allure.step("Adding data inside AAQ form fields without submitting the form"):
        sumo_pages.aaq_flow.add__valid_data_to_all_aaq_fields_without_submitting(
            subject=test_utilities.aaq_question_test_data["valid_firefox_question"]["subject"],
            topic_value=sumo_pages.aaq_form_page._get_aaq_form_topic_options()[0],
            body_text=test_utilities.aaq_question_test_data["valid_firefox_question"]
            ["question_body"]
        )

    with allure.step("Adding text inside the troubleshooting information field and "
                     "submitting the AAQ question"):
        sumo_pages.aaq_form_page._add_text_to_troubleshooting_information_textarea(
            test_utilities.aaq_question_test_data["troubleshooting_information"]
        )
        sumo_pages.aaq_form_page._click_aaq_form_submit_button()

    with allure.step("Verifying that the troubleshooting information is displayed"):
        sumo_pages.question_page._click_on_question_details_button()
        sumo_pages.question_page._click_on_more_system_details_option()
        expect(
            sumo_pages.question_page._get_more_information_with_text_locator(
                test_utilities.aaq_question_test_data["troubleshooting_information"]
            )
        ).to_be_visible()

    with allure.step("Closing the additional details panel and deleting the posted question"):
        sumo_pages.question_page._click_on_the_additional_system_panel_close()
        sumo_pages.aaq_flow.deleting_question_flow()


@pytest.mark.aaqPage
def test_additional_system_details_user_agent_information(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    with allure.step("Signing in with an admin user account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts["TEST_ACCOUNT_MODERATOR"]
        ))

    with allure.step("Navigating to each product aaq form"):
        for product in test_utilities.general_test_data["freemium_products"]:
            test_utilities.navigate_to_link(
                test_utilities.aaq_question_test_data["products_aaq_url"][product])

            with allure.step(f"Submitting a question for the {product} product"):
                sumo_pages.aaq_flow.submit_an_aaq_question(
                    subject=test_utilities.aaq_question_test_data["valid_firefox_question"]
                    ["subject"],
                    topic_name=sumo_pages.aaq_form_page._get_aaq_form_topic_options()[0],
                    body=test_utilities.aaq_question_test_data["valid_firefox_question"]
                    ["question_body"],
                    attach_image=True
                )

            with check, allure.step("Verifying that the correct user-agent information is "
                                    "displayed"):
                sumo_pages.question_page._click_on_question_details_button()
                sumo_pages.question_page._click_on_more_system_details_option()
                assert "User Agent: " + test_utilities.get_user_agent(
                ) == sumo_pages.question_page._get_user_agent_information()

            with allure.step("Closing the additional details panel and deleting the posted "
                             "questions"):
                sumo_pages.question_page._click_on_the_additional_system_panel_close()
                sumo_pages.aaq_flow.deleting_question_flow()


@pytest.mark.aaqPage
def test_system_details_information(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    troubleshooting_info = [
        test_utilities.aaq_question_test_data["troubleshoot_product_and_os_versions"][
            0],
        "Firefox " + test_utilities.aaq_question_test_data["troubleshoot_product_and_os_versions"]
        [1]
    ]

    with allure.step("Signing in with an admin user account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts["TEST_ACCOUNT_MODERATOR"]
        ))

    with allure.step("Navigating to each product aaq form and and adding data without "
                     "submitting the form"):
        for product in test_utilities.general_test_data["freemium_products"]:
            if product == "Thunderbird":
                continue
            else:
                test_utilities.navigate_to_link(
                    test_utilities.aaq_question_test_data["products_aaq_url"][product])
                sumo_pages.aaq_flow.add__valid_data_to_all_aaq_fields_without_submitting(
                    subject=test_utilities.aaq_question_test_data["valid_firefox_question"]
                    ["subject"],
                    topic_value=sumo_pages.aaq_form_page._get_aaq_form_topic_options()[0],
                    body_text=test_utilities.aaq_question_test_data["valid_firefox_question"][
                        "question_body"]
                )

                with allure.step("Clicking on the 'Show details' option and adding data to "
                                 "product version and OS fields"):
                    sumo_pages.aaq_form_page._click_on_show_details_option()
                    sumo_pages.aaq_form_page._add_text_to_product_version_field(
                        test_utilities.aaq_question_test_data[
                            "troubleshoot_product_and_os_versions"][1]
                    )
                    sumo_pages.aaq_form_page._add_text_to_os_field(
                        test_utilities.aaq_question_test_data[
                            "troubleshoot_product_and_os_versions"][0]
                    )

                with check, allure.step("Submitting the AAQ question and verifying that the "
                                        "correct provided troubleshooting information is "
                                        "displayed"):
                    sumo_pages.aaq_form_page._click_aaq_form_submit_button()
                    sumo_pages.question_page._click_on_question_details_button()
                    assert sumo_pages.question_page._get_system_details_information(
                    ) == troubleshooting_info

                with allure.step("Deleting the posted question"):
                    sumo_pages.aaq_flow.deleting_question_flow()


# C1512592
@pytest.mark.aaqPage
def test_premium_products_aaq(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    aaq_form_messages = AAQFormMessages()
    with allure.step("Signing in with an admin account"):
        test_utilities.start_existing_session(test_utilities.username_extraction_from_email(
            test_utilities.user_secrets_accounts["TEST_ACCOUNT_MODERATOR"]
        ))

    with allure.step("Navigating to each premium product contact form and sending a ticket"):
        for premium_product in test_utilities.general_test_data['premium_products']:
            test_utilities.navigate_to_link(
                test_utilities.aaq_question_test_data['products_aaq_url'][premium_product]
            )
            test_utilities.wait_for_dom_to_load()
            if premium_product == 'Mozilla VPN':
                sumo_pages.aaq_flow.submit_an_aaq_question(
                    subject=test_utilities.aaq_question_test_data['premium_aaq_question']
                    ['subject'],
                    body=test_utilities.aaq_question_test_data['premium_aaq_question']['body'],
                    is_premium=True
                )
            else:
                sumo_pages.aaq_flow.submit_an_aaq_question(
                    subject=test_utilities.aaq_question_test_data['premium_aaq_question']
                    ['subject'],
                    body=test_utilities.aaq_question_test_data['premium_aaq_question']['body'],
                    is_premium=True
                )

        with allure.step("Verifying that the correct success message is displayed"):
            assert sumo_pages.aaq_form_page._get_premium_card_submission_message(
            ) == aaq_form_messages.get_premium_ticket_submission_success_message(
                test_utilities.user_secrets_accounts["TEST_ACCOUNT_MODERATOR"]
            )


# C2635907
@pytest.mark.aaqPage
def test_loginless_mozilla_account_aaq(page: Page):
    test_utilities = TestUtilities(page)
    sumo_pages = SumoPages(page)
    aaq_form_messages = AAQFormMessages()
    with allure.step("Sending 4 loginless tickets and verifying that the user is successfully "
                     "blocked after 3 submissions"):
        i = 1
        while i <= 4:
            sumo_pages.top_navbar._click_on_signin_signup_button()
            sumo_pages.auth_page._click_on_cant_sign_in_to_my_mozilla_account_link()
            sumo_pages.aaq_flow.submit_an_aaq_question(
                subject=test_utilities.aaq_question_test_data['premium_aaq_question']['subject'],
                body=test_utilities.aaq_question_test_data['premium_aaq_question']['body'],
                is_premium=True,
                email=test_utilities.user_secrets_accounts["TEST_ACCOUNT_MODERATOR"],
                is_loginless=True
            )
            if i <= 3:
                with allure.step("Verifying that the correct success message is displayed"):
                    assert sumo_pages.aaq_form_page._get_premium_card_submission_message(
                    ) == aaq_form_messages.get_premium_ticket_submission_success_message(
                        test_utilities.user_secrets_accounts["TEST_ACCOUNT_MODERATOR"]
                    )
            else:
                with allure.step("Verifying that submission error message is displayed"):
                    assert sumo_pages.aaq_form_page._get_premium_card_submission_message(
                    ) == aaq_form_messages.LOGINLESS_RATELIMIT_REACHED_MESSAGE
            i += 1
