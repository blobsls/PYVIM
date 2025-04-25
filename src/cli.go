
package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
)

func handlePyVim() error {
	// Check if vim is installed
	_, err := exec.LookPath("vim")
	if err != nil {
		return fmt.Errorf("vim is not installed: %v", err)
	}

	// Check if python is installed
	_, err = exec.LookPath("python")
	if err != nil {
		return fmt.Errorf("python is not installed: %v", err)
	}

	// Get current working directory
	cwd, err := os.Getwd()
	if err != nil {
		return fmt.Errorf("failed to get working directory: %v", err)
	}

	// Find Python files in current directory
	pyFiles, err := filepath.Glob("*.py")
	if err != nil {
		return fmt.Errorf("failed to find Python files: %v", err)
	}

	if len(pyFiles) == 0 {
		return fmt.Errorf("no Python files found in %s", cwd)
	}

	// Launch vim with Python files
	cmd := exec.Command("vim", pyFiles...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	return cmd.Run()
}
