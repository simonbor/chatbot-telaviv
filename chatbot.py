import csv
from random import randint
from review import Review
from flask import Flask, render_template
from flask import request, jsonify

app = Flask(__name__) # initiate the app

##### User Message Processing #########################################################################################
def swear_words(user_msg):
    """
    This function checks user_msg for swear words

    :param user_msg: string
    :return: boolean
    """

    swear_word_bank = ['fuck', 'asshole', 'bitch', 'whore', 'slut', 'dick']

    for swear_word in swear_word_bank:

        if swear_word in user_msg:

            return True

    return False

def recommendation_request(user_msg):
    """
    This function checks user_msg for recommendation requests

    :param user_msg: string
    :return: boolean
    """

    if 'recommend me' in user_msg or 'recommend' in user_msg:

        return True

    else:

       return False

##### Replies ##########################################################################################################

def recommendation():
    """
    This function randomly selects a cafe from the cafes.csv file and uses
    string formatting to put the cafe's information into a response message

    :param None
    :return: str
    """

    # stores cafes information
    cafes = []

    # opens cafes csv file & saves info into cafes list
    with open('cafes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            cafe_data = {'cafe_name': row[0], 'cafe_address': row[1]}
            cafes.append(cafe_data)

    # randomly selects number between 0 and length of cafes list
    selector = randint(0, len(cafes))
    selected_cafe = cafes[selector]

    response_msg = "I think you might enjoy {0}. Located at {1}. Message me back to tell me what you thought of it!".format(
        selected_cafe['cafe_name'], selected_cafe['cafe_address'])

    return response_msg

def review(user_msg):
    """
    This function analyzes the users review of a cafe and returns a response
    about the sentiment of the review.

    :param user_msg: string
    :return: str
    """

    # initiate review object
    rvw = Review(user_msg)

    # determine if review is positive or negative
    predicted_sentiment = rvw.predict_sentiment()

    # store review
    #rvw.store_review()

    # if positive, respond to positive experience
    if predicted_sentiment == 1:
        response_msg = "Based on your review, it seems that you had a good time. Great! For another recommendation, please write: recommend me"
        sentiment = True

    # otherwise it was negative, respond to negative experience
    else:
        response_msg = "Based on your review, it seems that you did not have a good time. I'm sorry! For another recommendation, please write: recommend me"
        sentiment = False

    return response_msg, sentiment

##### Chatbot Functionality ############################################################################################
# route decorator allows us to bind a function to a URL & verb

@app.route('/',  methods=['GET'])
def index():
    return render_template("chatbot.html")

@app.route('/chat', methods=['POST']) # automatically has the "request" variable
def chat():
    user_msg = request.form.to_dict().get('msg').lower()
    animations = ['takeoff', 'excited', 'crying', 'dancing', 'bored', 'heartbroke']
        
    swear_bool = swear_words(user_msg)
    recommendation_bool = recommendation_request(user_msg)
    
    # chatbot logic
    if swear_bool is True:
        animation = animations[0]
        response_msg = "I have detected indecent language in your response. Please choose appropriate words. For a recommendation, please write: recommend me"

    elif recommendation_bool is True:
        animation = animations[1]
        response_msg = recommendation()

    else:
        animation = animations[2]
        response_msg, sentiment = review(user_msg)

        if sentiment:
            animation = animations[3]
        else:
            animation = animations[5]
        
    # and you can create "response" variables easily
    response = jsonify({"animation": animation, "msg": response_msg})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    """
    user_msg = raw_input("")

    # first get booleans for the chatbot logic
    swear_bool = swear_words(user_msg)
    recommendation_bool = recommendation_request(user_msg)
    
    # chatbot logic
    if swear_bool is True:
        response_msg = "I have detected indecent language in your response. Please choose appropriate words. For a recommendation, please write: recommend me"

    elif recommendation_bool is True:
        response_msg = recommendation()

    else:
        response_msg = review(user_msg)

    print response_msg
    """

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)

def hello_world():
    return "hello world"

if __name__ == '__main__':
    # app.run(debug=True) # run the app inside the main
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


"""
    print "Hello! My name is Tel Aviv Cafebot. I am a chatbot designed to recommend cafes in Tel Aviv!"
    print "For a recommendation, please write: recommend me"

    while True:

        chat()

This restaurant was awful. The food was so bad and the service was slow. Never going again!
This restaurant was the best! I loved the pizza and the service was fast.

        
"""





