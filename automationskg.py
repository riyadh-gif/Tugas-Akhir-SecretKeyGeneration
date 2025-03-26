import subprocess
import time
import os


extracted_folder = 'E:/PENS/Semester 8/Final TA/Code/Ruang Eksperimen/experimen 1/Percobaan_2/'


scripts_to_run = [
    "kalmanfilter_experiment.py",
    "thresholding_experiment.py",
    "splitthersholding.py",
    "BCH_Alice_doss1.py",
    "BCH_Bob_doss2.py",
    "BCH_Charlie_doss3.py",
    "Universal Hash_doss1_alice.py",
    "Universal Hash_doss2_bob.py",
    "Universal Hash_doss3_charlie.py",
    "NIST-TestALICE128.c",
    "NIST-TestBOB128.c",
    "NIST-TestCharlie128.c",
    "Hash_AES_Alice_experiment.py",
    "Hash_AES_Bob_experiment.py",
    "Hash_AES_Charlie_experiment.py"
]


def execute_script(script_name):
    script_path = os.path.join(extracted_folder, script_name)
    
  
    start_time = time.time()
    
    if script_name.endswith(".py"):
   
        process = subprocess.Popen(['python3', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.communicate()  
        if script_name in ["kalmanfilter_experiment.py", "thresholding_experiment.py"]:
            
            subprocess.run(['python3', '-c', 'import matplotlib.pyplot as plt; plt.close()'])  # Close plots programmatically
    elif script_name.endswith(".c"):
        
        compiled_path = script_path.replace('.c', '.out')
        subprocess.run(['gcc', script_path, '-o', compiled_path])  # Compile C file
        
       
        process = subprocess.Popen([compiled_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.communicate(input='\n')  # Simulates pressing "Enter" key
        
    # End time
    end_time = time.time()
    execution_time = end_time - start_time
    
    
    print(f"{script_name} successfully executed in {execution_time:.2f} seconds.")
    return execution_time


total_execution_time = 0
for script in scripts_to_run:
    total_execution_time += execute_script(script)

print(f"All tasks have been completed. Total execution time: {total_execution_time:.2f} seconds.")
