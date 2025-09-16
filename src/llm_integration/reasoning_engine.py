import json
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np

class ReasoningEngine:
    """
    Reasoning engine that replicates individual cognitive patterns and thinking styles.
    This is a foundational implementation that can be enhanced with actual LLM integration.
    """
    
    def __init__(self, cognitive_profile: Dict[str, Any], clone_settings: Optional[Dict] = None):
        self.profile = cognitive_profile
        self.settings = clone_settings or {}
        self.response_history = []
        self.learning_data = []
        
        # Extract key cognitive characteristics
        self.cognitive_traits = cognitive_profile.get('cognitive_traits', {})
        self.communication_style = cognitive_profile.get('communication_style', {})
        self.decision_making = cognitive_profile.get('decision_making_profile', {})
        self.thinking_architecture = cognitive_profile.get('thinking_architecture', {})
        
        # Load reasoning templates based on cognitive style
        self.reasoning_templates = self._load_reasoning_templates()
        
        # Initialize response patterns
        self.response_patterns = self._initialize_response_patterns()
        
    def reason_about_problem(self, problem: str, complexity: str = "medium") -> Dict[str, Any]:
        """Generate a response to a problem using the individual's cognitive patterns."""
        
        # Analyze the problem to determine best approach
        problem_analysis = self._analyze_problem_characteristics(problem)
        
        # Select reasoning approach based on cognitive profile
        reasoning_approach = self._select_reasoning_approach(problem_analysis, complexity)
        
        # Generate reasoning steps
        reasoning_steps = self._generate_reasoning_steps(problem, reasoning_approach, complexity)
        
        # Generate the actual response
        response = self._generate_response(problem, reasoning_steps, reasoning_approach)
        
        # Add decision factors
        decision_factors = self._identify_decision_factors(problem, problem_analysis)
        
        # Calculate confidence
        confidence = self._calculate_confidence(problem, complexity, reasoning_approach)
        
        # Create response object
        result = {
            'problem': problem,
            'response': response,
            'reasoning_steps': reasoning_steps,
            'decision_factors': decision_factors,
            'reasoning_approach': reasoning_approach,
            'complexity': complexity,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat(),
            'cognitive_signature': self.profile.get('cognitive_signature', 'Unknown')
        }
        
        # Store in history for learning
        self.response_history.append(result)
        
        return result
    
    def _load_reasoning_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load reasoning templates based on cognitive profile."""
        
        primary_style = self.cognitive_traits.get('primary_thinking_style', 'balanced')
        
        templates = {
            'analytical': {
                'opening': [
                    "Let me break this down systematically:",
                    "I need to analyze the key components here:",
                    "First, let me examine the core elements:",
                    "Looking at this logically, I should start by:"
                ],
                'process': [
                    "The evidence suggests that...",
                    "Based on the available data...",
                    "If I examine each factor individually...",
                    "The logical progression would be..."
                ],
                'conclusion': [
                    "Based on this analysis, my recommendation is:",
                    "Weighing all the factors, I conclude that:",
                    "The most logical approach would be to:",
                    "Given the evidence, the best course of action is:"
                ]
            },
            'intuitive': {
                'opening': [
                    "My initial sense about this is:",
                    "Something tells me that:",
                    "I have a strong feeling that:",
                    "My gut reaction is that:"
                ],
                'process': [
                    "This situation reminds me of...",
                    "I sense that the underlying issue might be...",
                    "My intuition suggests that...",
                    "It feels like the key insight here is..."
                ],
                'conclusion': [
                    "So my instinct says:",
                    "Based on my intuition, I believe:",
                    "My gut tells me the answer is:",
                    "I feel strongly that we should:"
                ]
            },
            'creative': {
                'opening': [
                    "What if we approached this differently?",
                    "Let me think outside the box here:",
                    "I'm imagining some unconventional possibilities:",
                    "There might be a creative solution here:"
                ],
                'process': [
                    "One innovative approach could be...",
                    "What if we completely reimagined...",
                    "I'm envisioning a scenario where...",
                    "A creative twist might be to..."
                ],
                'conclusion': [
                    "So my creative solution would be:",
                    "I think an innovative approach is:",
                    "The most interesting possibility is:",
                    "My unconventional recommendation is:"
                ]
            },
            'balanced': {
                'opening': [
                    "Let me consider this from multiple angles:",
                    "I want to balance logic and intuition here:",
                    "Looking at both the analytical and creative aspects:",
                    "This requires both systematic thinking and insights:"
                ],
                'process': [
                    "On one hand, the data shows... but I also sense that...",
                    "Logically, this suggests... yet intuitively, I feel...",
                    "The systematic approach would be... while creatively, we could...",
                    "Balancing facts with insights..."
                ],
                'conclusion': [
                    "Considering all perspectives, I recommend:",
                    "Balancing analysis with intuition, I think:",
                    "My integrated approach would be:",
                    "Combining logic and insight, the best path is:"
                ]
            }
        }
        
        return templates
    
    def _initialize_response_patterns(self) -> Dict[str, Any]:
        """Initialize response patterns based on communication style."""
        
        communication = self.communication_style
        decision_making = self.decision_making
        
        return {
            'typical_length': self._determine_response_length(),
            'question_tendency': communication.get('question_frequency', 0.2),
            'explanation_depth': communication.get('explanation_preference', 'moderate'),
            'stakeholder_focus': self.cognitive_traits.get('stakeholder_awareness', 'medium'),
            'risk_consideration': self.cognitive_traits.get('risk_assessment_style', 'medium'),
            'collaboration_inclination': self.cognitive_traits.get('collaboration_preference', 'medium'),
            'implementation_focus': self.cognitive_traits.get('implementation_focus', 'medium')
        }
    
    def _analyze_problem_characteristics(self, problem: str) -> Dict[str, Any]:
        """Analyze the characteristics of the given problem."""
        
        problem_lower = problem.lower()
        
        characteristics = {
            'type': self._classify_problem_type(problem_lower),
            'stakeholders_mentioned': self._count_stakeholder_mentions(problem_lower),
            'urgency_level': self._assess_urgency(problem_lower),
            'complexity_indicators': self._assess_complexity_indicators(problem_lower),
            'decision_required': self._requires_decision(problem_lower),
            'creative_potential': self._assess_creative_potential(problem_lower),
            'risk_elements': self._identify_risk_elements(problem_lower)
        }
        
        return characteristics
    
    def _select_reasoning_approach(self, problem_analysis: Dict, complexity: str) -> str:
        """Select the best reasoning approach based on problem and cognitive profile."""
        
        primary_style = self.cognitive_traits.get('primary_thinking_style', 'balanced')
        
        # Modify approach based on problem characteristics
        if problem_analysis.get('creative_potential', 0) > 0.7 and self.cognitive_traits.get('creative_tendency', 0) > 0.5:
            return 'creative'
        elif problem_analysis.get('complexity_indicators', 0) > 0.7 and self.cognitive_traits.get('analytical_tendency', 0) > 0.5:
            return 'analytical'
        elif problem_analysis.get('urgency_level', 'medium') == 'high' and self.cognitive_traits.get('intuitive_tendency', 0) > 0.5:
            return 'intuitive'
        else:
            return primary_style
    
    def _generate_reasoning_steps(self, problem: str, approach: str, complexity: str) -> List[str]:
        """Generate reasoning steps based on cognitive approach."""
        
        if approach == 'analytical':
            return self._analytical_reasoning_steps(problem, complexity)
        elif approach == 'intuitive':
            return self._intuitive_reasoning_steps(problem, complexity)
        elif approach == 'creative':
            return self._creative_reasoning_steps(problem, complexity)
        else:  # balanced
            return self._balanced_reasoning_steps(problem, complexity)
    
    def _analytical_reasoning_steps(self, problem: str, complexity: str) -> List[str]:
        """Generate analytical reasoning steps."""
        
        base_steps = [
            "Identify and define the core problem clearly",
            "Gather and analyze all available relevant information",
            "Break down the problem into manageable components",
            "Evaluate potential solutions against clear criteria",
            "Select the most logical solution based on evidence"
        ]
        
        if complexity == "complex":
            base_steps.extend([
                "Consider second-order effects and long-term implications", 
                "Identify potential risks and develop mitigation strategies",
                "Create implementation plan with measurable milestones"
            ])
        
        return base_steps
    
    def _intuitive_reasoning_steps(self, problem: str, complexity: str) -> List[str]:
        """Generate intuitive reasoning steps."""
        
        base_steps = [
            "Get an overall sense of the situation and context",
            "Notice patterns and what immediately stands out",
            "Draw on past experiences and gut feelings",
            "Trust initial instincts about promising directions",
            "Integrate insights into a holistic understanding"
        ]
        
        if complexity == "complex":
            base_steps.extend([
                "Allow time for subconscious processing of complex elements",
                "Validate intuitive insights with key stakeholders"
            ])
        
        return base_steps
    
    def _creative_reasoning_steps(self, problem: str, complexity: str) -> List[str]:
        """Generate creative reasoning steps."""
        
        base_steps = [
            "Reframe the problem from multiple perspectives",
            "Brainstorm unconventional approaches and possibilities", 
            "Look for unexpected connections and analogies",
            "Prototype and test innovative ideas quickly",
            "Iterate and refine the most promising concepts"
        ]
        
        if complexity == "complex":
            base_steps.extend([
                "Explore cross-industry solutions and inspirations",
                "Design experiments to test creative hypotheses"
            ])
        
        return base_steps
    
    def _balanced_reasoning_steps(self, problem: str, complexity: str) -> List[str]:
        """Generate balanced reasoning steps."""
        
        return [
            "Combine systematic analysis with intuitive insights",
            "Use data and logic while staying open to creative possibilities",
            "Validate analytical conclusions against gut feelings",
            "Consider both rational and emotional aspects of the situation",
            "Integrate multiple perspectives into a comprehensive solution"
        ]
    
    def _generate_response(self, problem: str, reasoning_steps: List[str], approach: str) -> str:
        """Generate the actual response text."""
        
        templates = self.reasoning_templates.get(approach, self.reasoning_templates['balanced'])
        
        # Select templates based on cognitive style
        opening = random.choice(templates['opening'])
        process = random.choice(templates['process'])
        conclusion = random.choice(templates['conclusion'])
        
        # Generate core solution
        solution = self._generate_solution_content(problem, approach)
        
        # Build response with personality adjustments
        response = f"{opening}\n\n{process}\n\n{solution}\n\n{conclusion}"
        
        # Apply communication style modifications
        response = self._apply_communication_style(response)
        
        # Apply decision-making style modifications  
        response = self._apply_decision_making_style(response, problem)
        
        return response
    
    def _generate_solution_content(self, problem: str, approach: str) -> str:
        """Generate solution content based on problem and approach."""
        
        problem_lower = problem.lower()
        
        # Determine problem category for targeted solutions
        if any(word in problem_lower for word in ['decision', 'choose', 'decide', 'select']):
            return self._generate_decision_solution(problem, approach)
        elif any(word in problem_lower for word in ['plan', 'organize', 'manage', 'schedule']):
            return self._generate_planning_solution(problem, approach)
        elif any(word in problem_lower for word in ['conflict', 'disagreement', 'problem', 'issue']):
            return self._generate_problem_solving_solution(problem, approach)
        elif any(word in problem_lower for word in ['create', 'design', 'innovate', 'improve']):
            return self._generate_creative_solution(problem, approach)
        else:
            return self._generate_general_solution(problem, approach)
    
    def _generate_decision_solution(self, problem: str, approach: str) -> str:
        """Generate decision-focused solutions."""
        
        if approach == 'analytical':
            return "I would create a decision matrix to evaluate the key criteria, assign weights based on importance, score each option objectively, and select the highest-scoring alternative while considering implementation feasibility."
        elif approach == 'intuitive':
            return "I would reflect deeply on which option feels most aligned with my core values and long-term vision, considering how each choice resonates emotionally and trusting my instincts about the right path forward."
        elif approach == 'creative':
            return "I would explore whether there are alternative options beyond the obvious choices, perhaps combining elements from different possibilities or finding a completely novel third way that addresses the underlying need differently."
        else:
            return "I would combine systematic evaluation of the options with careful consideration of how each choice feels intuitively, ensuring both the logical and emotional aspects align before making my final decision."
    
    def _generate_planning_solution(self, problem: str, approach: str) -> str:
        """Generate planning-focused solutions."""
        
        if approach == 'analytical':
            return "I would break this into clear phases with specific deliverables, create detailed timelines with dependencies mapped out, identify critical path activities, and establish measurable milestones with regular review points."
        elif approach == 'intuitive':
            return "I would start with the big picture vision of success, work backwards to identify the key milestones that feel most important, and maintain flexibility to adapt the plan as new insights emerge along the way."
        elif approach == 'creative':
            return "I would explore innovative approaches that might accomplish the goal more efficiently, look for opportunities to combine or reimagine traditional steps, and design the plan to allow for creative pivots and improvements."
        else:
            return "I would develop a structured framework that includes clear milestones while building in flexibility for adjustments, balancing detailed planning with the ability to respond to unexpected opportunities or challenges."
    
    def _generate_problem_solving_solution(self, problem: str, approach: str) -> str:
        """Generate problem-solving solutions."""
        
        if approach == 'analytical':
            return "I would systematically identify the root causes using techniques like the 5 Whys, research best practices and proven solutions, develop a step-by-step action plan, and implement with careful monitoring and adjustment."
        elif approach == 'intuitive':
            return "I would step back to understand the broader context and underlying patterns, listen carefully to all perspectives involved, and focus on addressing the deeper needs and concerns rather than just the surface symptoms."
        elif approach == 'creative':
            return "I would reframe the problem to uncover new possibilities, brainstorm unconventional solutions, look for ways to turn the challenge into an opportunity, and experiment with innovative approaches."
        else:
            return "I would combine thorough analysis of the situation with creative brainstorming, ensuring I understand both the logical and emotional dimensions of the problem while exploring both traditional and innovative solutions."
    
    def _generate_creative_solution(self, problem: str, approach: str) -> str:
        """Generate creative/innovation solutions."""
        
        base_solution = "I would start by immersing myself in the challenge to understand it deeply, then explore inspiration from diverse sources and industries, prototype ideas quickly to test concepts, and iterate based on feedback to refine the most promising innovations."
        
        if approach == 'analytical':
            return base_solution + " I'd also establish clear success metrics and evaluation criteria to ensure the creative solution meets practical requirements."
        elif approach == 'intuitive':
            return base_solution + " I'd trust my instincts about which ideas have the most potential and allow time for subconscious processing to generate breakthrough insights."
        else:
            return base_solution
    
    def _generate_general_solution(self, problem: str, approach: str) -> str:
        """Generate general problem solutions."""
        
        if approach == 'analytical':
            return "I would approach this systematically by first understanding all the key factors involved, researching relevant information and best practices, developing a clear strategy with specific steps, and implementing with careful tracking and adjustment as needed."
        elif approach == 'intuitive':
            return "I would start by getting a feel for the overall situation, trusting my instincts about the most important aspects to address first, and allowing my understanding to evolve naturally as I engage with the challenge."
        elif approach == 'creative':
            return "I would look for innovative ways to approach this challenge, explore unconventional solutions and fresh perspectives, and experiment with ideas that might lead to breakthrough results."
        else:
            return "I would combine careful analysis with creative thinking, ensuring I understand the situation thoroughly while remaining open to innovative solutions and approaches that might emerge during the process."
    
    def _apply_communication_style(self, response: str) -> str:
        """Apply communication style preferences to the response."""
        
        style = self.communication_style.get('style_category', 'balanced')
        explanation_pref = self.communication_style.get('explanation_preference', 'moderate')
        
        # Adjust for explanation depth preference
        if explanation_pref == 'detailed' or style in ['detailed_explanatory', 'detailed_inquisitive']:
            response += "\n\nTo elaborate further, this approach allows for comprehensive consideration of all relevant factors while maintaining flexibility to adapt as new information emerges."
        
        # Add questions for inquisitive styles
        if 'inquisitive' in style or self.response_patterns['question_tendency'] > 0.5:
            response += "\n\nI'd be curious to know: What aspects of this situation do you think are most important to consider? Are there any constraints or considerations I might have missed?"
        
        return response
    
    def _apply_decision_making_style(self, response: str, problem: str) -> str:
        """Apply decision-making style preferences."""
        
        # Add stakeholder considerations if high stakeholder awareness
        if self.response_patterns['stakeholder_focus'] == 'high':
            response += "\n\nIt would also be important to consider how this affects all stakeholders involved and ensure everyone's perspectives are heard and valued in the process."
        
        # Add risk considerations if high risk awareness
        if self.response_patterns['risk_consideration'] == 'high':
            response += "\n\nI'd also want to carefully assess potential risks and develop contingency plans to address any challenges that might arise during implementation."
        
        # Add collaboration elements if collaborative tendency is high
        if self.response_patterns['collaboration_inclination'] == 'high':
            response += "\n\nThis would work best as a collaborative effort, bringing together different perspectives and expertise to ensure the best possible outcome."
        
        # Add implementation focus if high
        if self.response_patterns['implementation_focus'] == 'high':
            response += "\n\nMost importantly, I'd want to ensure we have a concrete plan for implementation with clear responsibilities, timelines, and success metrics."
        
        return response
    
    def _identify_decision_factors(self, problem: str, analysis: Dict) -> List[str]:
        """Identify key factors this person would consider when making decisions."""
        
        factors = []
        
        # Base factors everyone considers
        factors.extend([
            "Potential outcomes and their likelihood",
            "Available resources and constraints",
            "Alignment with goals and values"
        ])
        
        # Add factors based on cognitive traits
        if self.cognitive_traits.get('analytical_tendency', 0) > 0.6:
            factors.append("Data and evidence supporting each option")
        
        if self.cognitive_traits.get('creative_tendency', 0) > 0.6:
            factors.append("Opportunities for innovation and creative solutions")
        
        if self.cognitive_traits.get('stakeholder_awareness') == 'high':
            factors.append("Impact on all stakeholders and their perspectives")
        
        if self.cognitive_traits.get('risk_assessment_style') == 'high':
            factors.append("Risk assessment and contingency planning")
        
        if self.cognitive_traits.get('collaboration_preference') == 'high':
            factors.append("Potential for collaboration and team input")
        
        if self.decision_making.get('implementation_orientation') == 'high':
            factors.append("Practical implementation feasibility")
        
        return factors[:6]  # Limit to most relevant factors
    
    def _calculate_confidence(self, problem: str, complexity: str, approach: str) -> float:
        """Calculate confidence level in the response."""
        
        base_confidence = 0.75
        
        # Adjust based on complexity
        complexity_adjustments = {
            'simple': 0.15,
            'medium': 0.0,
            'complex': -0.10
        }
        base_confidence += complexity_adjustments.get(complexity, 0.0)
        
        # Adjust based on approach alignment with cognitive style
        primary_style = self.cognitive_traits.get('primary_thinking_style', 'balanced')
        if approach == primary_style:
            base_confidence += 0.10
        
        # Adjust based on decision confidence trait
        decision_confidence = self.cognitive_traits.get('decision_confidence', 0.5)
        base_confidence += (decision_confidence - 0.5) * 0.2
        
        # Apply settings adjustments
        confidence_adjustment = self.settings.get('confidence_adjustment', 0.8)
        base_confidence *= confidence_adjustment
        
        return max(0.5, min(0.95, base_confidence))
    
    def _determine_response_length(self) -> str:
        """Determine typical response length based on communication style."""
        
        avg_length = self.communication_style.get('average_message_length', 30)
        explanation_pref = self.communication_style.get('explanation_preference', 'moderate')
        
        if avg_length > 75 or explanation_pref == 'detailed':
            return 'detailed'
        elif avg_length < 20 or explanation_pref == 'concise':
            return 'concise'
        else:
            return 'moderate'
    
    # Helper methods for problem analysis
    def _classify_problem_type(self, problem: str) -> str:
        """Classify the type of problem."""
        
        if any(word in problem for word in ['decision', 'choose', 'decide']):
            return 'decision'
        elif any(word in problem for word in ['plan', 'organize', 'manage']):
            return 'planning'
        elif any(word in problem for word in ['create', 'design', 'innovate']):
            return 'creative'
        elif any(word in problem for word in ['conflict', 'disagreement', 'problem']):
            return 'problem_solving'
        else:
            return 'general'
    
    def _count_stakeholder_mentions(self, problem: str) -> int:
        """Count mentions of stakeholders in the problem."""
        stakeholder_words = ['team', 'people', 'stakeholder', 'client', 'customer', 'employee', 'others']
        return sum(1 for word in stakeholder_words if word in problem)
    
    def _assess_urgency(self, problem: str) -> str:
        """Assess urgency level from problem description."""
        urgent_words = ['urgent', 'immediate', 'quickly', 'asap', 'deadline', 'emergency']
        if any(word in problem for word in urgent_words):
            return 'high'
        elif any(word in problem for word in ['soon', 'timeline', 'schedule']):
            return 'medium'
        else:
            return 'low'
    
    def _assess_complexity_indicators(self, problem: str) -> float:
        """Assess complexity indicators in the problem."""
        complexity_words = ['complex', 'complicated', 'multiple', 'various', 'many', 'different', 'challenging']
        count = sum(1 for word in complexity_words if word in problem)
        return min(count / 3.0, 1.0)  # Normalize to 0-1
    
    def _requires_decision(self, problem: str) -> bool:
        """Check if problem requires a decision."""
        decision_words = ['decide', 'choose', 'select', 'pick', 'option', 'alternative']
        return any(word in problem for word in decision_words)
    
    def _assess_creative_potential(self, problem: str) -> float:
        """Assess creative potential of the problem."""
        creative_words = ['creative', 'innovative', 'new', 'design', 'improve', 'better way']
        count = sum(1 for word in creative_words if word in problem)
        return min(count / 2.0, 1.0)  # Normalize to 0-1
    
    def _identify_risk_elements(self, problem: str) -> int:
        """Identify risk elements in the problem."""
        risk_words = ['risk', 'danger', 'problem', 'issue', 'challenge', 'difficulty']
        return sum(1 for word in risk_words if word in problem)
    
    # Learning and feedback methods
    def positive_feedback(self, problem: str, response: Dict[str, Any]):
        """Learn from positive feedback."""
        feedback_data = {
            'type': 'positive',
            'problem': problem,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        self.learning_data.append(feedback_data)
        
        # In a full implementation, this would update model weights or preferences
        
    def negative_feedback(self, problem: str, response: Dict[str, Any]):
        """Learn from negative feedback."""
        feedback_data = {
            'type': 'negative',
            'problem': problem,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        self.learning_data.append(feedback_data)
        
        # In a full implementation, this would adjust reasoning patterns
    
    def get_response_history(self) -> List[Dict[str, Any]]:
        """Get the history of responses."""
        return self.response_history
    
    def get_learning_data(self) -> List[Dict[str, Any]]:
        """Get the learning feedback data."""
        return self.learning_data
    
    def export_reasoning_patterns(self) -> Dict[str, Any]:
        """Export learned reasoning patterns for analysis."""
        return {
            'profile_id': self.profile.get('profile_id', 'unknown'),
            'cognitive_signature': self.profile.get('cognitive_signature', 'unknown'),
            'response_count': len(self.response_history),
            'feedback_count': len(self.learning_data),
            'reasoning_templates': self.reasoning_templates,
            'response_patterns': self.response_patterns,
            'export_timestamp': datetime.now().isoformat()
        }
