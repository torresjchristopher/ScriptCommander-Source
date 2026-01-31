"""Configuration for RIGHT SHIFT - Speech-to-Text"""

class STTConfig:
    """Speech-to-Text configuration"""
    mic_timeout = 5  # seconds
    energy_threshold = 300  # ultra-sensitive
    language = 'en-US'
    dynamic_energy_threshold = False
