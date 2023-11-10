import numpy as np

# Function to generate a random 3D rotation matrix
def random_rotation_matrix():
    random_matrix = np.random.rand(3, 3)
    u, _, vt = np.linalg.svd(random_matrix)
    rotation_matrix = u @ vt
    return rotation_matrix

# Number of random matrices to generate
num_matrices = 10000

# Generate a list of random rotation matrices
random_matrices = [random_rotation_matrix() for _ in range(num_matrices)]

# Compute the average matrix
average_matrix = np.mean(random_matrices, axis=0)

# Subtract each matrix from the average matrix
result_matrices = [matrix - average_matrix for matrix in random_matrices]

# Check if the result matrices are invertible
invertible_count = sum(np.linalg.matrix_rank(matrix) == 3 for matrix in result_matrices)

print(f"Number of invertible result matrices: {invertible_count} out of {num_matrices}")