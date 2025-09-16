
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import shutil

class ProfileManager:
    """Manages cognitive profile storage, loading, and organization."""
    
    def __init__(self, profiles_dir: Optional[str] = None):
        """Initialize profile manager with storage directory."""
        self.profiles_dir = Path(profiles_dir or os.path.expanduser("~/.neuralagent/profiles"))
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.profiles_dir / "individual").mkdir(exist_ok=True)
        (self.profiles_dir / "hybrid").mkdir(exist_ok=True)
        (self.profiles_dir / "assessments").mkdir(exist_ok=True)
    
    def save_profile(self, profile: Dict[str, Any], profile_type: str = "individual") -> str:
        """Save a cognitive profile to disk."""
        profile_id = profile.get('profile_id')
        if not profile_id:
            raise ValueError("Profile must have a profile_id")
        
        # Determine file path
        subdir = "hybrid" if profile.get('profile_type') == 'hybrid' else profile_type
        file_path = self.profiles_dir / subdir / f"{profile_id}.json"
        
        # Add metadata
        profile['saved_timestamp'] = datetime.now().isoformat()
        profile['file_path'] = str(file_path)
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(profile, f, indent=2)
        
        print(f"✅ Profile saved: {file_path}")
        return str(file_path)
    
    def load_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Load a cognitive profile by ID."""
        # Search in all subdirectories
        for subdir in ["individual", "hybrid", "assessments"]:
            file_path = self.profiles_dir / subdir / f"{profile_id}.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    profile = json.load(f)
                print(f"✅ Profile loaded: {profile_id}")
                return profile
        
        print(f"❌ Profile not found: {profile_id}")
        return None
    
    def list_profiles(self, profile_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all available profiles."""
        profiles = []
        
        # Determine which directories to search
        if profile_type:
            search_dirs = [profile_type]
        else:
            search_dirs = ["individual", "hybrid", "assessments"]
        
        for subdir in search_dirs:
            dir_path = self.profiles_dir / subdir
            if dir_path.exists():
                for file_path in dir_path.glob("*.json"):
                    try:
                        with open(file_path, 'r') as f:
                            profile = json.load(f)
                        
                        # Add summary info
                        profile_summary = {
                            'profile_id': profile.get('profile_id'),
                            'profile_type': profile.get('profile_type', subdir),
                            'creation_timestamp': profile.get('creation_timestamp'),
                            'cognitive_signature': profile.get('cognitive_signature'),
                            'file_path': str(file_path),
                            'use_case': profile.get('use_case', 'general')
                        }
                        profiles.append(profile_summary)
                    except Exception as e:
                        print(f"⚠️ Error reading profile {file_path}: {e}")
        
        return sorted(profiles, key=lambda x: x.get('creation_timestamp', ''), reverse=True)
    
    def delete_profile(self, profile_id: str) -> bool:
        """Delete a profile by ID."""
        # Search in all subdirectories
        for subdir in ["individual", "hybrid", "assessments"]:
            file_path = self.profiles_dir / subdir / f"{profile_id}.json"
            if file_path.exists():
                file_path.unlink()
                print(f"✅ Profile deleted: {profile_id}")
                return True
        
        print(f"❌ Profile not found for deletion: {profile_id}")
        return False
    
    def backup_profiles(self, backup_path: Optional[str] = None) -> str:
        """Create a backup of all profiles."""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.profiles_dir.parent / f"profiles_backup_{timestamp}"
        
        backup_path = Path(backup_path)
        shutil.copytree(self.profiles_dir, backup_path)
        
        print(f"✅ Profiles backed up to: {backup_path}")
        return str(backup_path)
    
    def restore_profiles(self, backup_path: str) -> bool:
        """Restore profiles from a backup."""
        backup_path = Path(backup_path)
        if not backup_path.exists():
            print(f"❌ Backup path not found: {backup_path}")
            return False
        
        # Create backup of current profiles
        current_backup = self.backup_profiles()
        print(f"Current profiles backed up to: {current_backup}")
        
        # Remove current profiles and restore from backup
        shutil.rmtree(self.profiles_dir)
        shutil.copytree(backup_path, self.profiles_dir)
        
        print(f"✅ Profiles restored from: {backup_path}")
        return True
    
    def find_compatible_profiles(self, target_profile: Dict[str, Any], 
                               compatibility_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Find profiles compatible for hybridization."""
        compatible_profiles = []
        target_traits = target_profile.get('cognitive_traits', {})
        
        # Get all individual profiles
        all_profiles = self.list_profiles('individual')
        
        for profile_summary in all_profiles:
            if profile_summary['profile_id'] == target_profile.get('profile_id'):
                continue  # Skip self
            
            # Load full profile
            full_profile = self.load_profile(profile_summary['profile_id'])
            if not full_profile:
                continue
            
            # Calculate compatibility score
            compatibility_score = self._calculate_compatibility(target_traits, 
                                                              full_profile.get('cognitive_traits', {}))
            
            if compatibility_score >= compatibility_threshold:
                profile_summary['compatibility_score'] = compatibility_score
                compatible_profiles.append(profile_summary)
        
        return sorted(compatible_profiles, key=lambda x: x['compatibility_score'], reverse=True)
    
    def _calculate_compatibility(self, traits1: Dict, traits2: Dict) -> float:
        """Calculate compatibility score between two trait profiles."""
        # Simple compatibility based on complementary traits
        score = 0.0
        comparisons = 0
        
        trait_pairs = [
            ('analytical_tendency', 'creative_tendency'),
            ('systematic_tendency', 'intuitive_tendency'),
            ('decision_confidence', 'cognitive_flexibility')
        ]
        
        for trait1, trait2 in trait_pairs:
            val1_1 = traits1.get(trait1, 0.5)
            val1_2 = traits1.get(trait2, 0.5)
            val2_1 = traits2.get(trait1, 0.5)
            val2_2 = traits2.get(trait2, 0.5)
            
            # Higher compatibility if one profile is strong where the other is weak
            complement_score = abs(val1_1 - val2_1) + abs(val1_2 - val2_2)
            score += complement_score
            comparisons += 2
        
        return score / comparisons if comparisons > 0 else 0.0
    
    def export_profile(self, profile_id: str, export_path: str, format: str = 'json') -> bool:
        """Export a profile to different formats."""
        profile = self.load_profile(profile_id)
        if not profile:
            return False
        
        export_path = Path(export_path)
        
        if format.lower() == 'json':
            with open(export_path, 'w') as f:
                json.dump(profile, f, indent=2)
        elif format.lower() == 'txt':
            with open(export_path, 'w') as f:
                f.write(self._profile_to_text(profile))
        else:
            print(f"❌ Unsupported export format: {format}")
            return False
        
        print(f"✅ Profile exported to: {export_path}")
        return True
    
    def _profile_to_text(self, profile: Dict[str, Any]) -> str:
        """Convert profile to human-readable text format."""
        lines = []
        lines.append(f"Cognitive Profile: {profile.get('profile_id', 'Unknown')}")
        lines.append("=" * 50)
        lines.append(f"Created: {profile.get('creation_timestamp', 'Unknown')}")
        lines.append(f"Type: {profile.get('profile_type', 'individual')}")
        lines.append(f"Signature: {profile.get('cognitive_signature', 'N/A')}")
        lines.append("")
        
        # Cognitive traits
        traits = profile.get('cognitive_traits', {})
        if traits:
            lines.append("Cognitive Traits:")
            lines.append("-" * 20)
            for key, value in traits.items():
                if isinstance(value, float):
                    lines.append(f"  {key.replace('_', ' ').title()}: {value:.2f}")
                else:
                    lines.append(f"  {key.replace('_', ' ').title()}: {value}")
            lines.append("")
        
        # Strengths
        strengths = profile.get('strengths', [])
        if strengths:
            lines.append("Strengths:")
            lines.append("-" * 20)
            for strength in strengths:
                lines.append(f"  • {strength.replace('_', ' ').title()}")
            lines.append("")
        
        # Learning preferences
        learning_prefs = profile.get('learning_preferences', {})
        if learning_prefs:
            lines.append("Learning Preferences:")
            lines.append("-" * 20)
            for key, value in learning_prefs.items():
                lines.append(f"  {key.replace('_', ' ').title()}: {value}")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_profile_stats(self) -> Dict[str, Any]:
        """Get statistics about stored profiles."""
        stats = {
            'total_profiles': 0,
            'individual_profiles': 0,
            'hybrid_profiles': 0,
            'assessment_profiles': 0,
            'storage_size_mb': 0,
            'oldest_profile': None,
            'newest_profile': None
        }
        
        # Count profiles by type
        for subdir in ["individual", "hybrid", "assessments"]:
            dir_path = self.profiles_dir / subdir
            if dir_path.exists():
                profile_count = len(list(dir_path.glob("*.json")))
                stats[f'{subdir}_profiles'] = profile_count
                stats['total_profiles'] += profile_count
        
        # Calculate storage size
        total_size = sum(f.stat().st_size for f in self.profiles_dir.rglob("*.json"))
        stats['storage_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        # Find oldest and newest profiles
        all_profiles = self.list_profiles()
        if all_profiles:
            sorted_by_date = sorted(all_profiles, key=lambda x: x.get('creation_timestamp', ''))
            stats['oldest_profile'] = sorted_by_date[0]['profile_id']
            stats['newest_profile'] = sorted_by_date[-1]['profile_id']
        
        return stats
