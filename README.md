# MTurkTools
This tool permits the creation of multiple Tasks of multiple HITs (images or videos) in Amazon Mechanical Turk.

## SetUp MTurk:
1) Sign in as a Requester [here](https://www.mturk.com) and create an Amazon account.
2) Create New Project [here](https://requester.mturk.com/create/projects/new) selecting Other type for the template.
3) Follow this image: ![alt text](instruction1.PNG)
4) Copy&Paste the content of [layoutImages.html](https://github.com/edoardore/MTurkTools/blob/master/layoutImages.html) in DESIGN LAYOUT (pass 2 for the creation).
5) Save.
6) Copy HITTypeID and LayoutID from: ![alt text](instruction2.PNG)
7) Paste  HITTypeID and LayoutID in [Key.py](https://github.com/edoardore/MTurkTools/blob/master/src/Key.py).

Repeat 2...7 with [layoutVideo.html](https://github.com/edoardore/MTurkTools/blob/master/layoutVideo.html).

8) Create AWS account [here](https://aws.amazon.com/it/).
9) Set up IAM console [here](https://console.aws.amazon.com/iam).
10) Follow this and click on ADD USER: ![alt text](instruction3.PNG)
11) Enter text like and press Next button. ![alt text](instruction4.PNG)
12) Select AmazonMechanicalTurkFullAccess like: ![alt text](instruction5.PNG)
13) Insert new key like: ![alt text](instruction6.PNG)
14) Select Next, and Create User.
15) Copy the two keys and paste it in [Key.py](https://github.com/edoardore/MTurkTools/blob/master/src/Key.py): ![alt text](instruction7.PNG) 
## SetUp Amazon S3:
1) Sign in [here](https://s3.console.aws.amazon.com/s3/home?region=eu-central-1#) with AWS UserID and password created earlier.
2) Create (in different times) two new buckets named: `imagesformturk` and `videosformturk`.
3) Deselect `Block all public access` here: ![alt text](instruction8.PNG)
4) Press Create Bucket.
5) In `imagesformturk` open bucket -> go to authorization -> Policy Bucket and paste:
```{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::imagesformturk/*"
        }
    ]
}
```
6) In `videosformturk` open bucket -> go to authorization -> Policy Bucket and paste:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::videosformturk/*"
        }
    ]
}
```

Now it's all setted up! The tool can work correctly.
Use the [requirement.txt](https://github.com/edoardore/MTurkTools/blob/master/requirements.txt) to recreate the virtual env for the project.


### Views:
1) Create a new Task, choosing from Image or Video Tasks.
2) Select files to upload on Amazon MTurk.
3) View of all Tasks precedently created.
4) It's possible to refresh the results of workers.
5) Each Task has a personalized dashboard with adaptive queries that shows the results.
6) It's possible to create other Tasks from the home view.

## Dashboard:
1) Evaluation History of single file (of the selected Task). Type: Line Graph.
2) Evaluation History of single worker (that evaluates some HITs in the task selected). Type: Line Graph.
3) Comparison of the evaluation done by two different workers (that evaluates some HITs in the task selected). Type: Radar Graph.
4) Single file evaluation results. Type: Pie Graph.
5) Workers ordered by the number of submitted HITs. Type: Bar Graph.
6) Number of submitted HITs by workers and average of the evaluation vote that they have assigned. Type: Scatter Graph.
7) Liar workers ordered by the number of times that they assigned random value in age and sex field. Type: Bar Graph.
8) Results showed based on sex: male/female. Type: Pie Graph.
9) Percents of the screen resolution of the workers. Type: Bar Graph.
10) Percents of the age of the workers. Type: Bar Graph.
11) Average and standard deviation of each file evaluated in the task; and average of all the votes of the task. Type: Line Graph.
12) Modular multiple graph with 3 of the precedent views.


## License
[Edoardo Re](https://github.com/edoardore), 2019

[Chart.js](https://www.chartjs.org)
