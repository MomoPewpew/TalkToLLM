from setuptools import setup, find_packages

setup(
    name="talktollm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "sounddevice",
        "soundfile",
        "pyaudio",
        "tts",
        "realtimetts",
        "edge-tts",
    ],
    python_requires=">=3.8",
) 