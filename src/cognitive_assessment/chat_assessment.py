import time
from datetime import datetime
import random
import spacy
from typing import Dict, List, Any, Optional
from textstat import flesch_reading_ease
import pandas as pd
import json
import re


def load_nlp_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        print("Please install spaCy English model: python -m spacy download en_core_web_sm")
        return None


class ChatBasedAssessment:
    def __init__(self):
        self.nlp = load_nlp_model()
        self.conversation_history = []
        self.behavioral_data = []
        self.session_start = time.time()

        # Personality chat state
        self.personality_chat_stage = 0
        self.personality_responses = {}
        self.personality_chat_history = []

        # Problem-solving chat state
        self.problem_chat_stage = 0
        self.problem_responses = {}
        self.problem_chat_history = []

        # Cognitive indicators
        self.analytical_patterns = [
            'first', 'second', 'third', 'next', 'then', 'therefore', 'because',
            'analyze', 'break down', 'step by step', 'systematic', 'logical',
            'evidence', 'data', 'facts', 'research', 'study', 'examine',
            'consider', 'evaluate', 'assess', 'measure', 'compare'
        ]

        self.intuitive_patterns = [
            'feel', 'sense', 'instinct', 'gut', 'intuition', 'seems like',
            'appears', 'impression', 'hunch', 'vibe', 'energy', 'flow',
            'natural', 'organic', 'spontaneous', 'instinctively', 'naturally'
        ]

        self.creative_patterns = [
            'imagine', 'what if', 'brainstorm', 'creative', 'innovative',
            'outside the box', 'alternative', 'unconventional', 'novel',
            'original', 'unique', 'artistic', 'inspiration', 'envision'
        ]

        self.systematic_patterns = [
            'process', 'procedure', 'method', 'approach', 'framework',
            'structure', 'organize', 'plan', 'schedule', 'timeline',
            'phases', 'stages', 'sequence', 'order', 'prioritize'
        ]

        # Personality stages
        self.chat_stages = [
            {
                'question': "Hi! Let's start with something I'm curious about. When you have free time, what kind of activities do you naturally gravitate toward? What draws you to spend your time that way?",
                'follow_ups': [
                    "That's interesting! What specifically do you enjoy about those activities?",
                    "How do you usually decide what to do when you have multiple options?"
                ],
                'trait_focus': 'openness'
            },
            {
                'question': "Now I'm curious about how you approach work or projects. When you start something new, what's your typical process? Walk me through how you like to tackle things.",
                'follow_ups': [
                    "Do you prefer to plan everything out first, or do you like to dive in and figure it out as you go?",
                    "How do you handle deadlines and time pressure?"
                ],
                'trait_focus': 'conscientiousness'
            },
            {
                'question': "Tell me about a recent situation where you had to work with other people - maybe at work, in a group project, or even planning something with friends. How did that experience go for you?",
                'follow_ups': [
                    "Do you usually prefer to take the lead, or do you like collaborating as an equal partner?",
                    "How do you handle it when people have different opinions or approaches?"
                ],
                'trait_focus': 'extraversion'
            },
            {
                'question': "When there's conflict or disagreement - whether it's at work, with friends, or even in online discussions - what's your natural response? How do you typically handle those situations?",
                'follow_ups': [
                    "How important is it to you that everyone gets along and feels heard?",
                    "Do you generally trust people's intentions, or do you tend to be more cautious?"
                ],
                'trait_focus': 'agreeableness'
            },
            {
                'question': "Let's talk about stress and pressure. Think of a recent time when you felt overwhelmed or stressed. How did you handle it? What goes through your mind in those moments?",
                'follow_ups': [
                    "What strategies do you use to cope when things get tough?",
                    "Do you find yourself worrying about things that might go wrong?"
                ],
                'trait_focus': 'neuroticism'
            }
        ]

        # Problem-solving scenarios
        self.problem_scenarios = [
            {
                'title': 'Project Management Challenge',
                'scenario': """You're managing a team project that's running behind schedule. The deadline is in two weeks, and you've just discovered that a key team member will be unavailable for the next week due to a family emergency. The project involves both technical development and client coordination. How would you handle this situation?""",
                'type': 'management',
                'follow_ups': [
                    "What would be your very first action in this situation?",
                    "How would you balance supporting your team member while meeting the deadline?",
                    "How would you communicate this setback to stakeholders?"
                ]
            },
            {
                'scenario': """Your company is considering launching a new product. Market research shows promising demand in one segment but concerning feedback from another key demographic. The financial projections are positive, but the timeline is aggressive. You need to make a recommendation to the leadership team. How would you approach this decision?""",
                'type': 'analytical',
                'follow_ups': [
                    "What additional information would you want before making this decision?",
                    "How would you weigh the conflicting market signals?",
                    "What factors would be most important in your final recommendation?"
                ]
            },
            {
                'scenario': """You need to design a solution that makes remote work more engaging and productive for a diverse team - some are highly social and miss office interaction, while others are introverted and prefer focused solo work. The budget is flexible, and you have creative freedom. What would you propose?""",
                'type': 'creative',
                'follow_ups': [
                    "How would you ensure your solution works for both personality types?",
                    "What would be your process for developing and testing this solution?",
                    "How would you measure success?"
                ]
            }
        ]

    # Personality CLI interaction methods
    def get_next_personality_question(self) -> Optional[str]:
        if self.personality_chat_stage < len(self.chat_stages):
            stage_data = self.chat_stages[self.personality_chat_stage]
            assistant_msgs = [m for m in self.personality_chat_history if m['role'] == 'assistant' and m['stage'] == self.personality_chat_stage]
            if not assistant_msgs:
                return stage_data['question']
            else:
                user_msgs = [m for m in self.personality_chat_history if m['role'] == 'user' and m['stage'] == self.personality_chat_stage]
                if len(user_msgs) == 1:
                    return stage_data['follow_ups'][0]
                elif len(user_msgs) == 2:
                    self.personality_chat_stage += 1
                    return self.get_next_personality_question()
                else:
                    return None
        else:
            return None

    def submit_personality_response(self, user_response: str):
        current_stage = self.personality_chat_stage
        stage_data = self.chat_stages[current_stage]
        response_time = time.time()
        response_data = self.analyze_response(user_response, stage_data['trait_focus'])

        self.personality_chat_history.append({
            'role': 'user',
            'content': user_response,
            'timestamp': response_time,
            'stage': current_stage,
            'trait_focus': stage_data['trait_focus'],
            'analysis': response_data
        })

        if stage_data['trait_focus'] not in self.personality_responses:
            self.personality_responses[stage_data['trait_focus']] = []
        self.personality_responses[stage_data['trait_focus']].append(response_data)

    # Problem solving CLI interaction methods
    def get_next_problem_scenario(self) -> Optional[Dict[str, Any]]:
        if self.problem_chat_stage < len(self.problem_scenarios):
            scenario = self.problem_scenarios[self.problem_chat_stage]
            assistant_msgs = [m for m in self.problem_chat_history if m['role'] == 'assistant' and m.get('scenario_index') == self.problem_chat_stage]
            if not assistant_msgs:
                return scenario
            else:
                user_msgs = [m for m in self.problem_chat_history if m['role'] == 'user' and m.get('scenario_index') == self.problem_chat_stage]
                if len(user_msgs) >= 3:
                    self.problem_chat_stage += 1
                    return self.get_next_problem_scenario()
                else:
                    return None
        else:
            return None

    def submit_problem_solving_response(self, user_response: str, scenario_type: str):
        response_data = self.analyze_problem_solving_response(user_response, scenario_type)
        self.problem_chat_history.append({
            'role': 'user',
            'content': user_response,
            'timestamp': time.time(),
            'scenario_index': self.problem_chat_stage,
            'analysis': response_data
        })

        if scenario_type not in self.problem_responses:
            self.problem_responses[scenario_type] = {
                'scenario': self.problem_scenarios[self.problem_chat_stage],
                'responses': [],
                'analysis_summary': None
            }
        self.problem_responses[scenario_type]['responses'].append(self.problem_chat_history[-1])
        self.problem_responses[scenario_type]['analysis_summary'] = response_data

    def analyze_response(self, text: str, context: str) -> Dict[str, Any]:
        """Analyze text response for cognitive and personality indicators."""
        if not self.nlp:
            return {'error': 'NLP model not loaded'}
        
        doc = self.nlp(text)
        
        analysis = {
            'text': text,
            'timestamp': time.time(),
            'context': context,
            'length': len(text),
            'word_count': len(text.split()),
            'sentence_count': len(list(doc.sents)),
            'avg_sentence_length': len(text.split()) / max(len(list(doc.sents)), 1),
            'complexity_score': flesch_reading_ease(text),
            'question_count': text.count('?'),
            'exclamation_count': text.count('!'),
            'uncertainty_words': self.count_uncertainty_words(text),
            'analytical_indicators': self.count_pattern_matches(text, self.analytical_patterns),
            'intuitive_indicators': self.count_pattern_matches(text, self.intuitive_patterns),
            'creative_indicators': self.count_pattern_matches(text, self.creative_patterns),
            'systematic_indicators': self.count_pattern_matches(text, self.systematic_patterns),
            'personal_pronouns': self.count_personal_pronouns(doc),
            'emotion_words': self.count_emotion_words(text),
            'certainty_level': self.assess_certainty_level(text)
        }
        
        return analysis

    def analyze_problem_solving_response(self, text: str, problem_type: str) -> Dict[str, Any]:
        """Analyze problem-solving response for cognitive patterns."""
        base_analysis = self.analyze_response(text, problem_type)
        
        # Additional problem-solving specific analysis
        problem_solving_indicators = {
            'solution_orientation': self.count_solution_words(text),
            'process_orientation': self.count_process_words(text),
            'stakeholder_awareness': self.count_stakeholder_references(text),
            'risk_awareness': self.count_risk_words(text),
            'resource_consideration': self.count_resource_words(text),
            'time_orientation': self.count_time_references(text),
            'collaboration_indicators': self.count_collaboration_words(text),
            'implementation_focus': self.count_implementation_words(text)
        }
        
        base_analysis.update(problem_solving_indicators)
        return base_analysis

    def count_pattern_matches(self, text: str, patterns: List[str]) -> int:
        """Count matches for given patterns in text."""
        text_lower = text.lower()
        count = 0
        for pattern in patterns:
            if pattern in text_lower:
                count += 1
        return count

    def count_uncertainty_words(self, text: str) -> int:
        """Count uncertainty expressions."""
        uncertainty_words = ['maybe', 'perhaps', 'possibly', 'might', 'could', 
                            'probably', 'likely', 'uncertain', 'unsure', 'guess']
        return sum(1 for word in uncertainty_words if word in text.lower())

    def count_personal_pronouns(self, doc) -> int:
        """Count personal pronouns using spaCy."""
        personal_pronouns = ['i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours']
        return sum(1 for token in doc if token.text.lower() in personal_pronouns)

    def count_emotion_words(self, text: str) -> int:
        """Count emotional expressions."""
        emotion_words = ['feel', 'excited', 'worried', 'happy', 'sad', 'angry', 
                        'frustrated', 'confident', 'nervous', 'passionate', 'enjoy',
                        'love', 'hate', 'fear', 'hope', 'concerned', 'pleased']
        return sum(1 for word in emotion_words if word in text.lower())

    def assess_certainty_level(self, text: str) -> str:
        """Assess overall certainty level of the response."""
        certain_words = ['definitely', 'certainly', 'absolutely', 'sure', 'confident', 'always', 'never']
        uncertain_words = ['maybe', 'perhaps', 'possibly', 'might', 'could', 'sometimes', 'usually']
        
        certain_count = sum(1 for word in certain_words if word in text.lower())
        uncertain_count = sum(1 for word in uncertain_words if word in text.lower())
        
        if certain_count > uncertain_count:
            return 'high'
        elif uncertain_count > certain_count:
            return 'low'
        else:
            return 'medium'

    def count_solution_words(self, text: str) -> int:
        """Count solution-oriented language."""
        solution_words = ['solve', 'solution', 'fix', 'resolve', 'address', 'handle', 'deal with', 'tackle']
        return sum(1 for word in solution_words if word in text.lower())

    def count_process_words(self, text: str) -> int:
        """Count process-oriented language."""
        process_words = ['step', 'process', 'approach', 'method', 'way', 'how', 'procedure']
        return sum(1 for word in process_words if word in text.lower())

    def count_stakeholder_references(self, text: str) -> int:
        """Count stakeholder awareness."""
        stakeholder_words = ['team', 'people', 'stakeholder', 'client', 'customer', 'user', 'others', 'everyone']
        return sum(1 for word in stakeholder_words if word in text.lower())

    def count_risk_words(self, text: str) -> int:
        """Count risk awareness language."""
        risk_words = ['risk', 'danger', 'problem', 'issue', 'challenge', 'difficulty', 'obstacle', 'concern']
        return sum(1 for word in risk_words if word in text.lower())

    def count_resource_words(self, text: str) -> int:
        """Count resource consideration."""
        resource_words = ['time', 'money', 'budget', 'resource', 'cost', 'effort', 'energy', 'capacity']
        return sum(1 for word in resource_words if word in text.lower())

    def count_time_references(self, text: str) -> int:
        """Count time-oriented thinking."""
        time_words = ['deadline', 'schedule', 'timeline', 'urgent', 'priority', 'quick', 'slow', 'immediate']
        return sum(1 for word in time_words if word in text.lower())

    def count_collaboration_words(self, text: str) -> int:
        """Count collaborative language."""
        collab_words = ['together', 'collaborate', 'teamwork', 'cooperation', 'partnership', 'joint', 'shared']
        return sum(1 for word in collab_words if word in text.lower())

    def count_implementation_words(self, text: str) -> int:
        """Count implementation-focused language."""
        impl_words = ['implement', 'execute', 'deploy', 'build', 'create', 'develop', 'action', 'do']
        return sum(1 for word in impl_words if word in text.lower())

    def generate_intelligent_follow_up(self, response: str, stage_data: Dict, analysis: Dict) -> str:
        """Generate intelligent follow-up questions based on response analysis."""
        
        # Analyze the dominant cognitive style in the response
        analytical_score = analysis.get('analytical_indicators', 0)
        intuitive_score = analysis.get('intuitive_indicators', 0)
        creative_score = analysis.get('creative_indicators', 0)
        
        trait_focus = stage_data['trait_focus']
        follow_ups = stage_data['follow_ups']
        
        # Choose follow-up based on response characteristics
        if analytical_score > intuitive_score and analytical_score > creative_score:
            # Analytical response - probe for intuitive/emotional aspects
            if trait_focus == 'neuroticism':
                return "You have a very systematic approach to stress. How do you factor in your emotions or gut feelings when you're under pressure?"
            elif trait_focus == 'agreeableness':
                return "That's a logical way to handle conflict. How important are your personal feelings about the people involved in these situations?"
            else:
                return random.choice(follow_ups)
        elif intuitive_score > analytical_score:
            # Intuitive response - probe for analytical aspects  
            if trait_focus == 'conscientiousness':
                return "I can hear that you trust your instincts about projects. How do you balance that with concrete planning and organization?"
            else:
                return "That's a very intuitive response. What concrete steps or processes help you turn those insights into action?"
        elif creative_score > 2:
            # Creative response - explore implementation
            return "Those are some creative approaches! How do you typically move from creative ideas to practical implementation?"
        else:
            # Default to scenario-specific follow-up
            return follow_ups[0] if follow_ups else "Can you tell me more about that?"

    def generate_problem_solving_follow_up(self, response: str, scenario: Dict, analysis: Dict, response_count: int) -> str:
        """Generate follow-up for problem-solving scenarios."""
        
        scenario_type = scenario['type']
        follow_ups = scenario.get('follow_ups', [])
        
        if response_count == 1:  # First follow-up
            if follow_ups:
                return follow_ups[0]
            
            # Generate based on analysis
            solution_focus = analysis.get('solution_orientation', 0)
            process_focus = analysis.get('process_orientation', 0)
            
            if solution_focus > process_focus:
                return "You seem very solution-focused. Can you walk me through the process you'd use to get there?"
            else:
                return "That's a thoughtful process. What would success look like in this situation?"
        
        elif response_count == 2:  # Second follow-up
            if len(follow_ups) > 1:
                return follow_ups[1]
            
            stakeholder_awareness = analysis.get('stakeholder_awareness', 0)
            if stakeholder_awareness > 0:
                return "How would you ensure all stakeholders stay aligned throughout this process?"
            else:
                return "Who else would need to be involved in implementing this approach?"
        
        else:  # Final question
            return "Is there anything else you'd want to consider or prepare for in this situation?"

    def generate_personality_profile(self) -> Dict[str, Any]:
        """Generate personality profile from chat responses."""
        responses = self.personality_responses
        all_analyses = []
        
        # Collect all analysis data
        for trait_responses in responses.values():
            all_analyses.extend(trait_responses)
        
        if not all_analyses:
            return None
        
        # Analyze patterns across all responses
        total_analytical = sum(a.get('analytical_indicators', 0) for a in all_analyses)
        total_intuitive = sum(a.get('intuitive_indicators', 0) for a in all_analyses)
        total_creative = sum(a.get('creative_indicators', 0) for a in all_analyses)
        total_systematic = sum(a.get('systematic_indicators', 0) for a in all_analyses)
        
        # Calculate averages
        num_responses = len(all_analyses)
        avg_analytical = total_analytical / num_responses
        avg_intuitive = total_intuitive / num_responses  
        avg_creative = total_creative / num_responses
        avg_systematic = total_systematic / num_responses
        
        # Determine primary thinking style
        max_score = max(avg_analytical, avg_intuitive, avg_creative)
        if max_score == avg_analytical:
            primary_style = 'analytical'
        elif max_score == avg_intuitive:
            primary_style = 'intuitive'
        elif max_score == avg_creative:
            primary_style = 'creative'
        else:
            primary_style = 'balanced'
        
        # Calculate other metrics
        avg_certainty = sum(1 for a in all_analyses if a.get('certainty_level') == 'high') / num_responses
        avg_emotion = sum(a.get('emotion_words', 0) for a in all_analyses) / num_responses
        avg_word_count = sum(a.get('word_count', 0) for a in all_analyses) / num_responses
        avg_questions = sum(a.get('question_count', 0) for a in all_analyses) / num_responses
        
        profile = {
            'primary_thinking_style': primary_style,
            'analytical_tendency': avg_analytical,
            'intuitive_tendency': avg_intuitive,
            'creative_tendency': avg_creative,
            'systematic_tendency': avg_systematic,
            'certainty_level': avg_certainty,
            'emotional_expression': avg_emotion,
            'communication_style': self.determine_communication_style(all_analyses),
            'response_patterns': self.identify_response_patterns(all_analyses),
            'avg_response_length': avg_word_count,
            'question_frequency': avg_questions,
            'generation_timestamp': datetime.now().isoformat()
        }
        
        return profile

    def generate_problem_solving_profile(self) -> Dict[str, Any]:
        """Generate problem-solving profile from scenarios."""
        responses = self.problem_responses
        all_analyses = []
        
        # Collect analysis data from all scenarios
        for response_data in responses.values():
            if 'responses' in response_data:
                for resp in response_data['responses']:
                    if 'analysis' in resp:
                        all_analyses.append(resp['analysis'])
        
        if not all_analyses:
            return None
        
        # Aggregate analysis across scenarios  
        num_analyses = len(all_analyses)
        
        solution_focus = sum(a.get('solution_orientation', 0) for a in all_analyses) / num_analyses
        process_focus = sum(a.get('process_orientation', 0) for a in all_analyses) / num_analyses
        stakeholder_awareness = sum(a.get('stakeholder_awareness', 0) for a in all_analyses) / num_analyses
        risk_awareness = sum(a.get('risk_awareness', 0) for a in all_analyses) / num_analyses
        collaboration_tendency = sum(a.get('collaboration_indicators', 0) for a in all_analyses) / num_analyses
        implementation_focus = sum(a.get('implementation_focus', 0) for a in all_analyses) / num_analyses
        
        profile = {
            'problem_solving_style': 'solution-focused' if solution_focus > process_focus else 'process-focused',
            'stakeholder_orientation': 'high' if stakeholder_awareness > 1.5 else 'medium' if stakeholder_awareness > 0.5 else 'low',
            'risk_assessment': 'high' if risk_awareness > 1.5 else 'medium' if risk_awareness > 0.5 else 'low',
            'collaboration_tendency': 'high' if collaboration_tendency > 1.5 else 'medium' if collaboration_tendency > 0.5 else 'low',
            'implementation_focus': 'high' if implementation_focus > 1.5 else 'medium' if implementation_focus > 0.5 else 'low',
            'decision_making_speed': self.assess_decision_speed(all_analyses),
            'complexity_comfort': self.assess_complexity_comfort(all_analyses),
            'generation_timestamp': datetime.now().isoformat()
        }
        
        return profile

    def determine_communication_style(self, analyses: List[Dict]) -> str:
        """Determine communication style from analyses."""
        avg_length = sum(a.get('word_count', 0) for a in analyses) / len(analyses)
        avg_questions = sum(a.get('question_count', 0) for a in analyses) / len(analyses)
        
        if avg_length > 75 and avg_questions > 1:
            return 'detailed_inquisitive'
        elif avg_length > 75:
            return 'detailed_explanatory'
        elif avg_questions > 1:
            return 'concise_inquisitive'
        else:
            return 'concise_direct'

    def identify_response_patterns(self, analyses: List[Dict]) -> List[str]:
        """Identify consistent patterns across responses."""
        patterns = []
        
        # Check for consistency in analytical thinking
        analytical_scores = [a.get('analytical_indicators', 0) for a in analyses]
        if all(score > 0 for score in analytical_scores):
            patterns.append('consistently_analytical')
        
        # Check for emotional awareness
        emotion_scores = [a.get('emotion_words', 0) for a in analyses]
        if sum(emotion_scores) > len(analyses):
            patterns.append('emotionally_aware')
        
        # Check for systematic thinking
        systematic_scores = [a.get('systematic_indicators', 0) for a in analyses]
        if sum(systematic_scores) > len(analyses):
            patterns.append('systematic_thinker')
        
        # Check for creative language
        creative_scores = [a.get('creative_indicators', 0) for a in analyses]
        if sum(creative_scores) > len(analyses) * 0.5:
            patterns.append('creative_thinker')
        
        return patterns

    def assess_decision_speed(self, analyses: List[Dict]) -> str:
        """Assess decision-making speed from response patterns."""
        avg_length = sum(len(a.get('text', '')) for a in analyses) / len(analyses)
        return 'deliberate' if avg_length > 300 else 'quick'

    def assess_complexity_comfort(self, analyses: List[Dict]) -> str:
        """Assess comfort with complexity."""
        complexity_scores = [a.get('complexity_score', 50) for a in analyses]
        avg_complexity = sum(complexity_scores) / len(complexity_scores)
        
        # Lower Flesch score = more complex text = higher comfort with complexity
        if avg_complexity < 50:
            return 'high'
        elif avg_complexity < 70:
            return 'medium'  
        else:
            return 'low'

    def display_personality_results(self, profile: Dict[str, Any]):
        """Display personality assessment results."""
        print("\n🧠 Your Personality Profile")
        print("=" * 50)
        
        print(f"Primary Thinking Style: {profile['primary_thinking_style'].title()}")
        print(f"Communication Style: {profile['communication_style'].replace('_', ' ').title()}")
        print(f"Certainty Level: {profile['certainty_level']:.1%}")
        print(f"Analytical Tendency: {profile['analytical_tendency']:.1f}")
        print(f"Intuitive Tendency: {profile['intuitive_tendency']:.1f}")
        print(f"Creative Tendency: {profile['creative_tendency']:.1f}")
        
        # Response patterns
        if profile['response_patterns']:
            print("\n🔍 Identified Patterns:")
            for pattern in profile['response_patterns']:
                print(f"• {pattern.replace('_', ' ').title()}")

    def display_problem_solving_results(self, profile: Dict[str, Any]):
        """Display problem-solving assessment results."""
        print("\n🧩 Your Problem-Solving Profile")
        print("=" * 50)
        
        print(f"Problem-Solving Style: {profile['problem_solving_style'].replace('_', ' ').title()}")
        print(f"Stakeholder Orientation: {profile['stakeholder_orientation'].title()}")
        print(f"Risk Assessment: {profile['risk_assessment'].title()}")
        print(f"Collaboration Tendency: {profile['collaboration_tendency'].title()}")
        print(f"Decision Speed: {profile['decision_making_speed'].title()}")
        print(f"Complexity Comfort: {profile['complexity_comfort'].title()}")

    def run_personality_assessment(self):
        """Run the complete personality assessment via CLI."""
        print("🗣️ Personality Discovery Chat")
        print("Let's have a natural conversation to understand your personality and thinking style.\n")
        
        while self.personality_chat_stage < len(self.chat_stages):
            question = self.get_next_personality_question()
            if question:
                print(f"Assistant: {question}")
                user_response = input("You: ")
                self.submit_personality_response(user_response)
            else:
                break
        
        print("\n✅ Personality chat complete!")
        personality_profile = self.generate_personality_profile()
        if personality_profile:
            self.display_personality_results(personality_profile)
        return personality_profile

    def run_problem_solving_assessment(self):
        """Run the complete problem-solving assessment via CLI."""
        print("\n🧩 Problem-Solving Discovery")
        print("Let's explore how you approach and solve problems through interactive scenarios.\n")
        
        while self.problem_chat_stage < len(self.problem_scenarios):
            scenario = self.get_next_problem_scenario()
            if scenario:
                print(f"\nScenario {self.problem_chat_stage + 1}: {scenario.get('title', 'Problem-Solving Challenge')}")
                print(f"{scenario['scenario']}")
                print("\nAssistant: Take your time and walk me through how you'd approach this problem. What's your thinking process?")
                
                # Get multiple responses for this scenario
                response_count = 0
                while response_count < 3:
                    user_response = input("You: ")
                    self.submit_problem_solving_response(user_response, scenario['type'])
                    response_count += 1
                    
                    if response_count < 3:
                        follow_up = self.generate_problem_solving_follow_up(
                            user_response, scenario, 
                            self.problem_chat_history[-1]['analysis'], 
                            response_count
                        )
                        print(f"Assistant: {follow_up}")
                
                self.problem_chat_stage += 1
            else:
                break
        
        print("\n✅ Problem-solving assessment complete!")
        problem_solving_profile = self.generate_problem_solving_profile()
        if problem_solving_profile:
            self.display_problem_solving_results(problem_solving_profile)
        return problem_solving_profile


# Example usage
if __name__ == "__main__":
    assessment = ChatBasedAssessment()
    
    # Run personality assessment
    personality_profile = assessment.run_personality_assessment()
    
    # Run problem-solving assessment
    problem_solving_profile = assessment.run_problem_solving_assessment()
    
    # Save results to JSON
    results = {
        'personality_profile': personality_profile,
        'problem_solving_profile': problem_solving_profile,
        'session_data': {
            'start_time': assessment.session_start,
            'end_time': time.time(),
            'personality_chat_history': assessment.personality_chat_history,
            'problem_chat_history': assessment.problem_chat_history
        }
    }
    
    with open(f'assessment_results_{int(time.time())}.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Results saved to assessment_results_{int(time.time())}.json")
