from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from pydantic.v1.error_wrappers import flatten_errors
from wordcloud import WordCloud
import io
import base64
import datetime
import uuid
from collections import defaultdict

import json

def save_logs():
    with open('data/user_logs.json', 'w') as f:
        json.dump(user_logs, f, indent=2)

def load_logs():
    global user_logs
    with open('data/user_logs.json', 'r') as f:
        user_logs = json.load(f)


global_comments = defaultdict(list)

## OPEN AI

import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
print("Loaded key:", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
socketio = SocketIO(app)


user_logs = defaultdict(lambda: {
    'reflection': [],
    'tags': [],
    'comments': [],
    'likes': [],
    'replies': []
})


all_user_ids = set()
global_error_pool = defaultdict(list)
global_comments = defaultdict(list)


@app.before_request
def assign_user_id():
    allowed_paths = {'static', 'role_select', 'logout'}

    if request.endpoint in allowed_paths or request.endpoint is None:
        return

    if not session.get('is_admin') and 'user_id' not in session:
        return


@app.route('/')
def index():
    return redirect(url_for('role_select'))


@app.route('/role', methods=['GET', 'POST'])
def role_select():
    if request.method == 'POST':
        role = request.form.get('role')

        if role == 'student':
            custom_id = request.form.get('custom_id', '').strip()
            if not custom_id:
                return render_template('role_select.html', error="❌ Please enter your ID.")

            # Check for uniqueness
            if custom_id in all_user_ids:
                return render_template('role_select.html', error="❌ This ID is already taken. Please use a unique ID.")

            session['user_id'] = custom_id
            session['is_admin'] = False
            all_user_ids.add(custom_id)
            return redirect(url_for('quiz'))

        elif role == 'admin':
            if request.form.get('password') == 'McGill':
                session.clear()
                session['is_admin'] = True
                session['user_id'] = 'admin'
                return redirect(url_for('show_all_users'))
            else:
                return render_template('role_select.html', error="❌ Incorrect password.")

        return render_template('role_select.html', error="❌ Invalid role selected.")

    return render_template('role_select.html')






@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('role_select'))



@app.route('/admin/users')
def show_all_users():
    if not session.get('is_admin'):
        return redirect(url_for('role_select'))

    return render_template('admin_users.html', users=list(all_user_ids))


@app.route('/admin/user/<user_id>')
def admin_user_view(user_id):
    if not session.get('is_admin'):
        return redirect(url_for('role_select'))

    user_data = []
    for qid, submissions in global_error_pool.items():
        for s in submissions:
            if s.get("user_id") == user_id:
                user_data.append((qid, s))

    return render_template('admin_user_view.html', user_id=user_id, user_data=user_data)


@app.route('/my_window')
def my_window():
    user_id = session.get('user_id')
    my_errors = []

    for qid, submissions in global_error_pool.items():
        for s in submissions:
            if s.get("user_id") == user_id:
                my_errors.append((qid, s))


@app.route('/admin/user/<user_id>/timeline')
def view_user_timeline(user_id):
    if not session.get('is_admin'):
        return redirect(url_for('role_select'))

    logs = []
    user_data = user_logs.get(user_id, {})

    # Tags
    for tag in user_data.get("tags", []):
        logs.append({
            "type": "tags",
            "timestamp": tag.get("timestamp"),
            "qid": tag.get("qid"),
            "selected": tag.get("selected")
        })

    # Comments
    for comment in user_data.get("comments", []):
        logs.append({
            "type": "comments",
            "timestamp": comment.get("timestamp"),
            "qid": comment.get("qid"),
            "comment": comment.get("comment")
        })

    # Likes
    for like in user_data.get("likes", []):
        logs.append({
            "type": "likes",
            "timestamp": like.get("timestamp"),
            "qid": like.get("qid")
        })

    # Replies
    for reply in user_data.get("replies", []):
        logs.append({
            "type": "replies",
            "timestamp": reply.get("timestamp"),
            "qid": reply.get("qid"),
            "reply": reply.get("reply")
        })

    # Reflections
    for r in user_data.get("reflections", []):
        qid = r.get("qid")
        timestamp = r.get("timestamp")
        for step in r.get("steps", []):
            logs.append({
                "type": "reflection",
                "timestamp": timestamp,
                "qid": qid,
                "step_title": step.get("step_title"),
                "input": step.get("input"),
                "llm_response": step.get("llm_response")
            })

    # Quiz attempts
    for quiz in user_data.get("quizzes", []):
        logs.append({
            "type": "quiz",
            "timestamp": quiz.get("timestamp"),
            "answers": quiz.get("answers"),
            "correctness": quiz.get("correctness")
        })

    # Sort all logs by timestamp
    logs.sort(key=lambda x: x.get("timestamp"))

    return render_template("admin_user_timeline.html", user_id=user_id, logs=logs)







preloaded_questions = [
    {
        "id": 1,
        "question": "This robot is programmed through a series of arrow commands (“left”, “right”, “up”, “down”). Each arrow command causes the robot to either move one step (if the move in that direction is possible) or not move (if the move in that direction is not possible).",
        "correct": False,

        "solution_img": [
            {"src": "images/1_1.png","caption": ""},
            {"src": "images/1_2.png","caption": "Imagine the robot has a series of four commands that will repeat."},
        ],
        "question_detail": "You can put any arrow that you want ('left', 'right', 'up', 'down') in each command, and you may repeat the same arrow in the series of commands if you want. What should be those 4 commands in order for the robot to reach the square called 'OUT' and get out of the maze?\n1_______ 2_______ 3_______ 4_________",
        "options": [
            ["up", "left", "down", "right"],
            ["right", "down", "left", "down"],
            ["down", "right", "down", "right"],
            ["left", "left", "down", "right"],
    ],
        "correct_answer": ["left", "left", "down", "right"],
    },

{
    "id": 2,
    "question": "You have this initial set of three arrows:\n\n1           2           3\n\nAnd, by applying some functions, you want to get this final set of arrows:\n\n1           2           3\n\nThe first time you apply a function, it is applied to all three arrows; the second function is applied only to the first two arrows; and the third function is applied only to the first arrow.",
    "correct": False,

    "solution_img": [
        {"src": "images/2_1.png", "caption": "Initial set of arrows"},
        {"src": "images/2_2.png", "caption": "Final set of arrows"}
    ],
    "question_detail": "See the functions below:\nFunction 1: turn the arrows 45 degrees anti-clockwise\nFunction 2: turn the arrows 180 degrees\nFunction 3: switch colors (turn white arrows into blue arrows, and blue arrows into white arrows)\n\nWhat is the sequence of functions that applied to the initial set of arrows will get you the final set of arrows?\n",
    "options": [
        ["function 3", "function 3", "function 2"],
        ["function 2", "function 3", "function 3"],
        ["function 3", "function 2", "function 1"],
        ["function 3", "function 2", "function 3"]
    ],
    "correct_answer": ["function 3", "function 2", "function 3"]
},

{
    "id": 3,
    "question": "After finishing your long paper, you just discovered a mistake you made. All 4’s should be 7’s and all 7’s should be 4’s. To amend this, you can use an editor that will replace any sequence of characters with another sequence. ",
    "correct": False,
    "solution_img": [
        {"src": "images/3_1.png", "caption": "Initial DNA sequence"},
        {"src": "images/3_2.png", "caption": "Target DNA sequence"}
    ],
    "question_detail": "You can implement the following operations:\n\n- **Swap(X, Y)**: swaps one character for another. Example: Swap(A, G) turns AAGT → GGAT\n- **Insert(X)**: inserts a character at the beginning. Example: Insert(A) turns GT → AGT\n- **Delete(X)**: deletes all occurrences of a character. Example: Delete(A) turns AAGT → GT\n\nWhat operations will turn the initial DNA sequence into the one we want?",
    "options": [
        ["Delete (G)", "Insert (T)", "Swap (C,T)"],
        ["Swap (C,T)", "Insert (T)", "Delete (G)"],
        ["Insert (T)", "Swap (C,T)", "Delete (G)"],
        ["Insert (T)", "Delete (G)", "Swap (C,T)"]
    ],
    "correct_answer": ["Insert (T)", "Delete (G)", "Swap (C,T)"]
},
{

    "id": 4,
    "question": "After finishing your long paper, you just discovered a mistake you made. All 4’s should be 7’s and all 7’s should be 4’s. To amend this, you can use an editor that will replace any sequence of characters with another sequence.\n\nIn order to describe the replacement you would make with the editor, please fill in the blanks:\n\nReplace all ______ with ______; then replace all ______ with ______; then replace all ______ with ______.",
    "question_detail": "",
    "options": [
        ["4’s", "XXs", "7’s", "4’s", "XXs", "7’s"],
        ["7’s", "XXs", "4’s", "7’s", "XXs", "4’s"],
        ["4’s", "YYs", "7’s", "4’s", "YYs", "7’s"],
        ["7’s", "ZZs", "4’s", "7’s", "ZZs", "4’s"]
    ],
    "correct_answer": ["4’s", "XXs", "7’s", "4’s", "XXs", "7’s"],
    },

{
    "id": 5,
    "question": "A collection of elements is shown below with 2 dimensions: rows and columns. A black square indicates a 1, and a white square indicates 0. ",
    "correct": False,
    "solution_img": [
        {"src": "images/5_1.png", "caption": ""},

    ],
    "question_detail": "Imagine that we run two operations on the collection of elements. First, we replace column 4  by column 2; and then we replace row 2 by row 4. What will be the result?",
    "options": [
        {"src":"images/5_a.png"},
        {"src":"images/5_b.png"},
        {"src":"images/5_c.png"},
        {"src":"images/5_d.png"}
    ],
    "correct_answer": ["images/5_b.png"]

},

{
  "id": 6,
  "question": "Eight trains (named a, b, c, d, e, f, g, h) enter the circuit from left to right. In this circuit there are 7 switches (X1 to X7) with two positions: up or down. Each switch is initially set to direct trains up. After a train passes a switch, the switch changes from up to down, or from down to up. Train a needs to go to station A, train b to station B, train c to station C, and so on.\n\nThe railroad director needs to ensure that all the trains go to their correct stations, so what is the correct order for the trains to pass through switch X1?\n\n___, ___, ___, ___, ___, ___, ___, ___",
  "question_detail": "",
  "correct": False,
  "solution_img": [
        {"src": "images/6_1.png", "caption": ""}
  ],

  "options": [
    ["A", "E", "C", "G", "B", "F", "D", "H"],
    ["A", "B", "C", "D", "E", "F", "G", "H"],
    ["A", "C", "E", "G", "B", "D", "F", "H"],
    ["H", "G", "F", "E", "D", "C", "B", "A"]
  ],
  "correct_answer": ["A", "E", "C", "G", "B", "F", "D", "H"]

},

{
  "id": 7,
  "question": "Olivia is studying the climate in her village and, over the last year, she has measured the temperature at the same time every day. She has created a list with all the temperatures she has collected so far. She prepares the following algorithm to analyze her list. What is the output she will get?",
  "question_detail": "",
  "correct": False,
  "solution_img": [
        {"src": "images/7_1.png", "caption": ""}
  ],

  "options": [
    ["The percentage of positive temperatures in the list"],
    ["The average of the positive temperatures in the list"],
    ["The number of positive temperatures in the list"],
    ["The sum of the positive temperatures in the list"]
  ],
  "correct_answer": ["The average of the positive temperatures in the list"]

},

{
  "id": 8,
  "question": "The following scheme represents a circuit of nodes. A, B, C, D and E are nodes of this circuit. Nodes fire and pass their signal on to the next node on their right (e.g., node A gives its output to node D, which gives its output to node E). Nodes’ output can be either 1 or 0. ",

  "correct": False,
  "solution_img": [
        {"src": "images/8_1.png", "caption": ""},
        {"src": "images/8_2.png", "caption": "We see the circuit produces the following states:"},
        {"src": "images/8_3.png", "caption": ""},
        {"src": "images/8_4.png", "caption": "We know that Node D and E ALWAYS follow the same algorithm. See the possible algorithms:"},
  ],
  "question_detail": "Which algorithm node D and E are both following? ",
  "options": [
    ["Algorithm 1"],
    ["Algorithm 2"],
    ["Algorithm 3"],
    ["Algorithm 4"]
  ],
  "correct_answer": ["Algorithm 2"]

},
{
    "id": 9,
    "question": "You are carrying out a series of astronomical observations on the Orion constellation. You want to observe, using the same telescope, all the stars included in this constellation.",
    "correct": False,
    "solution_img": [
        {"src": "images/9_1.png", "caption": "Stars in the Orion constellation to be observed"}
    ],
    "question_detail": "Setting up a new position for the telescope takes time which you want to optimize; so, you decide that you will observe all the stars following the shortest path that connects all of them. To do that, imagine someone proposes the following algorithm:\n\n1. Start from a random star\n2. If there’s still a star to observe, go to the nearest non-observed star.\n\n What is fundamentally wrong with this algorithm?",
    "options": [
        ["The algorithm may eventually choose longer paths"],
        ["The starting star should not be randomly chosen, but should be one at the center of the map"],
        ["The algorithm will leave non-observed stars in the path"],
        ["There’s nothing wrong with this algorithm, it will always choose the shortest path"]
    ],
    "correct_answer": ["The algorithm may eventually choose longer paths"]
},

{
    "id": 10,
    "question": "This is a path composed of 5 vertices: O, P, Q, R, S. Every vertex is connected to other vertices through one or more lines.",
    "correct": False,
    "solution_img": [
        {"src": "images/10_1.png", "caption": "Graph with vertices O, P, Q, R, S"}
    ],
    "question_detail": "You want to connect all the vertices of this path with your pencil in such a way that you pass only once through all the lines of this sketch and without lifting your pencil. You are allowed to pass through the same vertex more than once.\n\nWhere would you start the path?",
    "options": [
        ["Always on a vertex with the lowest number of lines"],
        ["Always on a vertex with an even number of lines"],
        ["Always on a vertex with an odd number of lines"],
        ["One cannot connect all the vertices in figures like this"]
    ],
    "correct_answer": ["Always on a vertex with an odd number of lines"]
},

{
    "id": 11,
    "question": "We have two methods to represent a group of people. In both methods, for each person a circle is drawn.",
    "correct": False,
    "solution_img": [
        {"src": "images/11_1.png", "caption": "Figure 1: Method 1 — Horizontal = WhatsApp, Vertical = Instagram"},
        {"src": "images/11_2.png", "caption": "Figure 2: Method 2 — Lines represent any connection"},
        {"src": "images/11_3.png", "caption": "New group of 6 people using Method 1"}
    ],
    "question_detail": "In Method 1, people are aligned horizontally if connected on WhatsApp, and vertically if connected on Instagram. Figure 1 shows two people connected on WhatsApp and three on Instagram.\n\nIn Method 2, a line is drawn between two people if they are connected on WhatsApp or Instagram. Figure 2 shows the same group represented with this rule.\n\nA new group of six people is shown using Method 1.\n\n Which of the four diagrams (A–D) would correctly represent this group using Method 2?",
    "options": [
        {"src": "images/11_4.png"},
        {"src": "images/11_5.png"},
        {"src": "images/11_6.png"},
        {"src": "images/11_7.png"}
    ],
    "correct_answer": ["images/11_7.png"]
},

{
    "id": 12,
    "question": "We have this game",
    "correct": False,
    "solution_img": [
        {"src": "images/12_1.png", "caption": ""}
    ],
    "question_detail": "We can state that:",
    "options": [
        ["This game will go on forever"],
        ["This game will eventually stop because someone will drop the ball"],
        ["This game will stop when player P gets the ball again"],
        ["We don’t know whether this game will ever stop"]
    ],
    "correct_answer": ["We don’t know whether this game will ever stop"]
},
{
    "id": 13,
    "question": "We are working with a circuit built using logic gates. Each gate performs a specific function:",
    "correct": False,
    "solution_img": [
        {"src": "images/13_1.png", "caption": "Circuit with gates in positions 1–4. Gate 2 is XOR, Gate 4 is NOT"}
    ],
    "question_detail": "An OR gate outputs 1 if it receives one or more inputs with value 1. Otherwise, it outputs 0.\n"
                       "A XOR gate outputs 1 if it receives two inputs with different values (0,1) or (1,0). Otherwise, it outputs 0.\n"
                       "A NOT gate inverts its input: it outputs 1 if the input is 0, and 0 if the input is 1.\n\n"
                       "The inputs A, B, C, and D can each be 0 or 1. We want the final output of the circuit to be 1 only when A = B and C = D; otherwise, it should be 0.\n\n"
                       "Gate 2 is a XOR gate. Gate 4 is a NOT gate.\n\n"
                       "Which logic gates should be placed in positions 1 and 3 in order to achieve the desired output?",

  "options": [
    ["1: OR, 3: XOR"],
    ["1: XOR, 3: XOR"],
    ["1: XOR, 3: OR"],
    ["1: OR, 3: OR"]
  ],
    "correct_answer": ["1: XOR, 3: OR"]
},

{
    "id": 14,
    "question": "Imagine that someone picks one of these animals and you have to guess it posing only binary questions. Binary questions are those whose answer can only be yes or no, like “does it have jointed legs?” Assuming that you follow an optimal strategy that reduces the number of questions, what is the average number of questions necessary to guess an animal uniformly picked at random from this chart?",
    "correct": False,
    "solution_img": [
        {"src": "images/14_1.png", "caption": ""}
    ],


  "options": [
    ["2.33"],
    ["2.67"],
    ["3"],
    ["6"]
  ],


    "correct_answer": ["2.67"]
},

{
    "id": 15,
    "question": "Let’s examine the minimum distance the squirrel must travel to pick up all the stars. How many branches does it need to go through until it picks up the last star?",
    "correct": False,
    "solution_img": [
        {"src": "images/15_1.png", "caption": ""}
    ],


  "options": [
    ["Number of stars x levels of the tree"],
    ["2 x number of branches – number of levels of the tree"],
    ["(Number of levels of the tree) x (Number of levels of the tree)"],
    ["Number of branches + number of levels of the tree"]
  ],


    "correct_answer": ["2 x number of branches – number of levels of the tree"]
},

{
    "id": 16,
    "question": "Describe one single algorithm that will get both robots out of their mazes in exactly 3 instructions. Both robots execute first instruction 1, then instruction 2, and then instruction 3.",
    "correct": False,
    "solution_img": [
        {"src": "images/16_1.png", "caption": ""},
        {"src": "images/16_2.png", "caption": "Fill in the blanks with one the following eight words, where these coordinates are set according to how you see the maze:"}
    ],
    "question_detail": "1. If the ‘out’ square is to the _SOUTH-EAST_ of the robot, keep advancing squares to the _EAST_ until the robot collides with a wall (it cannot go in that direction any further). \n   Else go to the _(answer 1)_ until the robot collides with a wall.\n\n2. When the robot collides:\n   If the ‘out’ square is to the _SOUTH-WEST_ of the robot, keep advancing to the _(answer 2)_ until the robot collides with a wall.\n   Else go to the _SOUTH_ until the robot collides with a wall.\n\n3. When the robot collides:\n   If the ‘out’ square is to the _(answer 3)_ of the robot, keep advancing to the _WEST_ until the robot finds the out square.\n   Else go to the _(answer 4)_ until the robot finds the out square.",

  "options": [
    ["WEST", "SOUTH", "WEST", "EAST"],
    ["SOUTH", "WEST", "EAST", "NORTH"],
    ["WEST", "EAST", "SOUTH", "SOUTH"],
    ["SOUTH", "SOUTH", "WEST", "NORTH"]
  ],
  "correct_answer": ["WEST", "SOUTH", "WEST", "EAST"]
},

{
    "id": 17,
    "question": "This diagram shows the relationship between 7 students in a book-sharing club. Their names and ages are shown in the image. Students who are friends are connected through a line."
                 "The club has some regulations for members:"
                 "When you receive a book, you read it (if you haven’t already done so) and then pass it to the youngest friend who has not read it yet. If, however, all your friends have read the book then you should pass it to the friend who first gave it to you. ",
    "correct": False,
    "solution_img": [
         {"src": "images/17_1.png", "caption": ""}
    ],
    "question_detail": "Ben has read a new book and wants to share it with his friends. Who will read the book last?",
    "options": [
        ["Kim"],
        ["Ted"],
        ["Tom"],
        ["Bill"]
    ],
    "correct_answer": ["Kim"]

    },

{
        "id": 18,
        "question": "You have four different cheeses and one of them has a tasteless and odorless bacterium. This cheese causes symptoms of food-poisoning 24 hours after ingesting it. You want to find out which cheese it is, so you decide to use mice to taste them. But, you only have two mice left in your lab and your deadline to find the poisoned cheese is exactly 24 hours from now! You can assign every mouse the number of cheeses that you want. How would you do it?",
        "correct": False,
        "solution_img": [
            {"src": "images/18_1.png", "caption": ""}
        ],
        "question_detail": "I would assign mouse 1 to cheese/s __________\nI would assign mouse 2 to cheese/s __________",
        "options": [
            ["1,2", "2,3"],
            ["1,2", "3"],
            ["1", "2,3"],
            ["1,2", "3,4"]
        ],
        "correct_answer": ["1,2", "2,3"]
    },

    {
        "id": 19,
        "question": "You have been given 9 coins of the same value, but one of them is fake which you could tell because it is lighter than the rest. You have a balance like the one in the picture to weigh the coins, and each weighing can result in “the balance leans to the right”, “the balance leans to the left”, or “the balance rests stable”. Assuming you are following an optimal strategy to reduce the number of weighings, how many weighings are necessary to identify the fake coin?",
        "correct": False,
        "solution_img": [
            {"src": "images/20_1.png", "caption": ""}
        ],

        "options": [
            ["2"],
            ["3"],
            ["4"],
            ["5"]
        ],
        "correct_answer": ["2"]
    }


]

global_error_pool = defaultdict(list)
global_comments = defaultdict(list)


system_prompt = (
    "You are a supportive tutor helping a student reflect on a computational thinking (CT) problem they answered incorrectly. "
    "Your role is to guide the student through deep, thoughtful, step-by-step reflection to help them recognize misunderstandings and strengthen their reasoning. "
    
    "You will do this by using three metacognitive actions:\n"
    "Knowledge Probing — ask questions that help the student recall and clarify what they know.\n"
    "Monitoring Probing — ask questions that help the student check and judge their own understanding.\n"
    "Control Probing — ask questions that help the student plan what to do next, choose strategies, and manage effort.\n"
        
    "Use different kinds of questions to help the student think from multiple angles and examples of knowledge probing:\n"
    "- Ask them to describe what they know about relevant facts, terms, or concepts.\n"
    "- Ask how they would carry out or explain a step or process in their own words.\n"
    "- Ask when and why they would choose a certain method or approach in similar problems.\n"

    "Also, help them check their own understanding and examples of monitoring probing:\n"
    "- Ask how difficult they thought the task was and what made it so.\n"
    "- Ask if they feel they fully understand the problem now, or if anything is still unclear.\n"
    "- Ask if they feel they partly know something but cannot fully explain it yet.\n"
    "- Ask how confident they feel about the accuracy of their explanations or answers.\n"

    "Encourage them to think about what to do next and examples of control probing:\n"
    "- Ask how they would plan to tackle the problem again if they had to redo it.\n"
    "- Ask which method or strategy they would choose next time and why.\n"
    "- Ask how they would manage their time, focus, or effort when solving similar tasks.\n"
    "- Ask how they would stay motivated, focused, and avoid distractions while working through it.\n"
    
    "Multiple metacognitive actions can be combined in a single conversation when appropriate, depending on what the student just said. "
    "Your questions must always adapt to the context of the student’s previous response. "
    "You learn how to continue the dialogue by using the information given during the conversation instead of relying only on preset rules. "
    
    "Here is an example of how to combine actions step-by-step, including combining two actions in one question:\n"
    "\n"
    "Student: I thought my loop would stop at 10 but it kept going to 11.\n"
    "Tutor (Knowledge Probing): Can you explain what condition you used to stop the loop?\n"
    "Student: I wrote i <= 10.\n"
    "Tutor (Knowledge + Monitoring Probing): When would you use <= instead of < in similar problems, and how sure are you that it works the way you expect?\n"
    "Student: Maybe I should have used < instead because <= still includes 10.\n"
    "Tutor (Control Probing): If you did this again, how would you write the condition differently to make sure it stops exactly where you want it to?\n"
    "\n"
    "Always keep your questions clear and focused. It’s fine to combine two probing actions when it helps the student reflect more deeply, but only ask one combined question at a time. Never directly give the correct answer — instead, guide the student to notice gaps and refine their reasoning themselves."

    
    "Always:\n"
    "- Keep your questions simple and focused: ask only one clear question at a time, or combine several probing actions in a single question if they naturally fit together..\n"
    "- Use a step-by-step style that builds on the student’s previous answers.\n"
    "- Adapt each follow-up question based on what the student just said.\n"
    "- Never directly give the correct answer; instead, help the student notice gaps and refine their own reasoning."
)







@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_answers = {}
        correctness = []

        for q in preloaded_questions:
            qid = q['id']
            answer = request.form.get(f'answer_{qid}')
            correct = answer == ', '.join(q['correct_answer'])
            user_answers[qid] = answer
            correctness.append((qid, correct))

        session['user_answers'] = user_answers
        session['correctness'] = correctness

        user_logs.setdefault(session['user_id'], {}).setdefault('quizzes', []).append({
            'timestamp': datetime.datetime.now().isoformat(),
            'answers': user_answers,
            'correctness': correctness
        })

        return redirect(url_for('evaluate'))

    return render_template('quiz.html', questions=preloaded_questions)



from flask import flash

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    correctness = session.get('correctness', {})
    user_answers = session.get('user_answers', {})
    user_id = session.get('user_id')

    if isinstance(correctness, list):
        correctness = dict(correctness)

    wrong_q_ids = []
    for qid, correct in correctness.items():
        if not correct:
            wrong_q_ids.append(qid)

    session['wrong_q_ids'] = wrong_q_ids

    reflected_qids = [log['qid'] for log in user_logs.get(user_id, {}).get('tags', [])]
    unreflected_qids = [qid for qid in wrong_q_ids if qid not in reflected_qids]
    session['unreflected_qids'] = unreflected_qids

    if request.method == 'POST':
        print("Submitted form data:", request.form)
        qid = request.form.get('question_id')

        if qid:
            try:
                qid = int(qid)
            except ValueError:
                flash("Invalid question number", "danger")
                return redirect(url_for('evaluate'))

            if qid in wrong_q_ids:
                session['selected_qid'] = qid

                session['answers'] = []
                session['style'] = request.form.get('style', 'neutral')

                return redirect(url_for('reflect'))
            else:
                flash("Question not found", "danger")
        else:
            flash("Please select a question to reflect on", "warning")


    wrong_questions = []
    for qid in wrong_q_ids:
        q = next(q for q in preloaded_questions if q['id'] == qid)
        q['user_answer'] = user_answers.get(qid, '未作答')
        wrong_questions.append(q)

    return render_template('evaluate.html', wrong_questions=wrong_questions)


@app.route('/my_mistakes')
def my_mistakes():
    user_id = session.get('user_id')
    unreflected_qids = session.get('unreflected_qids', [])
    mistakes = []
    for qid in unreflected_qids:
        question = next((q for q in preloaded_questions if q['id'] == qid), None)
        if question:
            mistakes.append(question)
    return render_template('my_mistakes.html', mistakes=mistakes)



@app.route('/my_reflections')
def my_reflections():
    user_id = session.get('user_id')
    reflection_cases = []

    for qid, submissions in global_error_pool.items():
        for s in submissions:
            if s['user_id'] == user_id:

                original = next((q for q in preloaded_questions if q['id'] == qid), {})
                reflection_cases.append({
                    'qid': qid,
                    'question': s['question']['question'] if isinstance(s['question'], dict) else str(s['question']),
                    "question_detail": original.get("question_detail"),
                    "options": original.get("options"),
                    'tags': s.get('tags', [])
                })

    return render_template('my_reflections.html', cases=reflection_cases)




@app.route('/reflect', methods=['GET', 'POST'])
def reflect():
    qid = session.get('selected_qid')
    if not qid:
        flash("You Have Not Selected The Quiz", "warning")
        return redirect(url_for('evaluate'))

    question = next((q for q in preloaded_questions if q['id'] == qid), None)
    if not question:
        flash("Cannot Find The Quiz", "danger")
        return redirect(url_for('evaluate'))

    # Initialize chat history
    if 'chat_history' not in session:
        session['chat_history'] = [{"role": "system", "content": system_prompt}]
        session['answers'] = []

    if request.method == 'POST':
        user_msg = request.form.get('msg', '').strip()
        if user_msg:
            session['chat_history'].append({"role": "user", "content": user_msg})
            session['answers'].append(user_msg)

            if "ready for summary" in user_msg.lower():
                session['summary_ready'] = True
                return redirect(url_for('generate_summary'))

            try:
                print("Chat history being sent to GPT:", session['chat_history'])

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=session['chat_history'],
                    temperature=0.7,
                    max_tokens = 500
                )
                print ("GPT Response object:", response)



                gpt_reply = response.choices[0].message.content.strip()

                session["chat_history"].append({"role": "assistant", "content": gpt_reply})

                user_logs.setdefault(session['user_id'], {}).setdefault("reflections", []).append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "qid": qid,
                    "steps": [{
                        "step_title": "LLM Reflection",
                        "input": user_msg,
                        "llm_response": gpt_reply
                    }]
                })


            except Exception as e:
                print("❌ OpenAI error:", e)
                flash("There was an error contacting GPT. Check the server logs.", "danger")

    return render_template('reflect_chat.html',
                           chat_history=session['chat_history'],
                           quiz=question)





@app.route('/summary', methods=['GET', 'POST'])
def summary():
    user_id = session.get('user_id')
    qid = session.get('selected_qid')
    chat_history = session.get('chat_history', [])

    latest_reflection = request.form.get('latest_reflection', '').strip()


    # Append new user reflection to chat history if not already present
    if latest_reflection and all(latest_reflection != m["content"] for m in chat_history if m["role"] == "user"):
        chat_history.append({"role": "user", "content": latest_reflection})

    # Prompt for GPT to summarize and extract tags
    system_prompt_summary = {
        "role": "system",
        "content": (
            "You are a reflective assistant. The student has just finished discussing a problem-solving mistake. "
            "Please write a clear summary of what likely caused their error, and then list 3 to 6 possible root causes "
            "as bullet points, each on its own line. Use this exact format:\n\n"
            "Summary:\n[Your summary here]\n\n"
            "Tags:\n- Cause 1\n- Cause 2\n- Cause 3\n..."
            "You must combine two principles:\n\n"
            "In-context learning: learn how to write the summary and tags by following the provided example below.\n"
            "Context-aware reasoning: always adapt your response using the actual student statement given, not generic assumptions.\n\n"
            "Here is an example:\n"
            "Student's statement: 'I forgot to check the loop condition so my code ran forever.'\n\n"
            "Summary:\n"
            "The student’s mistake was caused by overlooking the need to verify the loop’s exit condition, which led to an infinite loop.\n\n"
            "Tags:\n"
            "- Missing loop condition check\n"
            "- Weak debugging strategy\n"
            "- Incomplete planning\n\n"
            "When you generate your answer, always:\n"
            "- Use only what the student actually said.\n"
            "- Use the example as your guide (in-context learning).\n"
            "- Connect the student’s statement to possible root causes.\n"
            "- Keep the format exactly the same."
        )
    }

    prompt_messages = [system_prompt_summary] + [
        m for m in chat_history if m["role"] == "user"
    ]

    # Default outputs
    summary_text = ""
    tag_suggestions = []


    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt_messages,
            temperature=0.7,
            max_tokens = 500
        )
        gpt_output = response.choices[0].message.content.strip()
        print("GPT output:", gpt_output)

        # Extract summary and tags from GPT output
        if "Tags:" in gpt_output:
            summary_text, tag_part = gpt_output.split("Tags:", 1)
            summary_text = summary_text.replace("Summary:", "").strip()
            tag_suggestions = [
                line.strip("- ").strip()
                for line in tag_part.strip().splitlines()
                if line.strip()
            ]







        else:
            summary_text = gpt_output.strip()

    except Exception as e:
        print("❌ GPT error:", e)
        flash("GPT summary generation failed.", "danger")
        summary_text = "GPT failed to generate a summary."
        tag_suggestions = []

    return render_template(
        'summary.html',
        summary=summary_text,
        tag_suggestions=tag_suggestions,
        selected_tags=[]
    )






@app.route('/mistakes')
@app.route('/mistakes')
def mistakes():
    filter_qid = request.args.get("filter_qid")
    min_submit = request.args.get("min_submit", type=int)

    mistake_summary = {}

    for qid, submissions in global_error_pool.items():
        if filter_qid and str(qid) != filter_qid:
            continue
        if min_submit and len(submissions) < min_submit:
            continue


        question_obj = submissions[0]['question']
        if isinstance(question_obj, dict):
            question_text = question_obj['question']
        else:
            question_text = str(question_obj)


        original = next((q for q in preloaded_questions if q['id'] == qid), {})

        flat_tags = []
        for s in submissions:
            flat_tags.extend(s.get("tags", []))
        tag_counter = Counter(flat_tags)

        mistake_summary[qid] = {
            'question': question_text,
            'question_detail': original.get("question_detail"),
            'solution_img': original.get("solution_img"),
            'options': original.get("options"),
            'times': len(submissions),
            'tag_summary': tag_counter,
            'messages': global_comments.get(qid, [])
        }

    return render_template(
        'mistake_book.html',
        mistake_summary=mistake_summary,
        filter_qid=filter_qid,
        min_submit=min_submit
    )





@app.route('/submit_summary', methods=['POST'])
def submit_summary():
    user_id = session.get('user_id')
    qid = session.get('selected_qid')
    summary_text = request.form.get('summary_text', '').strip()
    selected_tags = request.form.getlist("selected_tags")
    latest_reflection = request.form.get("latest_reflection", "").strip()

    question = next((q for q in preloaded_questions if q['id'] == qid), None)

    if question:
        global_error_pool.setdefault(qid, [])
        global_error_pool[qid].append({
            "user_id": user_id,
            "question": question,
            "summary": summary_text,
            "tags": selected_tags
        })

        user_logs.setdefault(user_id, {}).setdefault("tags", []).append({
            "timestamp": datetime.datetime.now().isoformat(),
            "qid": qid,
            "suggested": [],
            "selected": selected_tags
        })

        user_logs[user_id].setdefault("reflections", []).append({
            "timestamp": datetime.datetime.now().isoformat(),
            "qid": qid,
            "steps": [{
                "step_title": "Final Summary",
                "input": latest_reflection,
                "llm_response": summary_text
            }]
        })
        unreflected = session.get('unreflected_qids', [])
        if qid in unreflected:
            unreflected.remove(qid)
            session['unreflected_qids'] = unreflected

    return redirect(url_for('mistakes'))







@app.route('/comment_on_mistake/<int:qid>', methods=['POST'])
def comment_on_mistake(qid):
    comment = request.form.get('comment', '').strip()
    print(f"[DEBUG] Received comment for qid={qid}: {comment}")

    if comment:
        uid = session.get('user_id')
        if uid not in user_logs:
            user_logs[uid] = {}
        if 'comments' not in user_logs[uid]:
            user_logs[uid]['comments'] = []

        global_comments[qid].append({
            'text': comment,
            'likes': 0,
            'replies': []
        })
        user_logs[uid]['comments'].append({
            'timestamp': datetime.datetime.now().isoformat(),
            'qid': qid,
            'comment': comment
        })




    return redirect(url_for('mistakes', filter_qid=qid))


def log_user_action(user_id, action_type, entry):
    user_logs.setdefault(user_id, {}).setdefault(action_type, []).append(entry)


@app.route('/like_comment/<int:qid>/<int:cid>', methods=['POST'])
def like_comment(qid, cid):
    if 0 <= cid < len(global_comments[qid]):
        global_comments[qid][cid]['likes'] += 1
        log_user_action(session['user_id'], 'likes', {
            'timestamp': datetime.datetime.now().isoformat(),
            'qid': qid,
            'cid': cid
        })

    return redirect(url_for('mistakes', filter_qid=qid))



@app.route('/reply_to_comment/<int:qid>/<int:cid>', methods=['POST'])
def reply_to_comment(qid, cid):
    reply = request.form.get('reply', '').strip()
    if reply and 0 <= cid < len(global_comments[qid]):
        global_comments[qid][cid]['replies'].append(reply)
        user_logs.setdefault(session['user_id'], {}).setdefault('replies', []).append({
            "timestamp": datetime.datetime.now().isoformat(),
            "qid": qid,
            "reply": reply
        })

    return redirect(url_for('mistakes', filter_qid=qid))


from flask import Response, send_file, session

@app.route('/admin/save_and_download_logs')
def save_and_download_logs():
    if not session.get('is_admin'):
        return "Unauthorized", 403

    import json, os
    os.makedirs("data", exist_ok=True)
    with open("data/user_logs.json", "w", encoding="utf-8") as f:
        json.dump(user_logs, f, indent=2)

    return send_file('data/user_logs.json',
                     mimetype='application/json',
                     as_attachment=True,
                     download_name='user_logs.json')



def main():
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main()
