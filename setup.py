from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements.txt file and returns a list of dependencies.
    Removes '-e .' if present to prevent installation loops.
    """
    requirements = []
    with open(file_path, "r") as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements

setup(
    name="ecommerce_recommender",
    version="0.0.1",
    author="Mohammed Hamid",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)