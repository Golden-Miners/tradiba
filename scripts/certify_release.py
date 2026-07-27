import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ReleaseCertification")

def run_checks():
    logger.info("Starting Release Certification Process for Tradiba v3.8")
    
    commands = [
        ("Linting (ruff)", ["ruff", "check", "."]),
        ("Type Checking (mypy)", ["mypy", "src"]),
        ("Unit Tests", ["pytest", "tests/unit"]),
        ("Integration Tests", ["pytest", "tests/integration"]),
        ("Security Tests", ["pytest", "tests/security"]),
        ("Operations Tests", ["pytest", "tests/operations"]),
    ]

    failed = False
    for name, cmd in commands:
        logger.info(f"Running: {name} ({' '.join(cmd)})")
        try:
            # Setting capture_output to avoid spamming the log if not necessary,
            # but for our CI/CD mock we'll just run them and grab the return code
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"{name} FAILED!")
                logger.error(result.stdout)
                logger.error(result.stderr)
                failed = True
            else:
                logger.info(f"{name} PASSED.")
        except Exception as e:
            logger.error(f"Failed to execute command '{cmd}': {e}")
            failed = True

    if failed:
        logger.error("Release Certification FAILED. Do not deploy to production.")
        sys.exit(1)
    else:
        logger.info("All checks passed. Release Certification SUCCESSFUL.")
        logger.info("Ready for Production Deployment.")
        sys.exit(0)

if __name__ == "__main__":
    run_checks()
