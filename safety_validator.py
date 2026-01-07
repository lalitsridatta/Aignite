"""Safety validation module to ensure responses comply with constraints."""

import re
from typing import Tuple, List


class SafetyValidator:
    """Validates responses to ensure they comply with safety constraints."""
    
    def __init__(self):
        # Patterns that indicate legal advice (should be flagged)
        self.legal_advice_patterns = [
            r'\byou should\b',
            r'\byou must\b',
            r'\bi recommend\b',
            r'\bi suggest\b',
            r'\byour case\b',
            r'\byour situation\b',
            r'\bfile a lawsuit\b',
            r'\bsue\b.*\bfor\b',
            r'\bwin.*case\b',
            r'\blose.*case\b',
            r'\blikely outcome\b',
            r'\bprobably\b.*\bwin\b',
            r'\bchances of\b.*\bsuccess\b'
        ]
        
        # Patterns that indicate proper procedural explanations (good)
        self.procedural_patterns = [
            r'\bprocess involves\b',
            r'\bsteps include\b',
            r'\bprocedure is\b',
            r'\btypically\b.*\bprocess\b',
            r'\bgeneral steps\b',
            r'\busually requires\b',
            r'\bstandard procedure\b'
        ]
        
        # Required disclaimers
        self.required_disclaimers = [
            "based on",
            "according to",
            "documents",
            "procedure",
            "process"
        ]
    
    def validate_response(self, response: str, query: str) -> Tuple[bool, List[str], str]:
        """
        Validate a response for safety compliance.
        
        Returns:
            - is_safe: Boolean indicating if response is safe
            - warnings: List of warning messages
            - safe_response: Modified response if needed
        """
        warnings = []
        is_safe = True
        safe_response = response
        
        # Check for legal advice patterns
        for pattern in self.legal_advice_patterns:
            if re.search(pattern, response.lower()):
                warnings.append(f"Potential legal advice detected: {pattern}")
                is_safe = False
        
        # Check if response is too specific to individual cases
        if self._is_case_specific(query, response):
            warnings.append("Response may be too case-specific")
            is_safe = False
        
        # Check for predictions or outcomes
        if self._contains_predictions(response):
            warnings.append("Response contains predictions or outcome assessments")
            is_safe = False
        
        # If unsafe, generate a safer response
        if not is_safe:
            safe_response = self._generate_safe_fallback(query)
        
        return is_safe, warnings, safe_response
    
    def _is_case_specific(self, query: str, response: str) -> bool:
        """Check if response is too specific to individual cases."""
        case_specific_indicators = [
            "your case", "your situation", "your lawsuit", "your claim",
            "in your instance", "for your matter"
        ]
        
        return any(indicator in response.lower() for indicator in case_specific_indicators)
    
    def _contains_predictions(self, response: str) -> bool:
        """Check if response contains predictions or outcome assessments."""
        prediction_patterns = [
            r'\bwill win\b', r'\bwill lose\b', r'\blikely to\b.*\bwin\b',
            r'\bchances are\b', r'\bprobably\b.*\bsucceed\b',
            r'\bexpect.*outcome\b', r'\bpredict\b'
        ]
        
        return any(re.search(pattern, response.lower()) for pattern in prediction_patterns)
    
    def _generate_safe_fallback(self, query: str) -> str:
        """Generate a safe fallback response."""
        return (
            "I can only provide general information about court procedures based on "
            "the available documents. For specific legal advice or case guidance, "
            "please consult with a qualified attorney. If you have questions about "
            "general court processes or procedures, I'd be happy to explain those "
            "based on the court documents I have access to."
        )
    
    def validate_query(self, query: str) -> Tuple[bool, str]:
        """
        Validate if a query is appropriate for the system.
        
        Returns:
            - is_appropriate: Boolean indicating if query is appropriate
            - message: Response message if query is inappropriate
        """
        inappropriate_patterns = [
            r'\bmy case\b', r'\bmy lawsuit\b', r'\bmy situation\b',
            r'\bshould i sue\b', r'\bwill i win\b', r'\bcan i sue\b',
            r'\bhow much.*damages\b', r'\bwhat are my chances\b'
        ]
        
        for pattern in inappropriate_patterns:
            if re.search(pattern, query.lower()):
                return False, (
                    "I can only explain general court procedures and processes. "
                    "For questions about specific cases or legal advice, please "
                    "consult with a qualified attorney."
                )
        
        return True, ""