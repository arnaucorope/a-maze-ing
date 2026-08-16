*This project has been created as part of the 42 curriculum by acoromin and sayala-c*

# A-Maze-Ing

### 1. What part of your code is reusable, and how?
The most valuable part of this project is the **core maze engine**, which has been isolated from the execution script and delivered as a pre-compiled source distribution package (`.tar.gz`). 

Any external developer can take this archive file and install it into their independent Python projects. By importing `mazegen`, they can reuse the `MazeGenerator` class to create perfect or imperfect mathematical grids, extract matrix data, or plug it into different custom solvers without rewriting the core algorithms from scratch.

---

### 2. How to Set Up and Install the Library From Scratch

Since the `.tar.gz` package is already pre-built and included in the delivery, an external user only needs to run the following commands to install and test the library:

#### Step 1: Create the Virtual Environment
Run the automated Makefile command to set up a clean, isolated Python virtual environment:
```bash
make install
```
This command creates the .venv/ directory and prepares the environment parameters.
#### Step 2: Activate the Virtual Environment
Before installing the package, enter the newly created virtual environment:
```bash
source .venv/bin/activate
```
> *(Your terminal prompt will now show (.venv) at the beginning, confirming you are safely inside the isolated environment).*

#### Step 3: Install the Pre-built Package via pip

Install the delivered .tar.gz archive directly into your active virtual environment using pip:
```bash
pip install dist/mazegen-0.1.0.tar.gz
```
>  *(Note: Replace mazegen-0.1.0.tar.gz with the exact filename of the tar archive present in your repository).*

---
### 3. Implementation Example (How to use it)
Once the package is installed, create an independent testing file named main.py and paste the following clean code inside it:

```python
from mazegen import MazeGenerator

def main():
    maze = MazeGenerator(10, 10, (0, 0), (9, 9), True, "42")
    maze.generate()

    with open("output_maze.txt", "w") as f:
        f.write("\n".join("".join(f"{cell:X}" for cell in row) for row in maze._grid) + "\n")

if __name__ == "__main__":
    main()
```         
#### Run the test script:
To trigger the generator and write the final file, execute:
```bash
python3 main.py
```
You can check that the file output_maze.txt has been successfully created with the hexadecimal grid matrix by running:
```bash
cat output_maze.txt

