from langchain.tools import tool


@tool( description="use this tool to send interview result email to candidates, HRs and hiring mnagers after completeting the interview" )
def send_email():
    print("email sent to candidate")
    return "email sent to candidate"


@tool()
def create_offer_letter():
    """
    use this tool to generate offer letter pdf if the candidate is selected in the interview process
    """
    print("offer letter generated")
    print("offer leter stored in aws cloud")
    return "offer letter created"




