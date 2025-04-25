#!/usr/bin/env python3

import os
import subprocess
import argparse
import sys
from typing import List, Optional

class DockerBuilder:
    def __init__(self):
        self.dockerfile_content = """
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Pyvim
RUN pip install pyvim

# Create a non-root user
RUN useradd -m -s /bin/bash pyvim_user
RUN chown -R pyvim_user:pyvim_user /app

# Switch to non-root user
USER pyvim_user

# Set default command
CMD ["pyvim"]
"""
        self.requirements_content = """
pyvim>=3.0.0
prompt_toolkit>=3.0.0
pyflakes>=2.2.0
docopt>=0.6.2
"""

    def create_dockerfile(self, path: str = "./") -> None:
        """Create Dockerfile in specified path"""
        with open(os.path.join(path, "Dockerfile"), "w") as f:
            f.write(self.dockerfile_content.strip())

    def create_requirements(self, path: str = "./") -> None:
        """Create requirements.txt in specified path"""
        with open(os.path.join(path, "requirements.txt"), "w") as f:
            f.write(self.requirements_content.strip())

    def build_image(self, tag: str = "pyvim:latest") -> None:
        """Build Docker image"""
        try:
            subprocess.run(
                ["docker", "build", "-t", tag, "."],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(f"Successfully built Docker image: {tag}")
        except subprocess.CalledProcessError as e:
            print(f"Error building Docker image: {e.stderr.decode()}")
            sys.exit(1)

    def run_container(
        self,
        tag: str = "pyvim:latest",
        volume: Optional[str] = None,
        port_mapping: Optional[List[str]] = None,
    ) -> None:
        """Run Docker container"""
        cmd = ["docker", "run", "-it"]
        
        if volume:
            cmd.extend(["-v", volume])
        
        if port_mapping:
            for port in port_mapping:
                cmd.extend(["-p", port])
        
        cmd.append(tag)
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running Docker container: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Build and run Pyvim Docker container")
    parser.add_argument("--tag", default="pyvim:latest", help="Docker image tag")
    parser.add_argument("--volume", help="Volume mapping (host:container)")
    parser.add_argument(
        "--ports",
        nargs="+",
        help="Port mappings (host:container)",
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Only build the Docker image without running",
    )

    args = parser.parse_args()

    builder = DockerBuilder()
    
    # Create necessary files
    builder.create_dockerfile()
    builder.create_requirements()
    
    # Build Docker image
    builder.build_image(args.tag)
    
    # Run container if not build-only
    if not args.build_only:
        builder.run_container(
            tag=args.tag,
            volume=args.volume,
            port_mapping=args.ports,
        )

if __name__ == "__main__":
    main()
