# Side-Channel Attack Project: Timing Attack Demonstration

## Project Overview

This project demonstrates timing attack vulnerabilities in password verification systems and provides a secure, constant-time alternative implementation.

---

## Files Included

### Source Code
- `timing_attack_demo.py` - Main implementation with vulnerable and secure password checkers
- `visualization.py` - Generates graphs and statistical analysis

### Documentation
- `Literature_Review_Side_Channel_Attacks.docx` - Comprehensive literature review
- `Project_Report_Timing_Attack.docx` - Detailed project report with test results

### Outputs
- `timing_comparison.png` - Side-by-side comparison of implementations
- `overlay_comparison.png` - Overlay showing timing leak zone
- `distribution_plot.png` - Box plots of timing distributions
- `correlation_analysis.png` - Scatter plots with correlation analysis
- `metrics_summary.png` - Bar chart of security metrics
- `results_data.json` - Raw experimental data

---

## Requirements

### Python Dependencies
```bash
pip install matplotlib numpy --break-system-packages
```

### System Requirements
- Python 3.x
- Linux/Windows/macOS
- Minimum 2GB RAM

---

## How to Run

### 1. Run the Basic Demonstration
```bash
python3 timing_attack_demo.py
```

This will:
- Generate a random 8-character password
- Test both vulnerable and secure implementations
- Display timing results in the console
- Show statistical analysis

**Expected Output:**
- Vulnerable implementation shows increasing time with more correct characters
- Secure implementation maintains constant time
- Correlation analysis confirms vulnerability

### 2. Generate Visualizations
```bash
python3 visualization.py
```

This will:
- Run the complete simulation
- Generate all graphs (PNG files)
- Save raw data (JSON file)
- Display analysis in console

**Generated Files:**
- 5 PNG image files with different visualizations
- 1 JSON file with numerical data

---

## Understanding the Results

### Vulnerable Implementation
- **Correlation Coefficient:** Typically 0.85 - 0.98 (HIGH)
- **Time Increase:** ~90-100% from 0 to all correct characters
- **Verdict:** VULNERABLE to timing attacks

### Secure Implementation
- **Correlation Coefficient:** Typically < 0.3 (LOW)
- **Time Variance:** ~3-5% across all test cases
- **Verdict:** SECURE against timing attacks

---

## Key Concepts Demonstrated

### Timing Attack Vulnerability
The vulnerable implementation uses character-by-character comparison with early exit:
```python
for i in range(len(password)):
    if input[i] != correct[i]:
        return False  # STOPS HERE - timing leak!
```

### Constant-Time Mitigation
The secure implementation always checks all characters:
```python
result = 0
for i in range(len(password)):
    result |= ord(input[i]) ^ ord(correct[i])
return result == 0  # Always completes full loop
```

---

## Test Methodology

1. **Password Generation:** Random 8-character password
2. **Test Cases:** 0 through 8 correct characters
3. **Iterations:** 1000 measurements per test case
4. **Timing:** Nanosecond precision using `time.perf_counter_ns()`
5. **Analysis:** Statistical correlation and variance analysis

---

## Interpretation Guide

### Reading the Graphs

**Timing Comparison (Figure 1):**
- Left panel: Vulnerable - upward trend
- Right panel: Secure - flat line

**Overlay Comparison (Figure 2):**
- Yellow zone: Information leak area
- Red line: Vulnerable (rising)
- Green line: Secure (flat)

**Distribution Plot (Figure 3):**
- Shows spread of measurements
- Vulnerable: Increasing medians
- Secure: Consistent medians

**Correlation Analysis (Figure 4):**
- Scatter shows all 1000 measurements
- Line shows average trend
- Strong positive slope = vulnerable

**Metrics Summary (Figure 5):**
- Compares key security metrics
- Lower values = more secure

---

## Real-World Implications

### Attack Complexity Reduction
- **Brute Force:** 62^8 ≈ 2.18 × 10^14 attempts
- **Timing Attack:** 8 × 62 = 496 attempts
- **Reduction:** Over 10 orders of magnitude

### Affected Systems
- Password verification APIs
- Authentication systems
- Cryptographic key comparison
- Token validation

---

## Security Recommendations

1. ✅ Always use constant-time comparison for secrets
2. ✅ Avoid conditional branches on secret values
3. ✅ Use bitwise operations for equality testing
4. ✅ Implement rate limiting
5. ✅ Conduct timing analysis in security audits
6. ✅ Use established cryptographic libraries

---

## Troubleshooting

### Issue: Import errors
**Solution:** Install required packages:
```bash
pip install matplotlib numpy --break-system-packages
```

### Issue: Permission denied
**Solution:** Run with appropriate permissions or use virtual environment

### Issue: No graphs generated
**Solution:** Check that output directory exists and is writable

---

## References

See `Literature_Review_Side_Channel_Attacks.docx` for complete references including:
- Brumley & Boneh (2003) - Remote Timing Attacks
- Kocher et al. (2011) - Differential Power Analysis
- ACM and IEEE survey papers on side-channel attacks

---

## Project Structure

```
timing-attack-project/
├── timing_attack_demo.py          # Main implementation
├── visualization.py                # Graph generation
├── README.md                       # This file
└── outputs/
    ├── timing_comparison.png
    ├── overlay_comparison.png
    ├── distribution_plot.png
    ├── correlation_analysis.png
    ├── metrics_summary.png
    └── results_data.json
```

---



**Note:** This implementation is for educational demonstration only. For production systems, use well-tested cryptographic libraries with constant-time guarantees.
