from cognitive_assessment.chat_assessment import ChatBasedAssessment
from cognitive_profiling.cognitive_profiler import CognitiveProfileGenerator
from llm_integration.reasoning_engine import ReasoningEngine
import pprint

def run_cli():
    assessment = ChatBasedAssessment()
    profiler = CognitiveProfileGenerator()
    
    print("Welcome to Cognitive AI Clone CLI\n")
    
    # Personality chat loop
    while True:
        question = assessment.get_next_personality_question()
        if not question:
            print("\nPersonality Chat complete.\n")
            break
        print(f"AI: {question}")
        answer = input("Your response: ")
        assessment.submit_personality_response(answer)
    
    personality_profile = assessment.generate_personality_profile()
    print("\nGenerated personality profile:")
    pprint.pprint(personality_profile)
    
    print("\nStarting Problem Solving Scenarios...\n")
    # Problem-solving scenario loop
    while True:
        scenario = assessment.get_next_problem_scenario()
        if not scenario:
            print("\nProblem-solving assessment complete.\n")
            break
        print(f"AI Problem Scenario:\n{scenario['scenario']}")
        while True:
            user_input = input("Your approach (or 'next' to go to next scenario): ")
            if user_input.strip().lower() == 'next':
                break
            assessment.submit_problem_solving_response(user_input, scenario['type'])
            follow_up = assessment.generate_problem_solving_follow_up(user_input, scenario)
            print(f"AI Follow-up: {follow_up}")
    
    problem_solving_profile = assessment.generate_problem_solving_profile()
    print("\nGenerated problem solving profile:")
    pprint.pprint(problem_solving_profile)
    
    # Combine results and generate cognitive profile
    full_profile = profiler.generate_comprehensive_profile({
        "personality": personality_profile,
        "problem_solving": problem_solving_profile,
        # Optionally add conversation logs if implemented
    })
    
    print("\nYour complete cognitive profile:")
    pprint.pprint(full_profile)
    
    # Create reasoning engine and chat
    engine = ReasoningEngine(full_profile)
    
    print("\nStart chatting with your cognitive clone (type 'exit' to stop):\n")
    while True:
        prompt = input("You: ")
        if prompt.lower() in ['exit', 'quit']:
            print("Ending session.")
            break
        response = engine.reason_about_problem(prompt)
        print(f"Clone: {response['response']}\n")

if __name__ == '__main__':
    run_cli()
