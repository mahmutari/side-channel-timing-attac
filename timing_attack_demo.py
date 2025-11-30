"""
Side-Channel Attack Project: Timing Attack Demonstration
This program demonstrates timing attacks on password verification systems.

Author: Student Project
Course: Introduction to Cryptology
Date: 2025
"""

import time
import statistics
import random
import string

class PasswordChecker:
    """
    A class to demonstrate vulnerable and secure password checking methods.
    """
    
    def __init__(self, correct_password):
        """
        Initialize with a correct password to check against.
        
        Args:
            correct_password (str): The secret password to protect
        """
        self.correct_password = correct_password
    
    def vulnerable_check(self, input_password):
        """
        VULNERABLE: Character-by-character comparison with early exit.
        This implementation is vulnerable to timing attacks because it returns
        immediately when it finds the first incorrect character.
        
        Args:
            input_password (str): Password attempt to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        # Check length first
        if len(input_password) != len(self.correct_password):
            return False
        
        # Compare character by character - STOPS at first mismatch
        for i in range(len(self.correct_password)):
            if input_password[i] != self.correct_password[i]:
                return False  # TIMING LEAK: Returns immediately!
        
        return True
    
    def secure_check(self, input_password):
        """
        SECURE: Constant-time comparison that always checks all characters.
        This implementation is resistant to timing attacks because it always
        takes the same amount of time regardless of input.
        
        Args:
            input_password (str): Password attempt to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        # Normalize length to prevent length-based timing leaks
        if len(input_password) != len(self.correct_password):
            # Pad to correct length to maintain constant time
            input_password = input_password.ljust(len(self.correct_password), '\0')
        
        # Use bitwise OR to accumulate differences without early exit
        result = 0
        for i in range(len(self.correct_password)):
            # XOR reveals differences, OR accumulates them
            result |= ord(input_password[i]) ^ ord(self.correct_password[i])
        
        # Always completes all comparisons before returning
        return result == 0


def measure_execution_time(func, *args, iterations=1000):
    """
    Measure the average execution time of a function over multiple iterations.
    
    Args:
        func: Function to measure
        *args: Arguments to pass to the function
        iterations (int): Number of times to run the function
        
    Returns:
        tuple: (average_time, all_times) in nanoseconds
    """
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter_ns()
        func(*args)
        end = time.perf_counter_ns()
        times.append(end - start)
    
    avg_time = statistics.mean(times)
    return avg_time, times


def generate_password_attempts(correct_password, num_correct_chars):
    """
    Generate a password attempt with specified number of correct characters.
    
    Args:
        correct_password (str): The actual password
        num_correct_chars (int): How many characters should be correct (from start)
        
    Returns:
        str: Generated password attempt
    """
    if num_correct_chars >= len(correct_password):
        return correct_password
    
    # Take correct characters from the beginning
    attempt = correct_password[:num_correct_chars]
    
    # Fill rest with random characters (but different from correct ones)
    for i in range(num_correct_chars, len(correct_password)):
        # Get a random character that's different from the correct one
        chars = string.ascii_letters + string.digits
        random_char = random.choice(chars)
        while random_char == correct_password[i]:
            random_char = random.choice(chars)
        attempt += random_char
    
    return attempt


def timing_attack_simulation(password_length=8):
    """
    Simulate a timing attack by measuring response times for different inputs.
    
    Args:
        password_length (int): Length of the password to test
        
    Returns:
        dict: Results containing timing data for vulnerable and secure implementations
    """
    # Generate a random password
    correct_password = ''.join(random.choices(string.ascii_letters + string.digits, 
                                             k=password_length))
    
    print(f"\n{'='*70}")
    print(f"TIMING ATTACK SIMULATION")
    print(f"{'='*70}")
    print(f"Password Length: {password_length} characters")
    print(f"Correct Password (for demonstration): {correct_password}")
    print(f"{'='*70}\n")
    
    checker = PasswordChecker(correct_password)
    
    results = {
        'vulnerable': {},
        'secure': {},
        'password_length': password_length
    }
    
    # Test with different numbers of correct characters
    print("Testing VULNERABLE implementation (early exit)...")
    print(f"{'Correct Chars':<15} {'Avg Time (ns)':<20} {'Std Dev (ns)':<20}")
    print(f"{'-'*55}")
    
    for num_correct in range(password_length + 1):
        attempt = generate_password_attempts(correct_password, num_correct)
        avg_time, all_times = measure_execution_time(
            checker.vulnerable_check, 
            attempt, 
            iterations=1000
        )
        std_dev = statistics.stdev(all_times)
        
        results['vulnerable'][num_correct] = {
            'avg_time': avg_time,
            'std_dev': std_dev,
            'all_times': all_times
        }
        
        print(f"{num_correct:<15} {avg_time:<20.2f} {std_dev:<20.2f}")
    
    print(f"\n{'-'*55}\n")
    
    # Test secure implementation
    print("Testing SECURE implementation (constant-time)...")
    print(f"{'Correct Chars':<15} {'Avg Time (ns)':<20} {'Std Dev (ns)':<20}")
    print(f"{'-'*55}")
    
    for num_correct in range(password_length + 1):
        attempt = generate_password_attempts(correct_password, num_correct)
        avg_time, all_times = measure_execution_time(
            checker.secure_check, 
            attempt, 
            iterations=1000
        )
        std_dev = statistics.stdev(all_times)
        
        results['secure'][num_correct] = {
            'avg_time': avg_time,
            'std_dev': std_dev,
            'all_times': all_times
        }
        
        print(f"{num_correct:<15} {avg_time:<20.2f} {std_dev:<20.2f}")
    
    print(f"\n{'='*70}\n")
    
    return results, correct_password


def analyze_results(results):
    """
    Analyze the timing attack results and print insights.
    
    Args:
        results (dict): Results from timing_attack_simulation
    """
    print(f"\n{'='*70}")
    print(f"ANALYSIS: Timing Attack Vulnerability")
    print(f"{'='*70}\n")
    
    # Analyze vulnerable implementation
    vuln_times = [results['vulnerable'][i]['avg_time'] 
                  for i in sorted(results['vulnerable'].keys())]
    
    time_increase = vuln_times[-1] - vuln_times[0]
    correlation = statistics.correlation(
        list(range(len(vuln_times))), 
        vuln_times
    ) if len(vuln_times) > 1 else 0
    
    print("VULNERABLE Implementation:")
    print(f"  - Fastest response (0 correct): {vuln_times[0]:.2f} ns")
    print(f"  - Slowest response (all correct): {vuln_times[-1]:.2f} ns")
    print(f"  - Time increase: {time_increase:.2f} ns ({time_increase/vuln_times[0]*100:.1f}%)")
    print(f"  - Correlation coefficient: {correlation:.4f}")
    print(f"  - VERDICT: {'VULNERABLE' if correlation > 0.8 else 'POSSIBLY VULNERABLE'} to timing attacks")
    
    print()
    
    # Analyze secure implementation
    secure_times = [results['secure'][i]['avg_time'] 
                    for i in sorted(results['secure'].keys())]
    
    time_variance = max(secure_times) - min(secure_times)
    secure_correlation = statistics.correlation(
        list(range(len(secure_times))), 
        secure_times
    ) if len(secure_times) > 1 else 0
    
    print("SECURE Implementation:")
    print(f"  - Min response time: {min(secure_times):.2f} ns")
    print(f"  - Max response time: {max(secure_times):.2f} ns")
    print(f"  - Time variance: {time_variance:.2f} ns ({time_variance/min(secure_times)*100:.1f}%)")
    print(f"  - Correlation coefficient: {secure_correlation:.4f}")
    print(f"  - VERDICT: {'SECURE' if abs(secure_correlation) < 0.3 else 'POSSIBLY VULNERABLE'}")
    
    print(f"\n{'='*70}\n")
    
    return {
        'vulnerable_correlation': correlation,
        'secure_correlation': secure_correlation,
        'time_increase_percentage': time_increase/vuln_times[0]*100,
        'secure_variance_percentage': time_variance/min(secure_times)*100
    }


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║          SIDE-CHANNEL ATTACK: TIMING ATTACK DEMONSTRATION          ║
    ║                                                                    ║
    ║  This program demonstrates how timing variations in password       ║
    ║  verification can leak information about the correct password.     ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run simulation with 8-character password
    results, correct_pwd = timing_attack_simulation(password_length=8)
    
    # Analyze results
    analysis = analyze_results(results)
    
    print("\nSimulation completed successfully!")
    print("Run 'python visualization.py' to generate graphs of the results.")
