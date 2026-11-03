# Clone and publish the ImmunoSSM repository with GitHub Desktop

## A. Download and extract the source package

1. Download `ImmunoSSM-R2-Research-Repository.zip`.
2. In Windows File Explorer, right-click the ZIP and select **Extract All**.
3. Keep the extracted folder available. Do not upload the ZIP as one file.

## B. Clone your existing GitHub repository into a new local folder

1. Open GitHub Desktop.
2. Choose **File → Clone repository…** or **Clone a repository from the Internet…**.
3. Select the **URL** tab.
4. Enter the URL of your existing repository:
   `https://github.com/YOUR-USERNAME/ImmunoSSM-Precision-Sepsis-Treatment-Optimization.git`
5. For **Local path**, choose a new, empty folder, for example:
   `Documents/GitHub/ImmunoSSM-Precision-Sepsis-Treatment-Optimization`
6. Click **Clone**.
7. In GitHub Desktop, choose **Repository → Show in Explorer**. This opens the newly cloned local repository.

## C. Copy the project files into the cloned repository

1. Open the extracted `ImmunoSSM-R2-Research-Repository` folder.
2. Select all files and folders inside it.
3. Copy them into the cloned repository folder opened in Step B.
4. If Windows reports that files with the same names already exist, do not make a rushed choice. The package's `README.md`, configuration files, and source files are the reviewed versions intended to update the earlier starter files. Choose **Replace the files in the destination** for those matching project files only. Do not replace or delete the hidden `.git` folder.
5. Confirm that the repository root contains `README.md`, `configs`, `data`, `docs`, `scripts`, `src`, and `tests`.

## D. Commit and push

1. Return to GitHub Desktop.
2. Review the changed-file list.
3. Enter this summary: `Align ImmunoSSM repository with R2 research workflow`.
4. Click **Commit to main**.
5. Click **Push origin**.
6. Open the GitHub repository in your browser and check that the folders appear.

## E. Important

- Do not upload MIMIC-IV/eICU-CRD data, patient-level extracts, credentials, model checkpoints, or fabricated results.
- The repository contains a research implementation scaffold. Read `IMPLEMENTATION_STATUS.md` before describing it as a complete reproduction.
- Values shown in configuration files are either explicitly reported in the manuscript or left null pending verification. Do not guess missing settings.
