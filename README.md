<<<<<<< HEAD
# homophily
This repository uses [JATOS](https://www.jatos.org/) and [jsPsych](https://www.jspsych.org/) to specify an experiment studying homophily.

**Live Experiment Demo**: https://githubpsyche.github.io/homophily/experiment/index.html

## Setup and Development

### 1. Install and Initialize JATOS

Install [JATOS](https://www.jatos.org/) and initialize by following [these](https://www.jatos.org/Installation.html) instructions.

JATOS is a bit weird when it comes to playing nice with GitHub repositories, so we have to set it up first. The installation instructions for JATOS describe how to start the server and access the web interface; the precise way is specific to your OS. You can find the instructions [here](https://www.jatos.org/Installation.html). 

Once you log in, click "New Study" in the top left of the JATOS UI. Use any name for the experiment (e.g., "My Experiment") and confirm.

On the management page for the study, click "Properties" to access study properties. We want to update your "Study assets' directory name" to the name of the repository you will be using for your study. For example, when using this repository (which we recommend when getting sarted!), you'd use its name. This will create an empty folder in the JATOS directory where you can store your study assets.

### 2. Clone the Repository

Next, we want to clone your experiment repository (usually *this* repository!) to your computer at the JATOS study assets directory you just created. 

You might not know what cloning is: it's a way to copy the files from this repository to your computer. If you are new to git and Github, I suggest using Github Desktop. [This page](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop) should provide the most up-to-date instructions for cloning a repository using GitHub Desktop. 

The right place to clone your repository is inside the JATOS folder you created. If your JATOS is installed at the path `/jatos/` and your repository is named `my_experiment`, you should clone the repository to `/jatos/study_assets_root/my_experiment`. 

**IMPORTANT**: Make sure you don't accidentally clone to `/jatos/study_assets_root/my_experiment/my_experiment`. You want to replace the pre-existing `my_experiment` folder with the contents of the repository you are cloning.

If you've cloned using Github Desktop, you should be able to open your project in Visual Studio Code by clicking "Repository" menu option and then the "Open in Visual Studio Code" button in the Github Desktop interface. 

You can similarly open the project in your file explorer by clicking the "Show in Explorer/Finder" button.

### Optional: Make a New Branch (or Experiment Directory)

If you want to make changes to the repository, it's a good idea to create a new branch. A branch is a version of the repository that extends from and exists alongside the main version. You can make changes to the branch without affecting the main version. Once you are happy with the changes, you can merge the branch back into the main version.

[Here's](https://docs.github.com/en/desktop/making-changes-in-a-branch/managing-branches-in-github-desktop) the documentation for managing branches in Github Desktop.

[Here's](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository) the documentation for managing branches right on Github.

Another less robust but understandably popular way to manage different versions of your experiment is to create a new directory in the `experiments` directory for each new experiment you want to create. This is a good way to keep experiments separate from each other and to avoid conflicts between different versions of the same experiment. For new developers, branch management is maybe a bit more complicated than it needs to be. A new directory for each experiment should be sufficient for most purposes.

### 3. Add An Experiment's HTML file to JATOS
Not every html file in your repository is automatically associated with an experiment in JATOS. You have to manually add the file to JATOS as an experiment **Component**.

Go to the JATOS web interface and click on the study you created. Click on the "+ New Component" button. Give the component a name and also the file path for the HTML file you want associated with the experiment. 

Once you do this, as long as the HTML file is in the study assets directory and has no errors, you can click "Run" to start the experiment.

### 4. Updating Your Experiment

We've organized this repository to categorize code you shouldn't have to change (like the jsPsych library) and code you should change (like the experiment's HTML file) in order to make an experiment unique to your research.

Core files are located in the `core` directory. These files are the same for every experiment you create. You shouldn't have to change them, but sometimes you might want to, particularly if implementing a custom plugin or feature.

The `experiments` directory is where you will create your experiments. Each experiment should have its own directory. Inside the experiment directory, you should have an HTML file that contains the experiment code. You can also have a CSS file and a JavaScript file if you want to separate the code into different files. When getting started, just stick to a single HTML file and don't worry about the CSS and JavaScript files.

At this point, you need to get familiar with the documentation for jsPsych to understand how to create experiments. You can find the documentation [here](https://www.jspsych.org/). Its tutorials are pretty beautiful; there's no point in me trying to outdo them here.

You can find an example experiment in the `experiments` directory. You can copy this directory and rename it to create a new experiment. You can then edit the HTML file to create your experiment.

### 5. Previewing Changes As You Code Using Live Server

We've provided functions that make it normally easy to preview your experiment without having to run it in JATOS as you code. This is the `initializeExperiment` function you see in most of the pre-existing experiment html files in the `experiments` directory. 

If you've installed the Live Server extension in Visual Studio Code, you can right-click on the HTML file you want to preview and select "Open with Live Server".

This will open a new tab in your browser with the experiment. Every time you save the HTML file, the changes will be reflected in the browser. This is a great way to see how your experiment looks as you code, streamlining the development process.

When you run an experiment outside of JATOS using our template, the data will be presented to you at the end of the experiment within your browser in the JSON format (by default) or whatever format you've configured it to be in.

While running an experiment this way, the default is usually to display arbitrary stimuli, not specific to any particular subject or condition. Managing the selection of a subject ID so that you don't repeat the same subject across different runs of the experiment requires interaction with previous runs of the experiment. This is where a backend tool like JATOS comes in. However, the exact details of how stimuli are presented/assigned and how data is saved can be customized in the experiment's JavaScript code. For your purposes, it's possible that you won't even need JATOS to run your experiment, especially if you're just testing ideas or running an in-person pilot study.

### 6. Debugging Your Experiment

In VSCode, you can use the debugger to set breakpoints in your code and step through it line by line. This is a great way to figure out what's going wrong in your experiment. It's best to rely on VSCode's [documentation](https://code.visualstudio.com/docs/editor/debugging) for how to use the debugger.

Sometimes it can be hard to tell where your breakpoints should go! When previewing an experiment, whether using Live Server or in JATOS, you can use the browser's developer tools to inspect the HTML, CSS, and JavaScript of the page. You usually can do this by right-clicking on the page and selecting "Inspect" or by pressing `Ctrl+Shift+I`. You usually also want to go to the "Console" tab to see any errors that are occurring. This will identify the number and an error code that you can use to debug your code. 

Setting breakpoints near where the error is occurring can help you figure out what's going wrong. AI tools like ChatGPT can also sometimes interpret the error code and provide a solution, particularly if you share your code with them and if the error is common.

### 7. Previewing Changes in JATOS

When you are ready to test your experiment in JATOS, use the "Run" button in the JATOS web interface. This will start the experiment in your same browser tab. If anything in your code uses JATOS-specific functions, like saving data, you will need to test it in JATOS.

If the experiment is configured properly to run in JATOS, you should see the experiment run as it would in a real study. Once the experiment finishes, the "Results" panel in JATOS for your study should include a row for the run you just completed. Under the "State" column, it should be marked as "FINISHED", rather than "FAIL" or "DATA_RETRIEVED" or something else. Clicking a dropdown arrow for your run should show you the data that was collected during the experiment.

An "Export Results" button at the top of the "Results" panel will allow you to download the data across runs in a variety of formats.

### Sharing Your Experiment Using GitHub Pages

While developing your experiment, you may want to share it with others to get feedback or to run a pilot study. You can use GitHub Pages to host your experiment online, though you won't have a JATOS backend to manage participants and data. This is usually insufficient for a real study, but it's great for testing ideas or running in-person pilot studies.

To host your experiment on GitHub Pages, first commit and then push your changes to your repository on GitHub. Here's a [guide](https://docs.github.com/en/desktop/making-changes-in-a-branch/pushing-changes-to-github-from-github-desktop) on how to do that.

This next stuff has already been done for this repository. Once your changes are on GitHub, go to the repository on GitHub and click on the "Settings" tab. Then on the left, find the "Pages" tab. You can then select the branch you want to host your site from. Usually, you want to select the `main` or `master` branch. Click "Save" and your site should be live at the URL provided, though it may take a few minutes to update.

The URL for your experiment will be `https://<your-username-or-organization-name>.github.io/<repository-name>/<path-to-your-experiment-html>`. For example, `https://githubpsyche.github.io/jspsych2150/free_recall.html` is the URL for a free recall experiment in the `jspsych2150` repository owned by `githubpsyche` located at the file path `free_recall.html` in said repository.

### 9. Sharing Your Experiment using JATOS

Once you are happy with your experiment, you can share it with others. Unless you're running experiments in person, you will need to host your experiment on a JATOS server instance that is accessible to others. 

JATOS has documentation for how to do this. You can find it [here](https://www.jatos.org/Bring-your-JATOS-online.html). Most of the solutions are kind of complicated for a first-timer, but you can always ask for help.

However, the creators of JATOS have also provided their own JATOS server that makes it especially easy to host experiments online. This service is called MindProbe and can be found [here](https://mindprobe.eu/). To host an experiment on MindProbe, you first create an account and log-in.  You'll then see a JATOS interface just like the one you have on your computer. This one is hosted on the web, and so can serve links to your experiments to anyone with the link.

To host your experiment here instead of locally, first go back to your local JATOS interface and click "Export Study" for the study you want to host. This will download a `.jzip` file that contains all your study assets and key information about your study.

Then go to the MindProbe interface and click "Import Study". You can then upload the `.jzip` file you just downloaded. This will create a study on the MindProbe server that you can run and share with others.

Now to actually share your experiment, go to "Study Links" in the MindProbe interface for your study. What to do next depends on how you want to serve your experiment. There are different options depending on if you're using MTurk or Prolific or just want to share a link. The right link also depends on whether you want the link to be reusable or not, or if you want the link to only work for one participant or an unlimited number of participants. At this point, you should consult the JATOS documentation for how to share your experiment for sure. Or talk to someone who knows how to do it!

Just as in our description of local JATOS-based development, once the experiment finishes, the "Results" panel in JATOS for your study should include a row for the run you just completed. Under the "State" column, it should be marked as "FINISHED", rather than "FAIL" or "DATA_RETRIEVED" or something else. Clicking a dropdown arrow for your run should show you the data that was collected during the experiment. An "Export Results" button at the top of the "Results" panel will allow you to download the data across runs in a variety of formats.


### Exporting Data

JATOS hosts all experiment data in an internal database.

With your experiment selected, the "Study Results" button will take you to a page where you can download the data you've collected so far. Find the "Select" section of the UI and click "All" to choose all applicable data. Failed runs of the experiment will be automatically filtered during exporting, so don't worry about excluding them manually! Once you've selected the runs you want data for, click "Export Results" and "Data Only" to then choose between downloading a zip file or text file containing your data.

Scripts in our `data/` directory contain code that will convert a file containing data from a JATOS experiment into an analyzable. You can configure the settings there to point to your data file and other relevant parameters, or ask me for help.
=======
# homophily-study
Data, code, and materials
>>>>>>> cb4523fbed762cb4a0011e35516b374fd0dc0e26
