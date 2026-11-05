

# workflows

# password reset

    email -> check in db -> if email exists -> yes -> create reset link -> send email -> show success message
                                            -> no -> show error message

# interview
    review resume -> if ok -> send invitation -> conduct interview -> if qualified -> send offer letter 
                  -> else -> send to backlog.                      -> not qualified -> send rejection email


# password 
email, email exits, reset link, email sewnt or not, message (success, fail)
data -> state

collect email
check in db
generate reset link
send email
show message

actions -> nodes -> python functions

nodes connect -> edges

# pip install langgraph


