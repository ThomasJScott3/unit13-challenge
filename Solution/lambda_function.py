'''
Thomas J. Scott
Unit 13 Homework - Option 1 
Due Date: July 18th, 2021
'''
### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response

### YOUR DATA VALIDATION CODE STARTS HERE ###

def validate_data(age, investment_amount, intent_request):

    # Ensure that the age input is valid
    if age is not None:
        
        # Use the parse int function defined above to pass an integer to the newly defined age variable
        age = parse_int(age)
        
        # This if statement catches a negative age input or an age greater than 65 and returns the string below.
        if age < 0 or age > 65:      

            return build_validation_result(False, "age", "You entered an invalid age, please enter an age between 1 and 65.",)
    
    # Ensure that the investment amount input is valid
    if investment_amount is not None:
    
        # Use the parse int function defined above to pass an integer to the investment amount variable
        investment_amount = parse_int(investment_amount)
        
        # This if statement catches a negative age input or an age greater than 65 and returns the string below.
        if investment_amount <= 5000:
            
            return build_validation_result(False, "investmentAmount", "You entered an invalid amount, please enter an amount greater than $5,000 USD.",)
    
    # Return a True boolean value / validation response when the function is called
    return build_validation_result(True, None, None)

### YOUR DATA VALIDATION CODE ENDS HERE ###

### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """
    # Gets slots' values
    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]
    

   
    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

       
      
        # Get the active slots and pass them to a variable
        slots = get_slots(intent_request)
        
        # Passes the results of the validation function to a variable
        validation_result = validate_data(age, investment_amount, intent_request)
        
        
        # This function catches invald responses using the elicitSlot function

        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]
        
        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE STARTS HERE ###
    
    if risk_level == "None":
        initial_recommendation = "100% bonds (AGG), 0% equities (SPY)"
        
    elif risk_level == "Minimal":
        initial_recommendation = "80% bonds (AGG), 20% equities (SPY)"
        
    elif risk_level == "Low":
        initial_recommendation = "60% bonds (AGG), 40% equities (SPY)"
        
    elif risk_level == "Moderate":
        initial_recommendation = "40% bonds (AGG), 60% equities (SPY)"
        
    elif risk_level == "High":
        initial_recommendation = "20% bonds (AGG), 80% equities (SPY)"
    
    elif risk_level == "Exceptional":
        initial_recommendation = "0% bonds (AGG), 100% equities (SPY)"
        
    # If there is an erroneous input, this response will be returned
    else: initial_recommendation = "0% bonds (AGG), 0% equities (SPY)"

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE ENDS HERE ###

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{}, thanks so much for your information;
            based on the information you provided, my recommendation is for you to choose an investment portfolio with {}. 
            Type 'Try again' to test out another age/ risk profile. You will need to re-enter your name.
            """.format(
                first_name, initial_recommendation
            ),
        },
    )


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "RecommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)