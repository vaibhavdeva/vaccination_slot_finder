
class Parameters():

    # api
    endpoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/"
    find_by_pin = "findByPin"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    pincodes = "<list_of_pincodes_to_look_for>" #e.g. [112211, 323431]
    interval = 10 #seconds
    lookup_horizon = 0 # number of days from today

    # email
    port = 465  # For SSL
    password = "<gmail_password>"
    sender_email = "<email_id>"
    receiver_email = "<list_of_receiver_email_ids>" # e.g. ["email1@domain.com", "email2@domain.com"]

    # extract data
    expected_keys = ["name", "address", "pincode", "fee_type", "date", "available_capacity", "min_age_limit", "vaccine", "slots"]
