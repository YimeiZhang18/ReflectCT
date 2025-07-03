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