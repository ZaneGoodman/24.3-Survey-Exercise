from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

"""This list acts as a data server intended to house the answers given by the user from the questions given by the app"""
responses = []


@app.route('/')
def home_survey_page():
    """Displays Survey title and instructions, routes to first question on submission """
    return render_template("home_survey_page.html", 
    title=survey.title, 
    instructions=survey.instructions)


@app.route('/questions/<int:num>')
def questions(num):
    """Renders the form for the proper question in order.
            Redirect user to thank you page IF the user puts in a higher question number than is available and
            redirects user to the correct question if the user has not answered previous questions but attempts to skip
            to future questions.    
    """
    if num >= len(survey.questions):
        return redirect('/thank_you')
    if num != len(responses):
        flash("You haven't answered this questions yet!")
        return redirect(f'/questions/{len(responses)}')
    else:
        num = len(responses)
        return render_template('questions.html', 
        question=survey.questions[num].question, 
        answers=survey.questions[num].choices)


@app.route('/answers', methods=["POST"])
def answers():
    """
    Handles post request from each question form and adds question data to responses list. Then checks to see if there is 
    another question after the current one. If so redirect to that page. If not reset the responses list and 
    redirect to the thank you page.    

    >> NOTE: The instructions state "Once theyve answered all of the questions, trying to access any 
            of the question pages should redirect them to the thank you page." I did not follow this because this requires 
            the user to manually go back to the start page to try the survey again. Instead I added a restart button
            to the thank you page which sends the user back to the home survey page. To do this without throwing an index error
            I needed to clear the responses list once the user answered all the questions. The only problem that arrises from doing
            this is that once the user completes the survey they can manually imput a question number, only one that exist,
            and the page will redirect them back to the first question because the responses list is now empty, 
            otherwise they will be redirected back to the thank you page.
            This allows for the app to run more fluidly without completing step 8. 
    """
    answer = request.form.get("choice")
    responses.append(answer)
    if len(responses) != len(survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        responses.clear()
        return redirect("/thank_you")
      


@app.route('/thank_you')
def completed_survey():
    """Page shown once the user has answered all questions"""
    return render_template("completed.html")
    

    


