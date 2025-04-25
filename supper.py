
import os
import sys
from typing import List, Optional, Dict, Any
import logging

class SupperSyntaxWorker:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        self.initialize_worker()
    
    def initialize_worker(self) -> None:
        """Initialize the syntax worker with default configurations"""
        self.syntax_rules = {}
        self.parse_tree = []
        self.errors = []
        
    def add_syntax_rule(self, name: str, pattern: str, handler: callable) -> None:
        """Add a new syntax rule to the worker
        
        Args:
            name: Unique identifier for the rule
            pattern: Syntax pattern to match
            handler: Callback function to handle the pattern
        """
        self.syntax_rules[name] = {
            'pattern': pattern,
            'handler': handler
        }
        
    def parse(self, content: str) -> List[Any]:
        """Parse content according to defined syntax rules
        
        Args:
            content: Input string to parse
            
        Returns:
            List of parsed elements
        """
        try:
            for rule_name, rule in self.syntax_rules.items():
                matches = rule['pattern'].findall(content)
                for match in matches:
                    result = rule['handler'](match)
                    self.parse_tree.append(result)
            return self.parse_tree
        except Exception as e:
            self.logger.error(f"Error parsing content: {str(e)}")
            self.errors.append(str(e))
            return []
            
    def validate(self) -> bool:
        """Validate the parsed content against syntax rules
        
        Returns:
            Boolean indicating if validation passed
        """
        return len(self.errors) == 0
        
    def get_errors(self) -> List[str]:
        """Get list of errors encountered during parsing
        
        Returns:
            List of error messages
        """
        return self.errors
        
    def clear(self) -> None:
        """Reset the worker state"""
        self.parse_tree = []
        self.errors = []
