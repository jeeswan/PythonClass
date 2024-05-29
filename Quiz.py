questions = [
    {
        "question": "What is the output of 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": 2,
    },
    {
        "question": "Which of the following is a mutable data type in Python?",
        "options": ["Tuple", "List", "Set", "Dictionary"],
        "correct_answer": 2,
    },
    {
        "question": "What is the syntax for a for loop in Python?",
        "options": ["for i in range(10)", "for i = 0; i < 10; i++", "for i = 0 to 10", "for i = 0; i <= 10; i++"],
        "correct_answer": 1,
    },
    {
        "question": "Which statement is used to exit a loop in Python?",
        "options": ["break", "continue", "return", "exit"],
        "correct_answer": 1,
    },
    {
        "question": "What is the result of {(1, 2), (2, 3), (3, 4)}?",
        "options": ["{1, 2, 3, 4}", "{(1, 2), (2, 3), (3, 4)}", "{(1, 2), (2, 3), (3, 4)}", "{1, 2}"],
        "correct_answer": 2,
    }
]

score = 0
for q in questions:
    print(q["question"])
    options = q["options"]
    for i in range(len(options)):
        print(f"{i + 1}. {options[i]}")
    choice = int(input("Enter your choice (1, 2, 3, or 4): "))
    if choice == q["correct_answer"]:
        print("Correct!")
        score += 1
    else:
        print("Incorrect!")

print(f"\nYour final score is: {score}/{len(questions)}")
