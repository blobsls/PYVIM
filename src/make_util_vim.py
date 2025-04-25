
import os
import sys
from typing import Dict, List, Optional, Union
from pathlib import Path

class VimUtilityManager:
    def __init__(self):
        self.vim_runtime_path = Path.home() / '.vim'
        self.plugin_path = self.vim_runtime_path / 'plugin'
        self.autoload_path = self.vim_runtime_path / 'autoload'
        self.syntax_path = self.vim_runtime_path / 'syntax'
        
    def ensure_directories(self) -> None:
        """Ensure all necessary Vim directories exist."""
        for path in [self.vim_runtime_path, self.plugin_path, 
                    self.autoload_path, self.syntax_path]:
            path.mkdir(parents=True, exist_ok=True)
            
    def install_plugin(self, plugin_name: str, content: str) -> bool:
        """Install a plugin to the Vim plugin directory."""
        try:
            plugin_file = self.plugin_path / f"{plugin_name}.vim"
            plugin_file.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Failed to install plugin {plugin_name}: {str(e)}")
            return False
            
    def create_syntax_file(self, filetype: str, syntax_rules: List[str]) -> bool:
        """Create a syntax highlighting file."""
        try:
            syntax_file = self.syntax_path / f"{filetype}.vim"
            content = "\n".join([
                '" Vim syntax file',
                f'" Language: {filetype}',
                '" Maintainer: Auto-generated',
                '" Latest Revision: ' + str(Path.today()),
                '',
                'if exists("b:current_syntax")',
                '    finish',
                'endif',
                '',
                *syntax_rules,
                '',
                f'let b:current_syntax = "{filetype}"'
            ])
            syntax_file.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Failed to create syntax file for {filetype}: {str(e)}")
            return False
            
    def create_autoload_function(self, namespace: str, 
                               function_name: str, 
                               function_body: str) -> bool:
        """Create an autoload function."""
        try:
            autoload_file = self.autoload_path / f"{namespace}.vim"
            content = (
                f"function! {namespace}#{function_name}()\n"
                f"{function_body}\n"
                "endfunction"
            )
            autoload_file.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Failed to create autoload function: {str(e)}")
            return False
            
    def create_mapping(self, mode: str, key: str, 
                      command: str, buffer_local: bool = False) -> str:
        """Create a Vim mapping string."""
        map_cmd = 'map' if not buffer_local else 'map <buffer>'
        return f"{mode}{map_cmd} {key} {command}"
        
    def generate_vimrc_section(self, settings: Dict[str, Union[str, bool, int]]) -> str:
        """Generate a section of vimrc with provided settings."""
        lines = []
        for setting, value in settings.items():
            if isinstance(value, bool):
                lines.append(f"set {'no' if not value else ''}{setting}")
            else:
                lines.append(f"set {setting}={value}")
        return "\n".join(lines)
        
    def backup_file(self, file_path: Path) -> Optional[Path]:
        """Create a backup of a Vim configuration file."""
        try:
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            if file_path.exists():
                file_path.rename(backup_path)
                return backup_path
            return None
        except Exception as e:
            print(f"Failed to create backup: {str(e)}")
            return None
            
    def validate_vim_script(self, content: str) -> bool:
        """Basic validation of Vim script syntax."""
        try:
            # Check for basic syntax errors
            error_indicators = [
                'endif without if',
                'endwhile without while',
                'endfor without for',
                'endfunction without function'
            ]
            
            stack = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('if '):
                    stack.append('if')
                elif line.startswith('while '):
                    stack.append('while')
                elif line.startswith('for '):
                    stack.append('for')
                elif line.startswith('function'):
                    stack.append('function')
                elif line in ['endif', 'endwhile', 'endfor', 'endfunction']:
                    if not stack:
                        return False
                    stack.pop()
                    
            return len(stack) == 0
        except Exception:
            return False
