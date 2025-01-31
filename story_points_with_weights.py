# Define the Fibonacci sequence up to a reasonable range for story points
fibonacci_sequence = [0, 1, 2, 3, 5, 8, 13, 21]

# Function to find the closest Fibonacci number
def closest_fibonacci(n):
    closest = fibonacci_sequence[0]
    for num in fibonacci_sequence:
        if abs(num - n) < abs(closest - n):
            closest = num
    return closest

# Mapping from scale to numeric value
scale_mapping = {
    'low': 1,
    'medium': 2,
    'high': 3
}

# Get weights from the user
print("Enter the weightings for each input as percentages (they should add up to 100%).")
complexity_weight = float(input("Enter the weight for complexity: "))
effort_weight = float(input("Enter the weight for effort: "))
risk_weight = float(input("Enter the weight for risk: "))
dependencies_weight = float(input("Enter the weight for dependencies: "))

# Ensure the weights add up to 100%
if complexity_weight + effort_weight + risk_weight + dependencies_weight != 100:
    print("The weights do not add up to 100%. Please adjust the weights.")
    exit()

# Get inputs from the user
complexity = input("Enter the complexity (low, medium, high): ").lower()
effort = input("Enter the effort (low, medium, high): ").lower()
risk = input("Enter the risk (low, medium, high): ").lower()
dependencies = input("Enter the dependencies (low, medium, high): ").lower()

# Convert inputs to numeric values
complexity_value = scale_mapping.get(complexity, 0)
effort_value = scale_mapping.get(effort, 0)
risk_value = scale_mapping.get(risk, 0)
dependencies_value = scale_mapping.get(dependencies, 0)

# Calculate the weighted sum of the values
weighted_sum = (complexity_value * complexity_weight +
                effort_value * effort_weight +
                risk_value * risk_weight +
                dependencies_value * dependencies_weight) / 100

# Find the closest Fibonacci number
story_points = closest_fibonacci(weighted_sum)

# Output the result
print(f"The estimated story points are: {story_points}")
