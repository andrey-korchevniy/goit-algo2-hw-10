import random
import time
import matplotlib.pyplot as plt
import numpy as np


def deterministic_partition(arr, low, high):
    """
    Partition function for deterministic QuickSort.
    Uses the last element as pivot.
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def randomized_partition(arr, low, high):
    """
    Partition function for randomized QuickSort.
    Uses a randomly selected element as pivot.
    """
    # Choose random pivot and swap with last element
    random_index = random.randint(low, high)
    arr[random_index], arr[high] = arr[high], arr[random_index]
    
    # Use deterministic partition with randomly chosen pivot
    return deterministic_partition(arr, low, high)


def deterministic_quick_sort_helper(arr, low, high):
    """Helper function for deterministic QuickSort"""
    if low < high:
        pi = deterministic_partition(arr, low, high)
        deterministic_quick_sort_helper(arr, low, pi - 1)
        deterministic_quick_sort_helper(arr, pi + 1, high)


def randomized_quick_sort_helper(arr, low, high):
    """Helper function for randomized QuickSort"""
    if low < high:
        pi = randomized_partition(arr, low, high)
        randomized_quick_sort_helper(arr, low, pi - 1)
        randomized_quick_sort_helper(arr, pi + 1, high)


def deterministic_quick_sort(arr):
    """
    Deterministic QuickSort implementation.
    Uses the last element as pivot.
    """
    arr_copy = arr.copy()
    deterministic_quick_sort_helper(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def randomized_quick_sort(arr):
    """
    Randomized QuickSort implementation.
    Uses a randomly selected element as pivot.
    """
    arr_copy = arr.copy()
    randomized_quick_sort_helper(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def generate_test_array(size):
    """Generate random array of given size"""
    return [random.randint(1, 1000000) for _ in range(size)]


def measure_time(sort_function, arr, iterations=5):
    """
    Measure average execution time of sorting function
    over multiple iterations.
    """
    total_time = 0
    
    for _ in range(iterations):
        test_arr = arr.copy()
        start_time = time.time()
        sort_function(test_arr)
        end_time = time.time()
        total_time += (end_time - start_time)
    
    return total_time / iterations


def run_performance_test():
    """Run performance comparison between algorithms"""
    # Test array sizes
    sizes = [10000, 50000, 100000, 500000]
    
    # Results storage
    randomized_times = []
    deterministic_times = []
    
    print("Порівняння рандомізованого та детермінованого QuickSort")
    print("=" * 60)
    
    for size in sizes:
        print(f"\nРозмір масиву: {size}")
        
        # Generate test array
        test_array = generate_test_array(size)
        
        # Measure randomized QuickSort
        random_time = measure_time(randomized_quick_sort, test_array)
        randomized_times.append(random_time)
        print(f"   Рандомізований QuickSort: {random_time:.4f} секунд")
        
        # Measure deterministic QuickSort
        deterministic_time = measure_time(deterministic_quick_sort, test_array)
        deterministic_times.append(deterministic_time)
        print(f"   Детермінований QuickSort: {deterministic_time:.4f} секунд")
    
    return sizes, randomized_times, deterministic_times


def create_performance_graph(sizes, randomized_times, deterministic_times):
    """Create performance comparison graph"""
    plt.figure(figsize=(12, 8))
    
    # Plot lines
    plt.plot(sizes, randomized_times, 'b-o', label='Рандомізований QuickSort', linewidth=2, markersize=6)
    plt.plot(sizes, deterministic_times, 'r-s', label='Детермінований QuickSort', linewidth=2, markersize=6)
    
    # Customize graph
    plt.xlabel('Розмір масиву', fontsize=12)
    plt.ylabel('Середній час виконання (секунди)', fontsize=12)
    plt.title('Порівняння рандомізованого та детермінованого QuickSort', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Format axes
    plt.ticklabel_format(style='plain', axis='x')
    
    # Add some styling
    plt.tight_layout()
    
    # Show and save graph
    plt.show()
    plt.savefig('quicksort_comparison.png', dpi=300, bbox_inches='tight')


def analyze_results(sizes, randomized_times, deterministic_times):
    """Analyze and print conclusions about the results"""
    print("\n" + "=" * 60)
    print("АНАЛІЗ РЕЗУЛЬТАТІВ")
    print("=" * 60)
    
    print("\n1. Порівняння часу виконання:")
    print("-" * 40)
    
    total_random = sum(randomized_times)
    total_deterministic = sum(deterministic_times)
    
    for i, size in enumerate(sizes):
        diff = deterministic_times[i] - randomized_times[i]
        diff_percent = (diff / randomized_times[i]) * 100
        print(f"   Розмір {size:6d}: різниця {diff:+.4f}с ({diff_percent:+.1f}%)")
    
    print(f"\n2. Загальна продуктивність:")
    print("-" * 40)
    print(f"   Загальний час рандомізованого: {total_random:.4f}с")
    print(f"   Загальний час детермінованого: {total_deterministic:.4f}с")
    
    if total_random < total_deterministic:
        faster = "рандомізований"
        diff = total_deterministic - total_random
    else:
        faster = "детермінований"
        diff = total_random - total_deterministic
    
    print(f"   Швидший алгоритм: {faster} (на {diff:.4f}с)")
    
    print(f"\n3. Висновки:")
    print("-" * 40)
    print("   • Обидва алгоритми показують схожу продуктивність")
    print("   • Рандомізований QuickSort менш схильний до найгірших випадків")
    print("   • Детермінований QuickSort більш передбачуваний у виконанні")
    print("   • На великих масивах різниця може бути більш помітною")
    print("   • Рандомізований підхід рекомендується для загального використання")


def test_correctness():
    """Test if both sorting algorithms work correctly"""
    print("Тестування коректності алгоритмів...")
    
    # Test case 1: Small array
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    expected = sorted(test_arr)
    
    random_result = randomized_quick_sort(test_arr)
    deterministic_result = deterministic_quick_sort(test_arr)
    
    assert random_result == expected, "Рандомізований QuickSort працює неправильно!"
    assert deterministic_result == expected, "Детермінований QuickSort працює неправильно!"
    
    # Test case 2: Already sorted array
    test_arr2 = [1, 2, 3, 4, 5]
    expected2 = [1, 2, 3, 4, 5]
    
    assert randomized_quick_sort(test_arr2) == expected2
    assert deterministic_quick_sort(test_arr2) == expected2
    
    # Test case 3: Reverse sorted array
    test_arr3 = [5, 4, 3, 2, 1]
    expected3 = [1, 2, 3, 4, 5]
    
    assert randomized_quick_sort(test_arr3) == expected3
    assert deterministic_quick_sort(test_arr3) == expected3
    
    print("✓ Всі тести пройдені успішно!")


def main():
    """Main function to run the complete analysis"""
    # Set random seed for reproducible results in testing
    random.seed(42)
    
    # Test correctness first
    test_correctness()
    
    # Run performance tests
    sizes, randomized_times, deterministic_times = run_performance_test()
    
    # Create visualization
    create_performance_graph(sizes, randomized_times, deterministic_times)
    
    # Analyze results
    analyze_results(sizes, randomized_times, deterministic_times)


if __name__ == "__main__":
    main() 