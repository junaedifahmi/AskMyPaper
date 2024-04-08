class DotConfig:
    def __init__(self, cfg):
        self._cfg = cfg
    
    def __getattr__(self, k):
        v = self._cfg[k]
        if isinstance(v, dict):
            return DotConfig(v)
        return v
    

def get_prompt(filepath):
    with open(filepath, "r") as f:
        return f.read()