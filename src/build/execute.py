
def execute_pyvim(command, args=None, cwd=None, env=None, capture_output=True):
    """Execute pyvim command with given arguments"""
    try:
        cmd = ['pyvim']
        if args:
            if isinstance(args, str):
                cmd.append(args)
            else:
                cmd.extend(args)
                
        import subprocess
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            universal_newlines=True
        )
        
        if capture_output:
            stdout, stderr = process.communicate()
            return {
                'returncode': process.returncode,
                'stdout': stdout,
                'stderr': stderr
            }
        else:
            process.wait()
            return {
                'returncode': process.returncode
            }
            
    except ImportError:
        raise RuntimeError("pyvim is not installed. Please install it using 'pip install pyvim'")
    except Exception as e:
        raise RuntimeError(f"Failed to execute pyvim command: {str(e)}")
