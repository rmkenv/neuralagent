#!/usr/bin/env python3
"""
Demo script showcasing the complete hybrid cognitive profile functionality
"""

import json
from src.cognitive_profiling.cognitive_profiler import CognitiveProfileGenerator
from src.cognitive_profiling.profile_manager import ProfileManager

def main():
    print("🧠 Neural Agent Hybrid Profile Demo")
    print("=" * 50)
    
    # Initialize components
    profiler = CognitiveProfileGenerator()
    manager = ProfileManager()
    
    # Create sample assessment data for different personality types
    analytical_data = {
        'personality': {
            'primary_thinking_style': 'analytical',
            'analytical_tendency': 0.9,
            'intuitive_tendency': 0.3,
            'creative_tendency': 0.4,
            'systematic_tendency': 0.8,
            'certainty_level': 0.8
        },
        'problem_solving': {
            'problem_solving_style': 'systematic',
            'stakeholder_orientation': 'high',
            'risk_assessment': 'high',
            'collaboration_tendency': 'medium',
            'implementation_focus': 'high',
            'decision_making_speed': 'deliberate',
            'complexity_comfort': 'high'
        },
        'conversation_history': [
            {'role': 'user', 'content': 'I need to analyze this problem systematically, considering all variables and potential risks.'},
            {'role': 'user', 'content': 'Let me break this down step by step and examine the data carefully.'}
        ]
    }
    
    creative_data = {
        'personality': {
            'primary_thinking_style': 'creative',
            'analytical_tendency': 0.4,
            'intuitive_tendency': 0.8,
            'creative_tendency': 0.9,
            'systematic_tendency': 0.3,
            'certainty_level': 0.5
        },
        'problem_solving': {
            'problem_solving_style': 'creative',
            'stakeholder_orientation': 'medium',
            'risk_assessment': 'low',
            'collaboration_tendency': 'high',
            'implementation_focus': 'medium',
            'decision_making_speed': 'quick',
            'complexity_comfort': 'medium'
        },
        'conversation_history': [
            {'role': 'user', 'content': 'What if we approached this completely differently? I have some wild ideas!'},
            {'role': 'user', 'content': 'Let me brainstorm some innovative solutions that nobody has tried before.'}
        ]
    }
    
    intuitive_data = {
        'personality': {
            'primary_thinking_style': 'intuitive',
            'analytical_tendency': 0.5,
            'intuitive_tendency': 0.9,
            'creative_tendency': 0.6,
            'systematic_tendency': 0.4,
            'certainty_level': 0.6
        },
        'problem_solving': {
            'problem_solving_style': 'intuitive',
            'stakeholder_orientation': 'high',
            'risk_assessment': 'medium',
            'collaboration_tendency': 'high',
            'implementation_focus': 'medium',
            'decision_making_speed': 'quick',
            'complexity_comfort': 'high'
        },
        'conversation_history': [
            {'role': 'user', 'content': 'I have a gut feeling about this. Something tells me we should focus on the human element.'},
            {'role': 'user', 'content': 'The patterns I see suggest we need to consider the bigger picture here.'}
        ]
    }
    
    print("1. Generating Individual Profiles...")
    print("-" * 30)
    
    # Generate individual profiles
    analytical_profile = profiler.generate_comprehensive_profile(analytical_data)
    creative_profile = profiler.generate_comprehensive_profile(creative_data)
    intuitive_profile = profiler.generate_comprehensive_profile(intuitive_data)
    
    print(f"✅ Analytical Profile: {analytical_profile['cognitive_signature']}")
    print(f"   Strengths: {', '.join(analytical_profile['strengths'][:3])}")
    
    print(f"✅ Creative Profile: {creative_profile['cognitive_signature']}")
    print(f"   Strengths: {', '.join(creative_profile['strengths'][:3])}")
    
    print(f"✅ Intuitive Profile: {intuitive_profile['cognitive_signature']}")
    print(f"   Strengths: {', '.join(intuitive_profile['strengths'][:3])}")
    
    # Save individual profiles
    manager.save_profile(analytical_profile)
    manager.save_profile(creative_profile)
    manager.save_profile(intuitive_profile)
    
    print(f"\n2. Creating Hybrid Profiles...")
    print("-" * 30)
    
    # Create different hybrid profiles for different use cases
    
    # Leadership hybrid: Analytical + Intuitive
    leadership_hybrid = profiler.create_hybrid_profile(
        [analytical_profile, intuitive_profile],
        [0.6, 0.4],
        'leadership'
    )
    
    print(f"✅ Leadership Hybrid: {leadership_hybrid['cognitive_signature']}")
    print(f"   Source: {analytical_profile['cognitive_signature']} (60%) + {intuitive_profile['cognitive_signature']} (40%)")
    print(f"   Strengths: {', '.join(leadership_hybrid['hybrid_strengths'][:3])}")
    if leadership_hybrid['potential_conflicts']:
        print(f"   Potential Conflicts: {', '.join(leadership_hybrid['potential_conflicts'])}")
    
    # Innovation hybrid: Creative + Analytical
    innovation_hybrid = profiler.create_hybrid_profile(
        [creative_profile, analytical_profile],
        [0.7, 0.3],
        'innovation'
    )
    
    print(f"\n✅ Innovation Hybrid: {innovation_hybrid['cognitive_signature']}")
    print(f"   Source: {creative_profile['cognitive_signature']} (70%) + {analytical_profile['cognitive_signature']} (30%)")
    print(f"   Strengths: {', '.join(innovation_hybrid['hybrid_strengths'][:3])}")
    if innovation_hybrid['optimization_suggestions']:
        print(f"   Optimization: {innovation_hybrid['optimization_suggestions'][0]}")
    
    # Problem-solving hybrid: All three profiles
    problem_solving_hybrid = profiler.create_hybrid_profile(
        [analytical_profile, creative_profile, intuitive_profile],
        [0.4, 0.3, 0.3],
        'problem_solving'
    )
    
    print(f"\n✅ Problem-Solving Hybrid: {problem_solving_hybrid['cognitive_signature']}")
    print(f"   Source: 3-way blend (40%/30%/30%)")
    print(f"   Strengths: {', '.join(problem_solving_hybrid['hybrid_strengths'][:3])}")
    
    # Save hybrid profiles
    manager.save_profile(leadership_hybrid)
    manager.save_profile(innovation_hybrid)
    manager.save_profile(problem_solving_hybrid)
    
    print(f"\n3. Profile Management Demo...")
    print("-" * 30)
    
    # Show profile statistics
    stats = manager.get_profile_stats()
    print(f"📊 Profile Statistics:")
    print(f"   Total Profiles: {stats['total_profiles']}")
    print(f"   Individual: {stats['individual_profiles']}")
    print(f"   Hybrid: {stats['hybrid_profiles']}")
    print(f"   Storage: {stats['storage_size_mb']} MB")
    
    # List all profiles
    print(f"\n📋 All Profiles:")
    profiles = manager.list_profiles()
    for profile in profiles:
        profile_type = "🧠" if profile['profile_type'] == 'individual' else "🔀"
        print(f"   {profile_type} {profile['profile_id'][:20]}... | {profile['cognitive_signature']} | {profile['use_case']}")
    
    # Find compatible profiles
    print(f"\n🔍 Compatibility Analysis:")
    compatible = manager.find_compatible_profiles(analytical_profile, 0.5)
    print(f"   Profiles compatible with {analytical_profile['cognitive_signature']}:")
    for comp in compatible[:2]:
        print(f"   • {comp['profile_id'][:20]}... (Score: {comp['compatibility_score']:.2f})")
    
    print(f"\n4. Export Demo...")
    print("-" * 30)
    
    # Export a profile to text format
    export_path = "/tmp/sample_profile.txt"
    manager.export_profile(leadership_hybrid['profile_id'], export_path, 'txt')
    
    print(f"\n📄 Sample Profile Export (first 10 lines):")
    with open(export_path, 'r') as f:
        lines = f.readlines()[:10]
        for line in lines:
            print(f"   {line.rstrip()}")
    
    print(f"\n🎉 Demo Complete!")
    print("=" * 50)
    print("Key Features Demonstrated:")
    print("✅ Individual profile generation from assessment data")
    print("✅ Hybrid profile creation with multiple blending strategies")
    print("✅ Profile management (save, load, list, stats)")
    print("✅ Compatibility analysis for profile mixing")
    print("✅ Export functionality for sharing profiles")
    print("✅ Cognitive signatures for easy identification")
    print("✅ Use-case specific optimization suggestions")
    print("\nTry the CLI interface:")
    print("  python cli_chatbot.py --list-profiles")
    print("  python cli_chatbot.py --assess")
    print("  python cli_chatbot.py --create-hybrid PROF1,PROF2 0.6,0.4 leadership")

if __name__ == "__main__":
    main()
