""" User inputs: Initial Debt-to-GDP Ratio (%), Effective Interest Rate (%), Expected GDP Growth (%), 
                Primary Deficit (%), Simulation Length (years)
"""
def ask_number(prompt, default, min_value=None, max_value=None, whole=False):
    #   Asks for a number (float or int). Press Enter to accept default.
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            value = int(raw) if whole else float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return value

def ask_yes_no(prompt):
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please type y or n.")
        
def get_user_inputs(defaults=None):
    if defaults is None:
        defaults = {
            "initial_debt": 100.0,
            "interest_rate": 3.0,
            "growth_rate": 4.0,
            "primary_deficit": 3.0,
            "years": 30,
        }
    return {
        "initial_debt":    ask_number("Initial Debt-to-GDP Ratio (%)", defaults["initial_debt"], min_value=0),
        "interest_rate":   ask_number("Effective Interest Rate (%)", defaults["interest_rate"], min_value=-5, max_value=50),
        "growth_rate":     ask_number("Expected GDP Growth (%)", defaults["growth_rate"], min_value=-50.0, max_value=50.0),
        "primary_deficit": ask_number("Primary Deficit (%)", defaults["primary_deficit"], min_value=-20.0, max_value=30.0),
        "years":           ask_number("Simulation Length (years)", defaults["years"], min_value=1, max_value=200, whole=True),
    }


