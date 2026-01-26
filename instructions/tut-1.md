# Tutorial 1

## Setting Up Your Development Environment
In this tutorial, we will guide you through the process of setting up your development environment for building the _Wealth-Wise_ Dashboard. By the end of this tutorial, you will have a fully functional setup that includes an Integrated Development Environment (IDE), version control system, and a virtual environment for managing your Python packages.

### Step 1: Install Visual Studio Code (VSCode)
Visual Studio Code (VSCode) is a popular, lightweight code editor that supports a wide range of programming languages and extensions. Follow these steps to install VSCode:
1. Go to the [VSCode download page](https://code.visualstudio.com/Download).
2. Download the installer for your operating system (Windows, macOS, or Linux).
3. Run the installer and follow the on-screen instructions to complete the installation.


### Step 2: Install Python and Necessary Libraries
We will be using Python as our primary programming language. Python is widely used in the financial industry due to its simplicity and powerful libraries. We will be using a tool called Miniconda to manage our Python installation and packages.
1. Install Miniconda [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions).
2. Open a terminal (Command Prompt, PowerShell, or Terminal) and create a new virtual environment for our project:
   ```bash
   conda create --name wealth-wise python
   ```
3. Activate the virtual environment:
   ```bash
    conda activate wealth-wise
    ```
4. Install the necessary libraries for our project:
    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Set Up Git and GitHub
Git is a version control system that allows you to track changes in your code and collaborate with others. GitHub is a platform for hosting Git repositories.
1. Install Git by following the instructions on the [Git download page](https://git-scm.com/downloads).
2. Create a GitHub account if you don't have one already by visiting [GitHub](https://github.com).
3. Register your credentials in Git, make sure to replace "Your Name" and "Your Email" with your actual name and email address associated with your GitHub account:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "Your Email"
   ```
4. Fork the repository for the _Wealth-Wise_ Dashboard project from the main repository to your GitHub account, if you are reading this, you've probably already done this step.
5. Clone your forked repository to your local machine:
   ```bash
   git clone https://github.com/your-username/FSE_Tutorials.git
   ```
6. Navigate to the cloned repository and check out the `tut-1` branch:
   ```bash
   cd FSE_Tutorials
   git checkout tut-1
   ```


### Step 4: Open the Project in VSCode  
1. Open VSCode.
2. Click on "File" > "Open Folder..." and select the folder where you cloned the repository.
3. Open the integrated terminal in VSCode by clicking on "Terminal" > "New Terminal".
4. Ensure that your virtual environment is activated in the terminal. If not, activate it using:
   ```bash
   conda activate wealth-wise
   ```

### Step 5: Make Your First Commit
1. In the terminal, check the status of your repository:
   ```bash
   git status
   ```
2. Create a new file named `tutorial-1-completed.txt` in the project directory to indicate that you have completed Tutorial 1.
3. Add the new file to the staging area:
   ```bash
   git add tutorial-1-completed.txt
   ```
4. Commit your changes with a meaningful message:
   ```bash
    git commit -m "Completed Tutorial 1: Set up development environment"
    ```
5. Push your changes to your forked repository on GitHub:
   ```bash
   git push origin tut-1
   ```
Congratulations! You have successfully set up your development environment for the _Wealth-Wise_ Dashboard project. You are now ready to proceed to Tutorial 2, where we will start building the core functionality of the application.

