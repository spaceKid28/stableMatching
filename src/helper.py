import numpy as np
import matplotlib.pyplot as plt
import random

class Solution:
  def __init__(self):
      pass
  # Problem 1

  def run_da(self, n):
      # for n doctors and n hospitals, randomly generate their preferences
      def generate_random_preferences(k):
          doctors_preferences = [random.sample(range(k), k) for _ in range(k)]
          hospital_preferences = [random.sample(range(k), k) for _ in range(k)]
          return doctors_preferences, hospital_preferences
      
      doct_pref, hosp_pref = generate_random_preferences(n)
      # Track which preference index each doctor is currently considering
      preference_index = [0 for _ in range(n)]
      # list of integers that represents who each hospital is currently matched to
      # ith integer represents the doctor the ith hospital is matched to. Unmatched hospital is -1
      hospitals_matched_doctor = [-1 for _ in range(n)]

      

      # We are guarenteed at least one stable matching. Therefore, we will continue proposing until the number of matches == n
      matches = 0
      proposal_count = 0
      while matches < n:
        for doctor in range(n):
            # Skip if doctor is already matched
            if doctor in hospitals_matched_doctor:
                continue
            
            # Get the next hospital this doctor will propose to
            hospital = doct_pref[doctor][preference_index[doctor]]
            # here we keep track of number of proposals
            proposal_count += 1

            # Check if hospital is unmatched
            if hospitals_matched_doctor[hospital] == -1:
                hospitals_matched_doctor[hospital] = doctor
                matches += 1
            else:
                # If hospital is matched, check if current doctor is preferred
                current_doctor = hospitals_matched_doctor[hospital]
                current_doctor_rank = hosp_pref[hospital].index(current_doctor)
                new_doctor_rank = hosp_pref[hospital].index(doctor)
                
                # Lower index means higher preference
                if new_doctor_rank < current_doctor_rank:
                    # New doctor is preferred, update matching
                    hospitals_matched_doctor[hospital] = doctor
                    
                    # Current doctor becomes unmatched and needs to try next hospital
                    preference_index[current_doctor] += 1
                    # matches count stays the same as we replaced one doctor with another
                else:
                    # Hospital prefers current match, doctor needs to try next hospital
                    preference_index[doctor] += 1
            
      return proposal_count
  
  # Count the number of proposals for doctor-hospitals sizes n = 10, 50, 100, 500, 10000
  # For each 
  def plot_proposals_vs_n(self):
    """
    Plot the average number of proposals as a function of n,
    using 5 runs for each of 5 well-spread values of n.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Define 5 well-spread values of n
    n_values = [10, 50, 100, 500, 1000]
    
    # Number of runs for each n
    num_runs = 5
    
    # Collect average proposals for each n
    avg_proposals = []
    
    for n in n_values:
        total_proposals = 0
        for _ in range(num_runs):
            total_proposals += self.run_da(n)
        avg = total_proposals / num_runs
        avg_proposals.append(avg)
        print(f"n = {n}: Average proposals = {avg}")
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, avg_proposals, 'o-', linewidth=2, label='Calculated Average (5 samples)')
    
    # Add theoretical n ln n curve
    x = np.array(n_values)
    plt.plot(x, x * np.log(x), '--', label='n ln n')
    
    plt.title('Average Number of Proposals in DA Algorithm')
    plt.xlabel('n = number of doctors/hospitals')
    plt.ylabel('Average Number of Proposals')
    plt.grid(True)
    plt.legend()
  
    
    # Add annotation about the asymptotic behavior
    plt.figtext(0.5, 0.01, 
                "The number of proposals is asymptotic to n ln n as shown in Pittel's paper",
                ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('proposals_vs_n.png')
    plt.show()
    
    return n_values, avg_proposals
  
  def plot_proposals_distribution(self, n = 500, num_instances=100):
    """
    Plot the distribution of the total number of proposals for a fixed value of n
    over several input instances.
    
    Parameters:
    - n: The fixed number of doctors and hospitals.
    - num_instances: The number of input instances to run the DA algorithm.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Collect the total number of proposals for each instance
    proposals = []
    x =0
    for _ in range(num_instances):
        print(x)
        x += 1
        total_proposals = self.run_da(n)
        proposals.append(total_proposals)

    # Plot the histogram of the proposals
    plt.figure(figsize=(10, 6))
    plt.hist(proposals, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title(f'Distribution of Total Proposals for n = {n} ({num_instances} Instances)')
    plt.xlabel('Total Number of Proposals')
    plt.ylabel('Frequency')
    plt.grid(True)

    # Add mean and standard deviation as annotations
    mean_proposals = np.mean(proposals)
    std_proposals = np.std(proposals)
    plt.axvline(mean_proposals, color='red', linestyle='dashed', linewidth=1, label=f'Mean = {mean_proposals:.2f}')
    plt.axvline(mean_proposals + std_proposals, color='green', linestyle='dashed', linewidth=1, label=f'+1 Std Dev = {mean_proposals + std_proposals:.2f}')
    plt.axvline(mean_proposals - std_proposals, color='green', linestyle='dashed', linewidth=1, label=f'-1 Std Dev = {mean_proposals - std_proposals:.2f}')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'proposals_distribution_n{n}.png')
    plt.show()

    return proposals
