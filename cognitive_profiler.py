import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import networkx as nx
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class CognitiveProfileGenerator:
    def __init__(self):
        self.version = "1.0"
        self.profile_history = []
        
    def generate_comprehensive_profile(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive cognitive profile from assessment data."""
        
        personality_data = assessment_data.get('personality', {})
        problem_solving_data = assessment_data.get('problem_solving', {})
        conversation_history = assessment_data.get('conversation_history', [])
        
        # Generate base profile components
        cognitive_traits = self._extract_cognitive_traits(personality_data, problem_solving_data)
        communication_style = self._analyze_communication_patterns(conversation_history)
        decision_making_profile = self._create_decision_making_profile(problem_solving_data)
        thinking_architecture = self._map_thinking_architecture(personality_data, problem_solving_data)
        
        # Create comprehensive profile
        comprehensive_profile = {
            'profile_id': self._generate_profile_id(),
            'version': self.version,
            'creation_timestamp': datetime.now().isoformat(),
            
            # Core cognitive characteristics
            'cognitive_traits': cognitive_traits,
            'thinking_architecture': thinking_architecture,
            'communication_style': communication_style,
            'decision_making_profile': decision_making_profile,
            
            # Derived insights
            'cognitive_signature': self._generate_cognitive_signature(cognitive_traits),
            'strengths': self._identify_cognitive_strengths(cognitive_traits, decision_making_profile),
            'potential_biases': self._identify_potential_biases(cognitive_traits),
            'learning_preferences': self._infer_learning_preferences(cognitive_traits, communication_style),
            
            # Compatibility and mixing potential
            'hybridization_potential': self._assess_hybridization_potential(cognitive_traits),
            'complementary_traits': self._identify_complementary_traits(cognitive_traits),
            
            # Metadata
            'confidence_score': self._calculate_confidence_score(assessment_data),
            'data_completeness': self._assess_data_completeness(assessment_data),
            'profile_reliability': self._calculate_reliability_score(assessment_data)
        }
        
        # Store in history
        self.profile_history.append(comprehensive_profile)
        
        return comprehensive_profile
    
    def _extract_cognitive_traits(self, personality_data: Dict, problem_solving_data: Dict) -> Dict[str, Any]:
        """Extract core cognitive traits from assessment data."""
        
        # Base traits from personality assessment
        base_traits = {
            'primary_thinking_style': personality_data.get('primary_thinking_style', 'balanced'),
            'analytical_tendency': personality_data.get('analytical_tendency', 0.5),
            'intuitive_tendency': personality_data.get('intuitive_tendency', 0.5),
            'creative_tendency': personality_data.get('creative_tendency', 0.5),
            'systematic_tendency': personality_data.get('systematic_tendency', 0.5)
        }
        
        # Enhanced with problem-solving patterns
        if problem_solving_data:
            base_traits.update({
                'problem_solving_approach': problem_solving_data.get('problem_solving_style', 'balanced'),
                'stakeholder_awareness': problem_solving_data.get('stakeholder_orientation', 'medium'),
                'risk_assessment_style': problem_solving_data.get('risk_assessment', 'medium'),
                'collaboration_preference': problem_solving_data.get('collaboration_tendency', 'medium'),
                'implementation_focus': problem_solving_data.get('implementation_focus', 'medium')
            })
        
        # Calculate composite scores
        base_traits['cognitive_flexibility'] = self._calculate_flexibility_score(base_traits)
        base_traits['decision_confidence'] = personality_data.get('certainty_level', 0.5)
        base_traits['complexity_comfort'] = problem_solving_data.get('complexity_comfort', 'medium') if problem_solving_data else 'medium'
        
        return base_traits
    
    def _analyze_communication_patterns(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Analyze communication patterns from conversation history."""
        
        if not conversation_history:
            return self._default_communication_style()
        
        user_messages = [msg for msg in conversation_history if msg.get('role') == 'user']
        
        if not user_messages:
            return self._default_communication_style()
        
        # Analyze message characteristics
        total_words = sum(len(msg.get('content', '').split()) for msg in user_messages)
        avg_message_length = total_words / len(user_messages)
        
        total_questions = sum(msg.get('content', '').count('?') for msg in user_messages)
        question_frequency = total_questions / len(user_messages)
        
        total_exclamations = sum(msg.get('content', '').count('!') for msg in user_messages)
        exclamation_frequency = total_exclamations / len(user_messages)
        
        # Determine communication style
        if avg_message_length > 50 and question_frequency > 0.5:
            style_category = 'detailed_inquisitive'
        elif avg_message_length > 50:
            style_category = 'detailed_explanatory'
        elif question_frequency > 0.5:
            style_category = 'concise_inquisitive'
        else:
            style_category = 'concise_direct'
        
        return {
            'style_category': style_category,
            'average_message_length': avg_message_length,
            'question_frequency': question_frequency,
            'exclamation_frequency': exclamation_frequency,
            'formality_level': self._assess_formality_level(user_messages),
            'explanation_preference': 'detailed' if avg_message_length > 50 else 'concise',
            'interaction_style': 'collaborative' if question_frequency > 0.3 else 'directive'
        }
    
    def _create_decision_making_profile(self, problem_solving_data: Dict) -> Dict[str, Any]:
        """Create decision-making profile from problem-solving data."""
        
        if not problem_solving_data:
            return self._default_decision_making_profile()
        
        return {
            'decision_speed': problem_solving_data.get('decision_making_speed', 'medium'),
            'information_gathering': 'extensive' if problem_solving_data.get('risk_assessment') == 'high' else 'focused',
            'stakeholder_consideration': problem_solving_data.get('stakeholder_orientation', 'medium'),
            'risk_tolerance': self._convert_risk_assessment_to_tolerance(problem_solving_data.get('risk_assessment', 'medium')),
            'consensus_seeking': problem_solving_data.get('collaboration_tendency', 'medium'),
            'implementation_orientation': problem_solving_data.get('implementation_focus', 'medium'),
            'contingency_planning': 'high' if problem_solving_data.get('risk_assessment') == 'high' else 'medium'
        }
    
    def _map_thinking_architecture(self, personality_data: Dict, problem_solving_data: Dict) -> Dict[str, Any]:
        """Map the individual's cognitive architecture."""
        
        # Core processing preferences
        processing_style = personality_data.get('primary_thinking_style', 'balanced')
        
        # Attention and focus patterns
        attention_pattern = self._infer_attention_pattern(personality_data, problem_solving_data)
        
        # Memory and knowledge organization
        memory_style = self._infer_memory_organization_style(personality_data)
        
        # Problem-solving approach
        problem_solving_architecture = self._map_problem_solving_approach(problem_solving_data)
        
        return {
            'primary_processing_mode': processing_style,
            'attention_allocation': attention_pattern,
            'memory_organization': memory_style,
            'problem_solving_framework': problem_solving_architecture,
            'metacognitive_awareness': self._assess_metacognitive_awareness(personality_data),
            'cognitive_control': self._assess_cognitive_control(personality_data, problem_solving_data)
        }
    
    def _generate_cognitive_signature(self, cognitive_traits: Dict) -> str:
        """Generate a unique cognitive signature for the profile."""
        
        # Create signature components
        thinking_style = cognitive_traits.get('primary_thinking_style', 'balanced')[:2].upper()
        
        analytical_level = 'H' if cognitive_traits.get('analytical_tendency', 0) > 0.7 else 'M' if cognitive_traits.get('analytical_tendency', 0) > 0.3 else 'L'
        intuitive_level = 'H' if cognitive_traits.get('intuitive_tendency', 0) > 0.7 else 'M' if cognitive_traits.get('intuitive_tendency', 0) > 0.3 else 'L'
        creative_level = 'H' if cognitive_traits.get('creative_tendency', 0) > 0.7 else 'M' if cognitive_traits.get('creative_tendency', 0) > 0.3 else 'L'
        
        problem_solving_style = cognitive_traits.get('problem_solving_approach', 'balanced')[:2].upper()
        
        return f"{thinking_style}-{analytical_level}{intuitive_level}{creative_level}-{problem_solving_style}"
    
    def _identify_cognitive_strengths(self, cognitive_traits: Dict, decision_making_profile: Dict) -> List[str]:
        """Identify key cognitive strengths based on profile."""
        
        strengths = []
        
        # Analytical strength
        if cognitive_traits.get('analytical_tendency', 0) > 0.7:
            strengths.append('systematic_analysis')
        
        # Creative strength
        if cognitive_traits.get('creative_tendency', 0) > 0.7:
            strengths.append('innovative_thinking')
        
        # Intuitive strength
        if cognitive_traits.get('intuitive_tendency', 0) > 0.7:
            strengths.append('pattern_recognition')
        
        # Decision-making strengths
        if decision_making_profile.get('decision_speed') == 'quick':
            strengths.append('rapid_decision_making')
        elif decision_making_profile.get('decision_speed') == 'deliberate':
            strengths.append('thorough_consideration')
        
        # Collaboration strength
        if cognitive_traits.get('collaboration_preference') == 'high':
            strengths.append('collaborative_leadership')
        
        # Implementation strength
        if cognitive_traits.get('implementation_focus') == 'high':
            strengths.append('execution_excellence')
        
        # Stakeholder awareness
        if cognitive_traits.get('stakeholder_awareness') == 'high':
            strengths.append('stakeholder_management')
        
        return strengths
    
    def _identify_potential_biases(self, cognitive_traits: Dict) -> List[str]:
        """Identify potential cognitive biases based on traits."""
        
        biases = []
        
        # Over-analytical bias
        if cognitive_traits.get('analytical_tendency', 0) > 0.8:
            biases.append('analysis_paralysis')
        
        # Over-intuitive bias
        if cognitive_traits.get('intuitive_tendency', 0) > 0.8:
            biases.append('confirmation_bias')
        
        # Risk-related biases
        risk_style = cognitive_traits.get('risk_assessment_style', 'medium')
        if risk_style == 'high':
            biases.append('loss_aversion')
        elif risk_style == 'low':
            biases.append('overconfidence_bias')
        
        # Decision speed biases
        if cognitive_traits.get('decision_confidence', 0) > 0.8:
            biases.append('anchoring_bias')
        
        return biases
    
    def _infer_learning_preferences(self, cognitive_traits: Dict, communication_style: Dict) -> Dict[str, str]:
        """Infer learning preferences from cognitive traits."""
        
        preferences = {}
        
        # Information processing preference
        if cognitive_traits.get('analytical_tendency', 0) > cognitive_traits.get('intuitive_tendency', 0):
            preferences['information_processing'] = 'sequential'
        else:
            preferences['information_processing'] = 'holistic'
        
        # Content delivery preference
        if communication_style.get('explanation_preference') == 'detailed':
            preferences['content_delivery'] = 'comprehensive'
        else:
            preferences['content_delivery'] = 'concise'
        
        # Interaction preference
        if communication_style.get('interaction_style') == 'collaborative':
            preferences['learning_mode'] = 'interactive'
        else:
            preferences['learning_mode'] = 'self_directed'
        
        # Complexity preference
        complexity_comfort = cognitive_traits.get('complexity_comfort', 'medium')
        if complexity_comfort == 'high':
            preferences['complexity_level'] = 'advanced'
        elif complexity_comfort == 'low':
            preferences['complexity_level'] = 'simplified'
        else:
            preferences['complexity_level'] = 'moderate'
        
        return preferences
    
    def _assess_hybridization_potential(self, cognitive_traits: Dict) -> Dict[str, Any]:
        """Assess how well this profile could be hybridized with others."""
        
        # Calculate trait flexibility
        trait_scores = [
            cognitive_traits.get('analytical_tendency', 0.5),
            cognitive_traits.get('intuitive_tendency', 0.5),
            cognitive_traits.get('creative_tendency', 0.5),
            cognitive_traits.get('systematic_tendency', 0.5)
        ]
        
        # Higher flexibility = better for hybridization
        flexibility_score = 1 - np.std(trait_scores)  # Lower standard deviation = more balanced = more flexible
        
        dominant_traits = []
        if cognitive_traits.get('analytical_tendency', 0) > 0.7:
            dominant_traits.append('analytical')
        if cognitive_traits.get('creative_tendency', 0) > 0.7:
            dominant_traits.append('creative')
        if cognitive_traits.get('intuitive_tendency', 0) > 0.7:
            dominant_traits.append('intuitive')
        
        return {
            'flexibility_score': flexibility_score,
            'dominant_traits': dominant_traits,
            'hybridization_difficulty': 'low' if flexibility_score > 0.7 else 'medium' if flexibility_score > 0.4 else 'high',
            'best_hybrid_roles': self._suggest_hybrid_roles(dominant_traits)
        }
    
    def _identify_complementary_traits(self, cognitive_traits: Dict) -> List[str]:
        """Identify traits that would complement this profile in a hybrid."""
        
        complementary = []
        
        # If low in analytical, needs analytical complement
        if cognitive_traits.get('analytical_tendency', 0) < 0.3:
            complementary.append('high_analytical')
        
        # If low in creative, needs creative complement
        if cognitive_traits.get('creative_tendency', 0) < 0.3:
            complementary.append('high_creative')
        
        # If low in intuitive, needs intuitive complement
        if cognitive_traits.get('intuitive_tendency', 0) < 0.3:
            complementary.append('high_intuitive')
        
        # If low risk tolerance, needs risk-taking complement
        if cognitive_traits.get('risk_assessment_style') == 'high':
            complementary.append('risk_taking')
        
        # If low collaboration, needs collaborative complement
        if cognitive_traits.get('collaboration_preference') == 'low':
            complementary.append('high_collaboration')
        
        return complementary
    
    def create_hybrid_profile(self, profiles: List[Dict], weights: List[float], use_case: str) -> Dict[str, Any]:
        """Create a hybrid cognitive profile from multiple profiles."""
        
        if len(profiles) != len(weights):
            raise ValueError("Number of profiles must match number of weights")
        
        if abs(sum(weights) - 1.0) > 0.01:
            raise ValueError("Weights must sum to 1.0")
        
        # Initialize hybrid profile structure
        hybrid_profile = {
            'profile_id': self._generate_profile_id(),
            'version': self.version,
            'creation_timestamp': datetime.now().isoformat(),
            'profile_type': 'hybrid',
            'source_profiles': [p.get('profile_id') for p in profiles],
            'hybrid_weights': weights,
            'use_case': use_case
        }
        
        # Blend cognitive traits
        hybrid_traits = self._blend_cognitive_traits(profiles, weights)
        hybrid_profile['cognitive_traits'] = hybrid_traits
        
        # Create hybrid thinking architecture
        hybrid_profile['thinking_architecture'] = self._blend_thinking_architectures(profiles, weights)
        
        # Determine dominant communication style
        hybrid_profile['communication_style'] = self._select_dominant_communication_style(profiles, weights)
        
        # Blend decision-making profiles
        hybrid_profile['decision_making_profile'] = self._blend_decision_making_profiles(profiles, weights)
        
        # Generate new signature
        hybrid_profile['cognitive_signature'] = self._generate_cognitive_signature(hybrid_traits)
        
        # Assess hybrid strengths and characteristics
        hybrid_profile['hybrid_strengths'] = self._identify_hybrid_strengths(profiles, weights)
        hybrid_profile['potential_conflicts'] = self._identify_potential_conflicts(profiles, weights)
        hybrid_profile['optimization_suggestions'] = self._generate_optimization_suggestions(use_case, hybrid_traits)
        
        return hybrid_profile
    
    def _blend_cognitive_traits(self, profiles: List[Dict], weights: List[float]) -> Dict[str, Any]:
        """Blend cognitive traits from multiple profiles."""
        
        blended_traits = {}
        
        # Numerical traits - weighted average
        numerical_traits = [
            'analytical_tendency', 'intuitive_tendency', 'creative_tendency', 
            'systematic_tendency', 'decision_confidence', 'cognitive_flexibility'
        ]
        
        for trait in numerical_traits:
            weighted_sum = sum(
                profile.get('cognitive_traits', {}).get(trait, 0.5) * weight 
                for profile, weight in zip(profiles, weights)
            )
            blended_traits[trait] = weighted_sum
        
        # Categorical traits - select from dominant profile
        dominant_profile_index = weights.index(max(weights))
        categorical_traits = [
            'primary_thinking_style', 'problem_solving_approach', 
            'complexity_comfort', 'stakeholder_awareness', 'risk_assessment_style'
        ]
        
        for trait in categorical_traits:
            blended_traits[trait] = profiles[dominant_profile_index].get('cognitive_traits', {}).get(trait, 'medium')
        
        return blended_traits
    
    # Helper methods
    def _calculate_flexibility_score(self, traits: Dict) -> float:
        """Calculate cognitive flexibility based on trait balance."""
        trait_values = [
            traits.get('analytical_tendency', 0.5),
            traits.get('intuitive_tendency', 0.5),
            traits.get('creative_tendency', 0.5)
        ]
        return 1 - np.std(trait_values)  # More balanced = more flexible
    
    def _default_communication_style(self) -> Dict[str, Any]:
        """Return default communication style when no data available."""
        return {
            'style_category': 'balanced',
            'average_message_length': 30,
            'question_frequency': 0.2,
            'exclamation_frequency': 0.1,
            'formality_level': 'medium',
            'explanation_preference': 'moderate',
            'interaction_style': 'collaborative'
        }
    
    def _default_decision_making_profile(self) -> Dict[str, Any]:
        """Return default decision-making profile when no data available."""
        return {
            'decision_speed': 'medium',
            'information_gathering': 'balanced',
            'stakeholder_consideration': 'medium',
            'risk_tolerance': 'medium',
            'consensus_seeking': 'medium',
            'implementation_orientation': 'medium',
            'contingency_planning': 'medium'
        }
    
    def _generate_profile_id(self) -> str:
        """Generate unique profile ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"PROFILE_{timestamp}"
    
    def _calculate_confidence_score(self, assessment_data: Dict) -> float:
        """Calculate confidence score based on data quality and completeness."""
        score = 0.0
        
        # Check personality data completeness
        personality_data = assessment_data.get('personality', {})
        if personality_data and len(personality_data) > 5:
            score += 0.4
        
        # Check problem-solving data completeness
        problem_solving_data = assessment_data.get('problem_solving', {})
        if problem_solving_data and len(problem_solving_data) > 3:
            score += 0.3
        
        # Check conversation data
        conversation_history = assessment_data.get('conversation_history', [])
        if len(conversation_history) > 10:
            score += 0.3
        
        return min(score, 1.0)
    
    def _assess_data_completeness(self, assessment_data: Dict) -> str:
        """Assess completeness of assessment data."""
        completeness_score = 0
        
        if assessment_data.get('personality'):
            completeness_score += 1
        if assessment_data.get('problem_solving'):
            completeness_score += 1
        if assessment_data.get('conversation_history') and len(assessment_data['conversation_history']) > 5:
            completeness_score += 1
        
        if completeness_score == 3:
            return 'complete'
        elif completeness_score == 2:
            return 'good'
        elif completeness_score == 1:
            return 'partial'
        else:
            return 'insufficient'
    
    def _calculate_reliability_score(self, assessment_data: Dict) -> float:
        """Calculate reliability score based on consistency of responses."""
        # This is a simplified reliability calculation
        # In a real implementation, you'd analyze consistency across similar questions
        base_score = 0.8
        
        # Reduce score if data is incomplete
        completeness = self._assess_data_completeness(assessment_data)
        if completeness == 'partial':
            base_score -= 0.2
        elif completeness == 'insufficient':
            base_score -= 0.4
        
        return max(base_score, 0.1)
    
    # Additional helper methods would be implemented here for the full system
    def _infer_attention_pattern(self, personality_data: Dict, problem_solving_data: Dict) -> str:
        """Infer attention allocation pattern."""
        if personality_data.get('systematic_tendency', 0) > 0.7:
            return 'focused_sequential'
        elif personality_data.get('creative_tendency', 0) > 0.7:
            return 'diffuse_exploratory'
        else:
            return 'adaptive_switching'
    
    def _infer_memory_organization_style(self, personality_data: Dict) -> str:
        """Infer memory organization preferences."""
        if personality_data.get('systematic_tendency', 0) > 0.7:
            return 'hierarchical_structured'
        elif personality_data.get('creative_tendency', 0) > 0.7:
            return 'associative_networked'
        else:
            return 'mixed_organization'
    
    def _map_problem_solving_approach(self, problem_solving_data: Dict) -> Dict[str, str]:
        """Map problem-solving approach characteristics."""
        if not problem_solving_data:
            return {'primary_approach': 'systematic', 'backup_approach': 'intuitive'}
        
        primary = problem_solving_data.get('problem_solving_style', 'systematic')
        return {'primary_approach': primary, 'backup_approach': 'intuitive' if primary == 'analytical' else 'analytical'}
    
    def _assess_metacognitive_awareness(self, personality_data: Dict) -> str:
        """Assess level of metacognitive awareness."""
        question_frequency = personality_data.get('question_frequency', 0)
        if question_frequency > 1.0:
            return 'high'
        elif question_frequency > 0.5:
            return 'medium'
        else:
            return 'low'
    
    def _assess_cognitive_control(self, personality_data: Dict, problem_solving_data: Dict) -> str:
        """Assess cognitive control and regulation."""
        systematic_score = personality_data.get('systematic_tendency', 0.5)
        certainty_level = personality_data.get('certainty_level', 0.5)
        
        control_score = (systematic_score + certainty_level) / 2
        
        if control_score > 0.7:
            return 'high'
        elif control_score > 0.3:
            return 'medium'
        else:
            return 'low'
    
    def _suggest_hybrid_roles(self, dominant_traits: List[str]) -> List[str]:
        """Suggest optimal roles for hybrid combinations."""
        role_suggestions = []
        
        if 'analytical' in dominant_traits:
            role_suggestions.append('strategic_advisor')
        if 'creative' in dominant_traits:
            role_suggestions.append('innovation_catalyst')
        if 'intuitive' in dominant_traits:
            role_suggestions.append('pattern_synthesizer')
        
        if len(dominant_traits) > 1:
            role_suggestions.append('cognitive_bridge')
        
        return role_suggestions if role_suggestions else ['balanced_generalist']